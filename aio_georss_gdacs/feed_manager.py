"""Feed Manager for GDACS feed."""
from __future__ import annotations

from typing import Awaitable, Callable

from aio_georss_client.feed_manager import FeedManagerBase
from aio_georss_client.status_update import StatusUpdate
from aiohttp import ClientSession

from .feed import GdacsFeed


class GdacsFeedManager(FeedManagerBase):
    """Feed Manager for GDACS feed."""

    def __init__(
        self,
        websession: ClientSession,
        generate_async_callback: Callable[[str], Awaitable[None]],
        update_async_callback: Callable[[str], Awaitable[None]],
        remove_async_callback: Callable[[str], Awaitable[None]],
        coordinates: tuple[float, float],
        filter_radius: float | None = None,
        filter_categories: list[str] | None = None,
        status_async_callback: Callable[[StatusUpdate], Awaitable[None]] = None,
    ):
        """Initialize the GDACS Feed Manager."""
        feed = GdacsFeed(
            websession,
            coordinates,
            filter_radius=filter_radius,
            filter_categories=filter_categories,
        )
        super().__init__(
            feed,
            generate_async_callback,
            update_async_callback,
            remove_async_callback,
            status_async_callback,
        )
