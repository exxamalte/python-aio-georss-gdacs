"""Test for the GDACS feed manager."""

import asyncio
import datetime
from http import HTTPStatus

import aiohttp
import pytest
import pytz

from aio_georss_gdacs.feed_manager import GdacsFeedManager
from tests.utils import load_fixture


@pytest.mark.asyncio
async def test_feed_manager(mock_aioresponse):
    """Test the feed manager."""
    home_coordinates = (-41.2, 174.7)
    mock_aioresponse.get(
        "https://www.gdacs.org/xml/rss.xml",
        status=HTTPStatus.OK,
        body=load_fixture("gdacs-1.xml"),
    )

    async with aiohttp.ClientSession(loop=asyncio.get_running_loop()) as websession:
        # This will just record calls and keep track of external ids.
        generated_entity_external_ids = []
        updated_entity_external_ids = []
        removed_entity_external_ids = []

        async def _generate_entity(external_id: str) -> None:
            """Generate new entity."""
            generated_entity_external_ids.append(external_id)

        async def _update_entity(external_id: str) -> None:
            """Update entity."""
            updated_entity_external_ids.append(external_id)

        async def _remove_entity(external_id: str) -> None:
            """Remove entity."""
            removed_entity_external_ids.append(external_id)

        feed_manager = GdacsFeedManager(
            websession,
            _generate_entity,
            _update_entity,
            _remove_entity,
            home_coordinates,
        )
        assert (
            repr(feed_manager) == "<GdacsFeedManager("
            "feed=<GdacsFeed(home=(-41.2, 174.7), "
            "url=https://www.gdacs.org/xml/"
            "rss.xml, "
            "radius=None, categories=None)>)>"
        )
        await feed_manager.update()
        entries = feed_manager.feed_entries
        assert entries is not None
        assert len(entries) == 4
        assert feed_manager.last_timestamp == datetime.datetime(
            2019, 12, 30, 1, 27, 0, tzinfo=pytz.utc
        )
        assert len(generated_entity_external_ids) == 4
        assert len(updated_entity_external_ids) == 0
        assert len(removed_entity_external_ids) == 0
