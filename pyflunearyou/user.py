"""Define endpoints related to user reports."""
import logging
from typing import Callable, Coroutine

from aiocache import cached

from .report import Report
from .util import haversine

_LOGGER = logging.getLogger(__name__)


class UserReport(Report):
    """Define a single class to handle these endpoints."""

    def __init__(
            self, request: Callable[..., Coroutine],
            get_raw_data: Callable[..., Coroutine],
            cache_seconds: int) -> None:
        """Initialize."""
        super().__init__(request, get_raw_data, cache_seconds)
        self.raw_data = cached(ttl=self._cache_seconds)(self._raw_user_data)

    async def _raw_user_data(self) -> dict:
        """Return the raw user data."""
        return await self._get_raw_data('map/markers')

    async def status_by_coordinates(
            self, latitude: float, longitude: float) -> dict:
        """Get symptom data for the location nearest to the user's lat/lon."""
        data = [
            d for d in await self.raw_data()
            if d['latitude'] and d['longitude']
        ]
        closest = min(
            data,
            key=lambda p: haversine(
                latitude,
                longitude,
                float(p['latitude']),
                float(p['longitude'])
            ))
        return closest

    async def status_by_zip(self, zip_code: str) -> dict:
        """Get symptom data for the provided ZIP code."""
        try:
            [info] = [d for d in await self.raw_data() if d['zip'] == zip_code]
        except ValueError:
            return {}

        return info
