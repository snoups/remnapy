import pytest

from remnapy.enums import TemplateType
from remnapy.models import (
    CreateSubscriptionTemplateRequestDto,
    CreateSubscriptionTemplateResponseDto,
    GetTemplateResponseDto,
    GetTemplatesResponseDto,
    ReorderSubscriptionTemplatesRequestDto,
    ReorderSubscriptionTemplatesResponseDto,
    ReorderTemplateItem,
    UpdateTemplateRequestDto,
    UpdateTemplateResponseDto,
)


def random_string(length=10):
    import random
    import string

    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


@pytest.mark.asyncio
async def test_get_all_templates(remnawave):
    """Fetching all templates"""
    templates = await remnawave.subscriptions_template.get_all_templates()
    assert isinstance(templates, GetTemplatesResponseDto)


@pytest.mark.asyncio
async def test_create_template(remnawave):
    """Creating a template"""
    rand_name = random_string()
    create_request = CreateSubscriptionTemplateRequestDto(
        name=rand_name,
        template_type=TemplateType.SINGBOX,
    )
    created_template = await remnawave.subscriptions_template.create_template(
        create_request
    )
    assert isinstance(created_template, CreateSubscriptionTemplateResponseDto)
    assert created_template.name == rand_name
    assert created_template.template_type == TemplateType.SINGBOX

    await remnawave.subscriptions_template.delete_template(str(created_template.uuid))


@pytest.fixture
async def created_template(remnawave):
    """Create a temporary template and remove it after the test."""
    create_request = CreateSubscriptionTemplateRequestDto(
        name="Temp Template",
        template_type=TemplateType.SINGBOX,
    )
    template = await remnawave.subscriptions_template.create_template(create_request)
    yield template
    await remnawave.subscriptions_template.delete_template(str(template.uuid))


@pytest.mark.asyncio
async def test_get_template_by_uuid(remnawave, created_template):
    """Fetching a template by UUID"""
    template = await remnawave.subscriptions_template.get_template_by_uuid(
        str(created_template.uuid)
    )
    assert isinstance(template, GetTemplateResponseDto)
    assert template.uuid == created_template.uuid


@pytest.mark.asyncio
async def test_update_template(remnawave, created_template):
    """Updating a template"""
    update_request = UpdateTemplateRequestDto(
        uuid=created_template.uuid,
        name="Updated Template Name",
    )
    updated_template = await remnawave.subscriptions_template.update_template(
        update_request
    )
    assert isinstance(updated_template, UpdateTemplateResponseDto)
    assert updated_template.name == "Updated Template Name"


@pytest.mark.asyncio
async def test_delete_template(remnawave):
    """Deleting a template"""
    create_request = CreateSubscriptionTemplateRequestDto(
        name="Temp Delete Template",
        template_type=TemplateType.SINGBOX,
    )
    created = await remnawave.subscriptions_template.create_template(create_request)

    delete_response = await remnawave.subscriptions_template.delete_template(
        str(created.uuid)
    )
    assert delete_response is None
    assert delete_response is None


@pytest.mark.asyncio
async def test_reorder_templates(remnawave):
    """Reordering templates"""
    templates = await remnawave.subscriptions_template.get_all_templates()
    assert isinstance(templates, GetTemplatesResponseDto)

    if len(templates.templates) >= 2:
        items = [
            ReorderTemplateItem(uuid=tmpl.uuid, view_position=idx)
            for idx, tmpl in enumerate(templates.templates)
        ]
        reorder_result = await remnawave.subscriptions_template.reorder_templates(
            ReorderSubscriptionTemplatesRequestDto(items=items)
        )
        assert isinstance(reorder_result, ReorderSubscriptionTemplatesResponseDto)
