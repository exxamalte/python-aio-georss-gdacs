"""GDACS feed."""
import logging
from typing import Dict, List, Tuple

from aio_georss_client.feed import GeoRssFeed
from aio_georss_client.xml_parser.feed_item import FeedItem
from aiohttp import ClientSession

from .consts import URL
from .feed_entry import GdacsFeedEntry

_LOGGER = logging.getLogger(__name__)


class GdacsFeed(GeoRssFeed[GdacsFeedEntry]):
    """GDACS feed."""

    def __init__(
        self,
        websession: ClientSession,
        home_coordinates: Tuple[float, float],
        filter_radius: float = None,
        filter_categories: List[str] = None,
    ):
        """Initialise this service."""
        super().__init__(
            websession,
            home_coordinates,
            URL,
            filter_radius=filter_radius,
            filter_categories=filter_categories,
        )

    def _new_entry(
        self,
        home_coordinates: Tuple[float, float],
        feature: FeedItem,
        global_data: Dict,
    ) -> GdacsFeedEntry:
        """Generate a new entry."""
        return GdacsFeedEntry(home_coordinates, feature)
