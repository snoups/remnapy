from datetime import datetime, timedelta

import pytest
import pytz

from remnapy.models import BulkUpdateUsersRequestDto, UpdateUserFields
from tests.conftest import REMNAWAVE_USER_ID


@pytest.mark.asyncio
async def test_users_bulk_actions(remnawave):
    expire_at = datetime.now(tz=pytz.utc) + timedelta(days=14)
    description = "TEST_DESCRIPTION"

    bulk_update_users = await remnawave.users_bulk_actions.bulk_update_users(
        body=BulkUpdateUsersRequestDto(
            user_ids=[REMNAWAVE_USER_ID],
            fields=UpdateUserFields(
                expire_at=expire_at,
                description=description,
            ),
        ),
    )
    assert bulk_update_users is None
    assert bulk_update_users is None
