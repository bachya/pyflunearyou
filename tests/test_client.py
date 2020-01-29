"""Define tests for the client object."""
import aiohttp
import pytest

from pyflunearyou import Client
from pyflunearyou.errors import RequestError

from .common import load_fixture


@pytest.mark.asyncio
async def test_request_error(aresponses):
    """Test that a bad API endpoint raises the correct exception."""
    aresponses.add(
        "api.v2.flunearyou.org",
        "/map/markers",
        "get",
        aresponses.Response(text=load_fixture("user_report_response.json"), status=200),
    )
    aresponses.add(
        "api.v2.flunearyou.org",
        "/bad/endpoint",
        "get",
        aresponses.Response(text="", status=404),
    )

    with pytest.raises(RequestError):
        async with aiohttp.ClientSession() as websession:
            client = Client(websession)
            await client._request("get", "bad/endpoint")
