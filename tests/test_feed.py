"""Test for the GDACS feed."""
import asyncio
import datetime
from http import HTTPStatus

import aiohttp
import pytest
import pytz
from aio_georss_client.consts import UPDATE_OK, UPDATE_OK_NO_DATA

from aio_georss_gdacs.consts import ATTRIBUTION
from aio_georss_gdacs.feed import GdacsFeed
from tests.utils import load_fixture


@pytest.mark.asyncio
async def test_update_ok(mock_aioresponse):
    """Test updating feed is ok."""
    home_coordinates = (-41.2, 174.7)
    mock_aioresponse.get(
        "https://www.gdacs.org/xml/rss.xml",
        status=HTTPStatus.OK,
        body=load_fixture("gdacs-1.xml"),
    )

    async with aiohttp.ClientSession(loop=asyncio.get_running_loop()) as websession:
        feed = GdacsFeed(websession, home_coordinates)
        assert (
            repr(feed) == "<GdacsFeed(home=(-41.2, 174.7), "
            "url=https://www.gdacs.org/xml/rss.xml, "
            "radius=None, categories=None)>"
        )
        status, entries = await feed.update()
        assert status == UPDATE_OK
        assert entries is not None
        assert len(entries) == 4

        feed_entry = entries[0]
        assert feed_entry is not None
        assert (
            feed_entry.title
            == "Green alert for tropical cyclone CALVINIA-19. Population affected by Category 1 (120 km/h) wind speeds or higher is 0."
        )
        assert feed_entry.external_id == "TC1000643"
        assert feed_entry.coordinates[0] == pytest.approx(-19.4)
        assert feed_entry.coordinates[1] == pytest.approx(59.8)
        assert round(abs(feed_entry.distance_to_home - 10517.9), 1) == 0
        assert repr(feed_entry) == "<GdacsFeedEntry(id=TC1000643)>"
        assert feed_entry.attribution == ATTRIBUTION
        assert feed_entry.category == "Tropical Cyclone"
        assert feed_entry.alert_level == "Green"
        assert feed_entry.country == "Mauritius"
        assert feed_entry.duration_in_week == 0
        assert feed_entry.event_id == 1000643
        assert feed_entry.event_name == "CALVINIA-19"
        assert feed_entry.event_type_short == "TC"
        assert feed_entry.event_type == "Tropical Cyclone"
        assert feed_entry.from_date == datetime.datetime(
            2019, 12, 29, 12, 0, 0, tzinfo=pytz.utc
        )
        assert feed_entry.to_date == datetime.datetime(
            2019, 12, 29, 12, 0, 0, tzinfo=pytz.utc
        )
        assert (
            feed_entry.icon_url
            == "http://www.gdacs.org/Images/gdacs_icons/alerts/Green/TC.png"
        )
        assert feed_entry.is_current is True
        assert (
            feed_entry.population
            == "Population affected by Category 1 (120 km/h) wind speeds or higher is 0"
        )
        assert feed_entry.severity == "Tropical Storm (maximum wind speed of 93 km/h)"
        assert feed_entry.temporary is False
        assert feed_entry.version == 1
        assert feed_entry.vulnerability == "Medium"
        assert feed_entry.published == datetime.datetime(
            2019, 12, 29, 12, 0, 0, tzinfo=pytz.utc
        )

        feed_entry = entries[1]
        assert feed_entry is not None
        assert (
            feed_entry.title
            == "Green earthquake alert (Magnitude 5.5M, Depth:10km) in South Africa 28/12/2019 15:36 UTC, No people within 100km."
        )
        assert feed_entry.external_id == "EQ1199929"
        assert feed_entry.vulnerability == 5.01535213120674

        feed_entry = entries[2]
        assert feed_entry is not None


@pytest.mark.asyncio
async def test_update_ok_with_categories_filter(mock_aioresponse):
    """Test updating feed is ok with categories filter."""
    home_coordinates = (-41.2, 174.7)
    mock_aioresponse.get(
        "https://www.gdacs.org/xml/rss.xml",
        status=HTTPStatus.OK,
        body=load_fixture("gdacs-1.xml"),
    )

    async with aiohttp.ClientSession(loop=asyncio.get_running_loop()) as websession:
        feed = GdacsFeed(websession, home_coordinates, filter_categories=["Drought"])
        assert (
            repr(feed) == "<GdacsFeed(home=(-41.2, 174.7), "
            "url=https://www.gdacs.org/xml/rss.xml, "
            "radius=None, categories=['Drought'])>"
        )
        status, entries = await feed.update()
        assert status == UPDATE_OK
        assert entries is not None
        assert len(entries) == 2

        feed_entry = entries[0]
        assert feed_entry is not None
        assert feed_entry.title == "Drought is on going in Bulgaria, Iraq, Iran, Turkey"
        assert feed_entry.external_id == "DR1013682"
        assert feed_entry.coordinates[0] == pytest.approx(39.544)
        assert feed_entry.coordinates[1] == pytest.approx(31.926)
        assert round(abs(feed_entry.distance_to_home - 16880.3), 1) == 0
        assert repr(feed_entry) == "<GdacsFeedEntry(id=DR1013682)>"

        feed_entry = entries[1]
        assert feed_entry is not None
        assert feed_entry.external_id == "DR1013588"


@pytest.mark.asyncio
async def test_empty_feed(mock_aioresponse):
    """Test updating feed is ok when feed does not contain any entries."""
    home_coordinates = (-41.2, 174.7)
    mock_aioresponse.get(
        "https://www.gdacs.org/xml/rss.xml",
        status=HTTPStatus.OK,
        body=load_fixture("gdacs-2.xml"),
    )

    async with aiohttp.ClientSession(loop=asyncio.get_running_loop()) as websession:
        feed = GdacsFeed(websession, home_coordinates)
        assert (
            repr(feed) == "<GdacsFeed(home=(-41.2, 174.7), "
            "url=https://www.gdacs.org/xml/rss.xml, "
            "radius=None, categories=None)>"
        )
        status, entries = await feed.update()
        assert status == UPDATE_OK
        assert entries is not None
        assert len(entries) == 0
        assert feed.last_timestamp is None


@pytest.mark.asyncio
async def test_update_not_xml(mock_aioresponse):
    """Test updating feed where returned payload is not XML."""
    # During tests it turned out that occasionally the GDACS server appears to return
    # invalid payload (00 control characters) which results in an exception thrown:
    # ExpatError: not well-formed (invalid token): line 1, column 0
    home_coordinates = (-41.2, 174.7)
    not_xml = "\x00\x00\x00"
    mock_aioresponse.get(
        "https://www.gdacs.org/xml/rss.xml",
        status=HTTPStatus.OK,
        body=not_xml,
    )

    async with aiohttp.ClientSession(loop=asyncio.get_running_loop()) as websession:
        feed = GdacsFeed(websession, home_coordinates)
        assert (
            repr(feed) == "<GdacsFeed(home=(-41.2, 174.7), "
            "url=https://www.gdacs.org/xml/rss.xml, radius=None, "
            "categories=None)>"
        )
        status, entries = await feed.update()
        assert status == UPDATE_OK_NO_DATA
        assert entries is None
