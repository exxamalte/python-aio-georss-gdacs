"""Feed Manager for GDACS feed."""
from aio_georss_client.feed_manager import FeedManagerBase
from aiohttp import ClientSession

from .feed import GdacsFeed


class GdacsFeedManager(FeedManagerBase):
    """Feed Manager for GDACS feed."""

    def __init__(self,
                 websession: ClientSession,
                 generate_callback,
                 update_callback,
                 remove_callback,
                 coordinates,
                 filter_radius=None,
                 filter_categories=None,
                 status_callback=None):
        """Initialize the GDACS Feed Manager."""
        feed = GdacsFeed(
            websession,
            coordinates,
            filter_radius=filter_radius,
            filter_categories=filter_categories)
        super().__init__(feed,
                         generate_callback,
                         update_callback,
                         remove_callback,
                         status_callback)
