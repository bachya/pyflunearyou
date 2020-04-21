"""Define tests for the client object."""
import aiohttp
import pytest

from pyflunearyou import Client
from pyflunearyou.errors import RequestError


@pytest.mark.asyncio
async def test_request_error(aresponses):
    """Test that a bad API endpoint raises the correct exception."""
    aresponses.add(
        "api.v2.flunearyou.org",
        "/bad/endpoint",
        "get",
        aresponses.Response(text="", status=404),
    )

    with pytest.raises(RequestError):
        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client._request(  # pylint: disable=protected-access
                "get", "bad/endpoint"
            )
