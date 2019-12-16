"""GDACS constants."""

ATTRIBUTION = "Global Disaster Alert and Coordination System"

XML_ATTRIBUTE_VALUE = "@value"
XML_TEXT = "#text"

XML_TAG_DC_SUBJECT = 'dc:subject'
XML_TAG_GDACS_ALERT_LEVEL = 'gdacs:alertlevel'
XML_TAG_GDACS_BBOX = 'gdacs:bbox'
XML_TAG_GDACS_COUNTRY = 'gdacs:country'
XML_TAG_GDACS_DURATION_IN_WEEK = 'gdacs:durationinweek'
XML_TAG_GDACS_EVENT_NAME = 'gdacs:eventname'
XML_TAG_GDACS_EVENT_TYPE = 'gdacs:eventtype'
XML_TAG_GDACS_FROM_DATE = 'gdacs:fromdate'
XML_TAG_GDACS_ICON = 'gdacs:icon'
XML_TAG_GDACS_IS_CURRENT = 'gdacs:iscurrent'
XML_TAG_GDACS_POPULATION = 'gdacs:population'
XML_TAG_GDACS_SEVERITY = 'gdacs:severity'
XML_TAG_GDACS_TEMPORARY = 'gdacs:temporary'
XML_TAG_GDACS_TO_DATE = 'gdacs:todate'
XML_TAG_GDACS_VERSION = 'gdacs:version'
XML_TAG_GDACS_VULNERABILITY = 'gdacs:vulnerability'

EVENT_TYPE_MAP = {
    "FL": "Flood",
    "EQ": "Earthquake",
    "TS": "Tsunami",
    "TC": "Tropical Cyclone",
    "VO": "Volcano",
    "DR": "Drought"
}

URL = "https://www.gdacs.org/xml/rss.xml"
