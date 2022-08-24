import logging

import pytest

logger = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_get(client):
    data = {
        'start_time': '2022-07-31 18:00:00',
        'stop_time': '2022-08-01 04:00:00',
    }
    result = await client.get('/api/v1/video/1', query_string=data)
    assert result.status_code == 200, f'Error with API {result.text=}'
    result_json = result.json()
    assert result_json['moda'] == 6
    assert result_json['data']['total'] == 5
    assert result_json['data']['items']['total_actions'] == 1995
    assert result_json['data']['items']['data'][0]['horse_id'] == 6
    assert result_json['data']['items']['data'][0]['total_actions'] == 1595
