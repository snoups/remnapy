"""Утилиты для сверки SDK со спекой OpenAPI Remnawave."""

from __future__ import annotations

import ast
import json
import re
import typing
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

from pydantic import BaseModel

SPEC_PATH = Path(__file__).parent / "spec" / "remnawave-3.2.1.json"
CONTROLLERS_DIR = Path(__file__).parent.parent / "remnapy" / "controllers"

HTTP_METHODS = ("get", "post", "put", "patch", "delete")

# Глубина разворачивания вложенных структур. Одинаковая для схем и моделей,
# иначе на глубоких деревьях появятся ложные расхождения.
MAX_DEPTH = 16


@dataclass(frozen=True)
class SdkEndpoint:
    """Endpoint, объявленный декоратором в контроллере SDK."""

    method: str
    path: str
    response_model: str | None
    body_model: str | None
    func: str
    file: str


@lru_cache(maxsize=1)
def load_spec() -> dict[str, Any]:
    """Загрузить спеку OpenAPI."""
    with SPEC_PATH.open(encoding="utf-8") as fh:
        return json.load(fh)


def normalize_path(path: str) -> str:
    """Заменить имена path-параметров на плейсхолдеры: /users/{userId} -> /users/{}."""
    return re.sub(r"\{[^}]+\}", "{}", path)


@lru_cache(maxsize=1)
def spec_endpoints() -> dict[tuple[str, str], dict[str, Any]]:
    """Endpoint'ы спеки. Ключ — (МЕТОД, путь без префикса /api)."""
    spec = load_spec()
    result: dict[tuple[str, str], dict[str, Any]] = {}
    for path, operations in spec["paths"].items():
        sdk_path = path[len("/api") :] if path.startswith("/api") else path
        for method, operation in operations.items():
            if method in HTTP_METHODS:
                result[(method.upper(), sdk_path)] = operation
    return result


@lru_cache(maxsize=1)
def sdk_endpoints() -> dict[tuple[str, str], SdkEndpoint]:
    """Endpoint'ы, объявленные в контроллерах SDK."""
    result: dict[tuple[str, str], SdkEndpoint] = {}
    for source in sorted(CONTROLLERS_DIR.glob("*.py")):
        tree = ast.parse(source.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not isinstance(node, (ast.AsyncFunctionDef, ast.FunctionDef)):
                continue
            for decorator in node.decorator_list:
                endpoint = _parse_decorator(decorator, node, source.name)
                if endpoint is not None:
                    result[(endpoint.method, endpoint.path)] = endpoint
    return result


def _parse_decorator(
    decorator: ast.expr, func: ast.AsyncFunctionDef | ast.FunctionDef, filename: str
) -> SdkEndpoint | None:
    if not isinstance(decorator, ast.Call) or not isinstance(decorator.func, ast.Name):
        return None
    if decorator.func.id not in HTTP_METHODS:
        return None
    if not decorator.args or not isinstance(decorator.args[0], ast.Constant):
        return None

    response_model = None
    for keyword in decorator.keywords:
        if keyword.arg == "response_class" and isinstance(keyword.value, ast.Name):
            response_model = keyword.value.id

    body_model = None
    for arg in func.args.args:
        if arg.arg == "body" and arg.annotation is not None:
            match = re.search(r"Annotated\[\s*([A-Za-z_0-9]+)", ast.unparse(arg.annotation))
            if match:
                body_model = match.group(1)

    return SdkEndpoint(
        method=decorator.func.id.upper(),
        path=decorator.args[0].value,
        response_model=response_model,
        body_model=body_model,
        func=func.name,
        file=filename,
    )


def schema_fields(
    schema: dict[str, Any] | None, spec: dict[str, Any], *, strip_response: bool = True
) -> set[str]:
    """Развернуть JSON-схему в плоское множество путей полей.

    Массивы обозначаются суффиксом `[]`, вложенность — точкой:
    `users[]activeInternalSquads[]uuid`. Конверт `response` снимается, если
    `strip_response=True` (по умолчанию; выключайте для схем тела запроса —
    там поле `response`, если есть, настоящее, а не конверт).

    Если снимать конверт не с чего (всё содержимое схемы/модели — это сам
    конверт целиком, без единого вложенного свойства, напр.
    `{"response": {}}`), поле остаётся под именем конверта (`response`
    / `root`) вместо того, чтобы схлопнуться в пустую строку — иначе такой
    endpoint пропадает из отчёта вместо того, чтобы быть в нём поимённо
    (см. `_strip_envelope`).
    """
    fields = _walk_schema(schema, spec, seen=frozenset(), depth=0)
    return {_strip_envelope(field, strip_response=strip_response) for field in fields}


def _walk_schema(
    node: dict[str, Any] | None,
    spec: dict[str, Any],
    seen: frozenset[str],
    depth: int,
) -> set[str]:
    if node is None or depth > MAX_DEPTH:
        return set()

    if "$ref" in node:
        name = node["$ref"].rsplit("/", 1)[-1]
        if name in seen:
            return set()
        target = spec["components"]["schemas"].get(name, {})
        return _walk_schema(target, spec, seen | {name}, depth + 1)

    for combinator in ("allOf", "oneOf", "anyOf"):
        if combinator in node:
            combined: set[str] = set()
            for sub in node[combinator]:
                combined |= _walk_schema(sub, spec, seen, depth + 1)
            return combined

    if node.get("type") == "array":
        return {f"[]{field}" for field in _walk_schema(node.get("items"), spec, seen, depth + 1)}

    if "properties" in node:
        fields: set[str] = set()
        for name, sub in node["properties"].items():
            children = _walk_schema(sub, spec, seen, depth + 1)
            if children:
                fields |= {f"{name}{'' if child.startswith('[]') else '.'}{child}" for child in children}
            else:
                fields.add(name)
        return fields

    return set()


def model_fields(model: type, *, strip_response: bool = True) -> set[str]:
    """Развернуть pydantic-модель в плоское множество путей полей.

    Формат путей совпадает с `schema_fields`. Обёртка `RootModel` снимается.
    `strip_response` управляет тем, снимается ли конверт `response` (см.
    `_strip_envelope`) — для тел запросов его нужно отключать.

    Как и в `schema_fields`, поле, которое нечего снимать кроме самого
    конверта, остаётся под именем конверта, а не схлопывается в пустую
    строку.
    """
    fields = _walk_model(model, seen=frozenset(), depth=0)
    return {_strip_envelope(field, strip_response=strip_response) for field in fields}


def _walk_model(model: type, seen: frozenset[type], depth: int) -> set[str]:
    if depth > MAX_DEPTH or model in seen or not hasattr(model, "model_fields"):
        return set()

    fields: set[str] = set()
    for name, field in model.model_fields.items():
        alias = field.alias or field.serialization_alias or field.validation_alias or name
        if not isinstance(alias, str):
            alias = name

        children = _annotation_fields(field.annotation, seen | {model}, depth + 1)
        if children:
            fields |= {f"{alias}{'' if child.startswith('[]') else '.'}{child}" for child in children}
        else:
            fields.add(alias)
    return fields


def _annotation_fields(annotation: Any, seen: frozenset[type], depth: int) -> set[str]:
    """Поля вложенной модели внутри аннотации (Optional, Union, list и т. п.)."""
    result: set[str] = set()
    for candidate in _unwrap_annotation(annotation):
        if isinstance(candidate, type) and issubclass(candidate, BaseModel):
            result |= _walk_model(candidate, seen, depth)
            continue
        origin = typing.get_origin(candidate)
        if origin in (list, set, tuple):
            args = typing.get_args(candidate)
            if args:
                nested = _annotation_fields(args[0], seen, depth)
                result |= {f"[]{field}" for field in nested}
    return result


def _unwrap_annotation(annotation: Any) -> list[Any]:
    """Развернуть Optional/Union/Annotated в список кандидатов."""
    origin = typing.get_origin(annotation)
    if origin is typing.Union or getattr(origin, "__name__", None) == "UnionType":
        return [arg for arg in typing.get_args(annotation) if arg is not type(None)]
    if origin is typing.Annotated or getattr(annotation, "__metadata__", None) is not None:
        args = typing.get_args(annotation)
        if args:
            return _unwrap_annotation(args[0])
    return [annotation]


def _strip_envelope(field: str, *, strip_response: bool = True) -> str:
    """Убрать внешний конверт `response.` (спека) или `root.` (RootModel).

    Конверт `response` существует только у схем ответа — панель никогда не
    оборачивает в него тело запроса, поэтому у request-схем/моделей поле
    `response`, если оно есть, настоящее и не должно вырезаться
    (`strip_response=False`). Конверт `root` (разворачивание pydantic
    `RootModel`) — отдельная механика и снимается всегда.

    Если поле — это конверт целиком и снимать нечего (напр. схема ответа
    `{"response": {}}` без единого вложенного свойства, или модель без полей),
    имя конверта не срезается до пустой строки: пустая строка — это не имя
    поля, а исчезновение endpoint'а из отчёта. Вместо этого возвращается имя
    самого конверта (`response`/`root`), чтобы такой endpoint остался в
    выводе под читаемым именем.
    """
    envelopes = ("response", "root") if strip_response else ("root",)
    for envelope in envelopes:
        if field == envelope:
            return field
        if field.startswith(f"{envelope}."):
            return field[len(envelope) + 1 :]
        if field.startswith(f"{envelope}[]"):
            return field[len(envelope) :]
    return field


def response_schema(operation: dict[str, Any]) -> dict[str, Any] | None:
    """Схема успешного ответа операции (200 или 201)."""
    for code in ("200", "201"):
        response = operation.get("responses", {}).get(code)
        if response is None:
            continue
        return response.get("content", {}).get("application/json", {}).get("schema")
    return None


def request_schema(operation: dict[str, Any]) -> dict[str, Any] | None:
    """Схема тела запроса операции."""
    body = operation.get("requestBody", {})
    return body.get("content", {}).get("application/json", {}).get("schema")


def spec_path_params(path: str) -> list[str]:
    """Имена path-параметров в порядке появления."""
    return re.findall(r"\{([^}]+)\}", path)
