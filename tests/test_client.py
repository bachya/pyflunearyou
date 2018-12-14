"""Define tests for the client object."""
import json

import aiohttp
import pytest

from pyflunearyou import Client
from pyflunearyou.errors import RequestError

from .fixtures.user import fixture_user_report_json


@pytest.mark.asyncio
async def test_request_error(aresponses, event_loop, fixture_user_report_json):
    """Test that a bad API endpoint raises the correct exception."""
    aresponses.add(
        'api.v2.flunearyou.org', '/map/markers', 'get',
        aresponses.Response(
            text=json.dumps(fixture_user_report_json), status=200))
    aresponses.add(
        'api.v2.flunearyou.org', '/bad/endpoint', 'get',
        aresponses.Response(text='', status=404))

    with pytest.raises(RequestError):
        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = Client(websession)
            await client._request('get', 'bad/endpoint')
