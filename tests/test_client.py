"""Define tests for the client object."""
import json

import aiohttp
import pytest

from pyflunearyou import create_client
from pyflunearyou.errors import RequestError

from .const import TEST_LATITUDE, TEST_LONGITUDE
from .fixtures.user import fixture_user_report_json


@pytest.mark.asyncio
async def test_client_creation(
        aresponses, event_loop, fixture_user_report_json):
    """Test creating a client."""
    aresponses.add(
        'api.v2.flunearyou.org', '/map/markers', 'get',
        aresponses.Response(
            text=json.dumps(fixture_user_report_json), status=200))

    # with pytest.raises(InvalidApiKeyError):
    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = await create_client(TEST_LATITUDE, TEST_LONGITUDE, websession)

        assert client.city == 'Los Angeles'
        assert client.zip_code == '90046'


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
            client = await create_client(
                TEST_LATITUDE, TEST_LONGITUDE, websession)
            await client._request('get', 'bad/endpoint')
