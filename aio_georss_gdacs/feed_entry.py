"""GDACS feed entry."""
from collections.abc import Mapping
from datetime import datetime
from typing import List, Optional, Tuple, Type, Union

import dateparser
from aio_georss_client.feed_entry import FeedEntry
from aio_georss_client.xml_parser.feed_item import FeedItem
from aio_georss_client.xml_parser.geometry import Geometry, Point, Polygon

from .consts import (
    ATTRIBUTION,
    EVENT_TYPE_MAP,
    XML_ATTRIBUTE_VALUE,
    XML_TAG_GDACS_ALERT_LEVEL,
    XML_TAG_GDACS_COUNTRY,
    XML_TAG_GDACS_DURATION_IN_WEEK,
    XML_TAG_GDACS_EVENT_ID,
    XML_TAG_GDACS_EVENT_NAME,
    XML_TAG_GDACS_EVENT_TYPE,
    XML_TAG_GDACS_FROM_DATE,
    XML_TAG_GDACS_ICON,
    XML_TAG_GDACS_IS_CURRENT,
    XML_TAG_GDACS_POPULATION,
    XML_TAG_GDACS_SEVERITY,
    XML_TAG_GDACS_TEMPORARY,
    XML_TAG_GDACS_TO_DATE,
    XML_TAG_GDACS_VERSION,
    XML_TAG_GDACS_VULNERABILITY,
    XML_TEXT,
)


class GdacsFeedEntry(FeedEntry):
    """GDACS feed entry."""

    def __init__(self, home_coordinates: Tuple[float, float], feature: FeedItem):
        """Initialise this service."""
        super().__init__(home_coordinates, feature)

    @property
    def features(self) -> List[Type[Geometry]]:
        """Only consider Point and Polygon in this integration."""
        return [Point, Polygon]

    @property
    def attribution(self) -> Optional[str]:
        """Return the attribution of this entry."""
        return ATTRIBUTION

    @property
    def category(self) -> Optional[str]:
        """Return the category of this entry."""
        return self.event_type

    @property
    def alert_level(self) -> Optional[str]:
        """Return the alert level of this entry."""
        if self._rss_entry:
            return self._rss_entry.get_additional_attribute(XML_TAG_GDACS_ALERT_LEVEL)
        return None

    @property
    def country(self) -> Optional[str]:
        """Return the country of this entry."""
        if self._rss_entry:
            return self._rss_entry.get_additional_attribute(XML_TAG_GDACS_COUNTRY)
        return None

    @property
    def duration_in_week(self) -> Optional[int]:
        """Return the duration in weeks of this entry."""
        if self._rss_entry:
            # 0 = First week
            # 1 = Second week
            # etc.
            duration_in_week = self._rss_entry.get_additional_attribute(
                XML_TAG_GDACS_DURATION_IN_WEEK
            )
            if duration_in_week:
                return int(duration_in_week)
        return None

    @property
    def event_id(self) -> Optional[int]:
        """Return the event id of this entry."""
        if self._rss_entry:
            event_id = self._rss_entry.get_additional_attribute(XML_TAG_GDACS_EVENT_ID)
            if event_id:
                return int(event_id)
        return None

    @property
    def event_name(self) -> Optional[str]:
        """Return the event name of this entry."""
        if self._rss_entry:
            return self._rss_entry.get_additional_attribute(XML_TAG_GDACS_EVENT_NAME)
        return None

    @property
    def event_type_short(self) -> Optional[str]:
        """Return the short event type of this entry."""
        if self._rss_entry:
            return self._rss_entry.get_additional_attribute(XML_TAG_GDACS_EVENT_TYPE)
        return None

    @property
    def event_type(self) -> Optional[str]:
        """Return the event type of this entry."""
        event_type_short = self.event_type_short
        if event_type_short and event_type_short in EVENT_TYPE_MAP:
            return EVENT_TYPE_MAP[event_type_short]
        return "Unknown"

    @property
    def from_date(self) -> Optional[datetime]:
        """Return the from date of this entry."""
        if self._rss_entry:
            from_date = self._rss_entry.get_additional_attribute(
                XML_TAG_GDACS_FROM_DATE
            )
            if from_date:
                return dateparser.parse(from_date)
        return None

    @property
    def icon_url(self) -> Optional[str]:
        """Return the icon url of this entry."""
        if self._rss_entry:
            return self._rss_entry.get_additional_attribute(XML_TAG_GDACS_ICON)
        return None

    @property
    def is_current(self) -> Optional[bool]:
        """Return if this entry is current."""
        if self._rss_entry:
            is_current = self._rss_entry.get_additional_attribute(
                XML_TAG_GDACS_IS_CURRENT
            )
            if is_current:
                return FeedEntry._string2boolean(is_current)
        return None

    @property
    def population(self) -> Optional[str]:
        """Return the population of this entry."""
        if self._rss_entry:
            population = self._rss_entry.get_additional_attribute(
                XML_TAG_GDACS_POPULATION
            )
            if population:
                if isinstance(population, Mapping):
                    if XML_TEXT in population:
                        return population[XML_TEXT]
                else:
                    return population
        return None

    @property
    def severity(self) -> Optional[str]:
        """Return the severity of this entry."""
        if self._rss_entry:
            severity = self._rss_entry.get_additional_attribute(XML_TAG_GDACS_SEVERITY)
            if severity:
                if isinstance(severity, Mapping):
                    if XML_TEXT in severity:
                        return severity[XML_TEXT]
                else:
                    return severity
        return None

    @property
    def temporary(self) -> Optional[bool]:
        """Return if this entry is temporary."""
        if self._rss_entry:
            temporary = self._rss_entry.get_additional_attribute(
                XML_TAG_GDACS_TEMPORARY
            )
            if temporary:
                return FeedEntry._string2boolean(temporary)
        return None

    @property
    def to_date(self) -> Optional[datetime]:
        """Return the to date of this entry."""
        if self._rss_entry:
            to_date = self._rss_entry.get_additional_attribute(XML_TAG_GDACS_TO_DATE)
            if to_date:
                return dateparser.parse(to_date)
        return None

    @property
    def version(self) -> Optional[int]:
        """Return the version of this entry."""
        if self._rss_entry:
            version = self._rss_entry.get_additional_attribute(XML_TAG_GDACS_VERSION)
            if version:
                return int(version)
        return None

    @property
    def vulnerability(self) -> Optional[Union[str, float]]:
        """Return the vulnerability of this entry."""
        if self._rss_entry:
            vulnerability = self._rss_entry.get_additional_attribute(
                XML_TAG_GDACS_VULNERABILITY
            )
            if vulnerability:
                if isinstance(vulnerability, Mapping):
                    # 1. See if there is a textual value.
                    if XML_TEXT in vulnerability:
                        return vulnerability[XML_TEXT]
                    # 2. See if there is a numerical value.
                    if XML_ATTRIBUTE_VALUE in vulnerability:
                        return float(vulnerability[XML_ATTRIBUTE_VALUE])
                else:
                    return vulnerability
        return None
