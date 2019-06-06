"""Define a client to interact with Flu Near You."""
import logging

from aiohttp import ClientSession, client_exceptions

from .cdc import CdcReport
from .errors import RequestError
from .user import UserReport

_LOGGER = logging.getLogger(__name__)

DEFAULT_CACHE_SECONDS = 60 * 60
DEFAULT_HOST = "api.v2.flunearyou.org"
DEFAULT_ORIGIN = "https://flunearyou.org"
DEFAULT_USER_AGENT = "Home Assistant (Macintosh; OS X/10.14.0) GCDHTTPRequest"

API_URL_SCAFFOLD = "https://{0}".format(DEFAULT_HOST)


class Client:  # pylint: disable=too-few-public-methods
    """Define the client."""

    def __init__(
        self, websession: ClientSession, *, cache_seconds: int = DEFAULT_CACHE_SECONDS
    ) -> None:
        """Initialize."""
        self._cache_seconds = cache_seconds
        self._websession = websession
        self.cdc_reports = CdcReport(self._request, cache_seconds)
        self.user_reports = UserReport(self._request, cache_seconds)

    async def _request(
        self, method: str, endpoint: str, *, headers: dict = None
    ) -> dict:
        """Make a request against air-matters.com."""
        url = "{0}/{1}".format(API_URL_SCAFFOLD, endpoint)

        if not headers:
            headers = {}
        headers.update(
            {
                "Host": DEFAULT_HOST,
                "Origin": DEFAULT_ORIGIN,
                "Referer": DEFAULT_ORIGIN,
                "User-Agent": DEFAULT_USER_AGENT,
            }
        )

        async with self._websession.request(method, url, headers=headers) as resp:
            try:
                resp.raise_for_status()
                return await resp.json(content_type=None)
            except client_exceptions.ClientError as err:
                raise RequestError(
                    "Error requesting data from {0}: {1}".format(endpoint, err)
                ) from None
