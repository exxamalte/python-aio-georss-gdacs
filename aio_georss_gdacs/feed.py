"""GDACS feed."""
import logging

from aio_georss_client.feed import GeoRssFeed
from aiohttp import ClientSession

from .consts import URL
from .feed_entry import GdacsFeedEntry

_LOGGER = logging.getLogger(__name__)


class GdacsFeed(GeoRssFeed):
    """GDACS feed."""

    def __init__(self,
                 websession: ClientSession,
                 home_coordinates,
                 filter_radius: float = None,
                 filter_categories=None):
        """Initialise this service."""
        super().__init__(websession,
                         home_coordinates,
                         URL,
                         filter_radius=filter_radius,
                         filter_categories=filter_categories)
        self._entries = None

    def _new_entry(self, home_coordinates, feature, global_data):
        """Generate a new entry."""
        return GdacsFeedEntry(home_coordinates, feature)
