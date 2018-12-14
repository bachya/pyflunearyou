"""Define a generic report object."""
from typing import Callable, Coroutine


class Report:  # pylint: disable=too-few-public-methods
    """Define a generic report object."""

    def __init__(
            self, request: Callable[..., Coroutine],
            get_raw_data: Callable[..., Coroutine],
            cache_seconds: int) -> None:
        """Initialize."""
        self._cache_seconds = cache_seconds
        self._get_raw_data = get_raw_data
        self._request = request
