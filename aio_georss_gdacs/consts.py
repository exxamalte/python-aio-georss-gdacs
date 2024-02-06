"""GDACS constants."""
from typing import Final

ATTRIBUTION: Final = "Global Disaster Alert and Coordination System"

XML_ATTRIBUTE_VALUE: Final = "@value"
XML_TEXT: Final = "#text"

XML_TAG_DC_SUBJECT: Final = "dc:subject"
XML_TAG_GDACS_ALERT_LEVEL: Final = "gdacs:alertlevel"
XML_TAG_GDACS_COUNTRY: Final = "gdacs:country"
XML_TAG_GDACS_DURATION_IN_WEEK: Final = "gdacs:durationinweek"
XML_TAG_GDACS_EVENT_ID: Final = "gdacs:eventid"
XML_TAG_GDACS_EVENT_NAME: Final = "gdacs:eventname"
XML_TAG_GDACS_EVENT_TYPE: Final = "gdacs:eventtype"
XML_TAG_GDACS_FROM_DATE: Final = "gdacs:fromdate"
XML_TAG_GDACS_ICON: Final = "gdacs:icon"
XML_TAG_GDACS_IS_CURRENT: Final = "gdacs:iscurrent"
XML_TAG_GDACS_POPULATION: Final = "gdacs:population"
XML_TAG_GDACS_SEVERITY: Final = "gdacs:severity"
XML_TAG_GDACS_TEMPORARY: Final = "gdacs:temporary"
XML_TAG_GDACS_TO_DATE: Final = "gdacs:todate"
XML_TAG_GDACS_VERSION: Final = "gdacs:version"
XML_TAG_GDACS_VULNERABILITY: Final = "gdacs:vulnerability"

EVENT_TYPE_MAP: Final = {
    "DR": "Drought",
    "EQ": "Earthquake",
    "FL": "Flood",
    "TC": "Tropical Cyclone",
    "TS": "Tsunami",
    "VO": "Volcano",
    "WF": "Wild Fire",
}

URL: Final = "https://www.gdacs.org/xml/rss.xml"
