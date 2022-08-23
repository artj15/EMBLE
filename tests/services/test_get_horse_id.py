import logging

import pytest

logger = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_get(client):
    data = {
        'start_time': '2022-08-01 00:00:00',
        'stop_time': '2022-08-01 04:00:00',
    }
    result = await client.get('/api/v1/video/1', query_string=data)
    assert result.status_code == 200, f'Error with API {result.text=}'
    assert 0
