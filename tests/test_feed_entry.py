"""Test for the GDACS feed entry."""
import pytest

from aio_georss_gdacs.feed_entry import GdacsFeedEntry


@pytest.mark.asyncio
async def test_empty_feed_entry(aresponses, event_loop):
    """Test feed entry without underlying RSS data."""
    home_coordinates = (-41.2, 174.7)
    feed_entry = GdacsFeedEntry(home_coordinates, None)
    assert feed_entry.alert_level is None
    assert feed_entry.country is None
    assert feed_entry.duration_in_week is None
    assert feed_entry.event_name is None
    assert feed_entry.event_type is None
    assert feed_entry.event_type_long == "Unknown"
    assert feed_entry.from_date is None
    assert feed_entry.icon_url is None
    assert feed_entry.is_current is None
    assert feed_entry.population is None
    assert feed_entry.severity is None
    assert feed_entry.temporary is None
    assert feed_entry.to_date is None
    assert feed_entry.version is None
    assert feed_entry.vulnerability is None
