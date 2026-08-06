"""Сверка SDK с OpenAPI-спекой Remnawave 3.2.1.

Тесты офлайновые: живая панель не нужна, сравнивается только форма.
"""

import re

import pytest

import remnapy.models as models
from remnapy.enums.error_code import ErrorCode
from tests import spec_utils
from tests.spec_utils import (
    load_spec,
    model_fields,
    normalize_path,
    request_schema,
    response_schema,
    schema_fields,
    sdk_endpoints,
    spec_endpoints,
    spec_path_params,
    spec_query_params,
)

# Расхождения, признанные допустимыми. Каждая запись обязана нести причину.
ALLOWED_FIELD_DIFFS: dict[tuple[str, str], str] = {}

# Известные, но не устранённые в этой волне расхождения по query-параметрам.
# Ключ — (МЕТОД, нормализованный путь). Каждая запись обязана нести причину.
ALLOWED_QUERY_PARAM_DIFFS: dict[tuple[str, str], str] = {}


def _spec_by_shape() -> dict[tuple[str, str], tuple[str, dict]]:
    """Endpoint'ы спеки с нормализованными путями."""
    return {
        (method, normalize_path(path)): (path, operation)
        for (method, path), operation in spec_endpoints().items()
    }


def _sdk_by_shape() -> dict[tuple[str, str], spec_utils.SdkEndpoint]:
    return {
        (endpoint.method, normalize_path(endpoint.path)): endpoint
        for endpoint in sdk_endpoints().values()
    }


def test_no_missing_endpoints():
    """Каждый endpoint спеки объявлен в контроллерах SDK."""
    missing = sorted(set(_spec_by_shape()) - set(_sdk_by_shape()))
    assert not missing, "Нет в SDK:\n" + "\n".join(f"  {m} {p}" for m, p in missing)


def test_no_stale_endpoints():
    """В контроллерах SDK нет endpoint'ов, отсутствующих в спеке."""
    sdk = _sdk_by_shape()
    stale = sorted(set(sdk) - set(_spec_by_shape()))
    assert not stale, "Нет в спеке:\n" + "\n".join(
        f"  {m} {p} ({sdk[(m, p)].file}::{sdk[(m, p)].func})" for m, p in stale
    )


def test_path_params_match():
    """Имена path-параметров совпадают со спекой."""
    spec_shapes = _spec_by_shape()
    mismatches = []
    for shape, endpoint in _sdk_by_shape().items():
        if shape not in spec_shapes:
            continue
        spec_path, _ = spec_shapes[shape]
        expected = spec_path_params(spec_path)
        actual = spec_path_params(endpoint.path)
        if expected != actual:
            mismatches.append(f"  {endpoint.file}::{endpoint.func}: {endpoint.path} -> ожидается {spec_path}")
    assert not mismatches, "Path-параметры расходятся:\n" + "\n".join(mismatches)


def test_query_params_match():
    """Имена query-параметров совпадают со спекой (alias-aware)."""
    spec_shapes = _spec_by_shape()
    mismatches = []
    for shape, endpoint in sorted(_sdk_by_shape().items()):
        if shape not in spec_shapes:
            continue
        if shape in ALLOWED_QUERY_PARAM_DIFFS:
            continue
        _, operation = spec_shapes[shape]
        expected = spec_query_params(operation)
        actual = endpoint.query_params
        missing, extra = expected - actual, actual - expected
        if missing or extra:
            lines = [f"  {shape[0]} {shape[1]} ({endpoint.file}::{endpoint.func})"]
            lines += [f"    + нет в SDK: {name}" for name in sorted(missing)]
            lines += [f"    - лишнее в SDK: {name}" for name in sorted(extra)]
            mismatches.append("\n".join(lines))
    assert not mismatches, "Query-параметры расходятся:\n" + "\n".join(mismatches)


def _field_diff(
    model_name: str, schema: dict | None, spec: dict, *, strip_response: bool
) -> tuple[set[str], set[str]]:
    """(поля спеки, которых нет в модели; поля модели, которых нет в спеке).

    `strip_response` должен быть True только для схем/моделей ответа — тело
    запроса никогда не оборачивается в конверт `response`, и поле с таким
    именем там настоящее (см. `VerifyPasskeyRegistrationBodyDto`).
    """
    model = getattr(models, model_name, None)
    if model is None or not hasattr(model, "model_fields"):
        return set(), set()
    expected = schema_fields(schema, spec, strip_response=strip_response)
    actual = model_fields(model, strip_response=strip_response)
    return expected - actual, actual - expected


@pytest.mark.parametrize("kind", ["request", "response"])
def test_models_match_spec(kind):
    """Поля request/response моделей совпадают со схемами спеки."""
    spec = load_spec()
    spec_shapes = _spec_by_shape()
    problems = []

    for shape, endpoint in sorted(_sdk_by_shape().items()):
        if shape not in spec_shapes:
            continue
        _, operation = spec_shapes[shape]

        if kind == "response":
            model_name, schema = endpoint.response_model, response_schema(operation)
        else:
            model_name, schema = endpoint.body_model, request_schema(operation)

        if model_name is None or schema is None:
            continue
        if (model_name, kind) in ALLOWED_FIELD_DIFFS:
            continue

        missing, extra = _field_diff(model_name, schema, spec, strip_response=(kind == "response"))
        if missing or extra:
            lines = [f"  {shape[0]} {shape[1]} — {model_name} ({endpoint.file}::{endpoint.func})"]
            lines += [f"    + нет в SDK: {field}" for field in sorted(missing)]
            lines += [f"    - лишнее в SDK: {field}" for field in sorted(extra)]
            problems.append("\n".join(lines))

    assert not problems, f"Модели ({kind}) расходятся со спекой:\n" + "\n".join(problems)


def test_error_codes_complete():
    """ErrorCode покрывает все коды ошибок из спеки.

    Проверка односторонняя: в SDK есть коды рантайма панели (AUTH*, BL*, N*
    и др.), которых нет в документации, и они должны сохраниться.
    """
    import json

    spec_codes = set(re.findall(r'"([A-Z]\d{3})"', json.dumps(load_spec())))
    sdk_codes = {member.value for member in ErrorCode}
    missing = sorted(spec_codes - sdk_codes)
    assert not missing, f"Нет в ErrorCode: {missing}"


WEBHOOK_SCHEMAS = {
    "RemnawaveWebhookUserEventsDto": "UserEventDto",
    "RemnawaveWebhookUserHwidDevicesEventsDto": "UserHwidDeviceEventDto",
    "RemnawaveWebhookNodeEventsDto": "NodeEventDto",
    "RemnawaveWebhookServiceEventsDto": "ServiceEventDto",
    "RemnawaveWebhookErrorsEventsDto": "CustomErrorEventDto",
    "RemnawaveWebhookCrmEventsDto": "CrmEventDto",
    "RemnawaveWebhookTorrentBlockerEventsDto": "TorrentBlockerEventDto",
}


def test_webhook_models_match():
    """Модели вебхуков совпадают со схемами RemnawaveWebhook*EventsDto."""
    from remnapy.models import webhook as webhook_models

    spec = load_spec()
    problems = []
    for schema_name, model_name in WEBHOOK_SCHEMAS.items():
        schema = spec["components"]["schemas"][schema_name]
        model = getattr(webhook_models, model_name)
        expected = schema_fields(schema, spec)
        actual = model_fields(model)
        missing, extra = expected - actual, actual - expected
        if missing or extra:
            lines = [f"  {schema_name} — {model_name}"]
            lines += [f"    + нет в SDK: {field}" for field in sorted(missing)]
            lines += [f"    - лишнее в SDK: {field}" for field in sorted(extra)]
            problems.append("\n".join(lines))

    assert not problems, "Модели вебхуков расходятся со спекой:\n" + "\n".join(problems)


@pytest.mark.parametrize("nullable_as_null", [False, True], ids=["заполнено", "nullable=null"])
def test_webhook_models_accept_spec_payloads(nullable_as_null):
    """Модели вебхуков принимают payload, построенный по спеке.

    Проверка имён полей (`test_webhook_models_match`) не видит ни типов, ни
    обязательности. Вебхуки приходят с панели, а не запрашиваются, поэтому
    иначе их разбор не проверить — отсюда построение payload'а из схемы.
    """
    from remnapy.models import webhook as webhook_models

    spec = load_spec()
    problems = []
    for schema_name, model_name in WEBHOOK_SCHEMAS.items():
        schema = spec["components"]["schemas"][schema_name]
        payload = spec_utils.sample_payload(schema, spec, nullable_as_null=nullable_as_null)
        try:
            getattr(webhook_models, model_name).model_validate(payload)
        except Exception as exc:  # noqa: BLE001
            problems.append(f"  {model_name}: {str(exc).splitlines()[0]}")

    assert not problems, "Модели вебхуков не разбирают payload из спеки:\n" + "\n".join(problems)
