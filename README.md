# python-aio-georss-gdacs

[![Build Status](https://github.com/exxamalte/python-aio-georss-gdacs/workflows/CI/badge.svg?branch=master)](https://github.com/exxamalte/python-aio-georss-gdacs/actions?workflow=CI)
[![codecov](https://codecov.io/gh/exxamalte/python-aio-georss-gdacs/branch/master/graph/badge.svg?token=JQ8DE4RPIX)](https://codecov.io/gh/exxamalte/python-aio-georss-gdacs)
[![PyPi](https://img.shields.io/pypi/v/aio-georss-gdacs.svg)](https://pypi.python.org/pypi/aio-georss-gdacs)
[![Version](https://img.shields.io/pypi/pyversions/aio-georss-gdacs.svg)](https://pypi.python.org/pypi/aio-georss-gdacs)

This library provides convenient async access to the [Global Disaster Alert and Coordination System (GDACS)](https://www.gdacs.org/) feeds.
 
## Installation
`pip install aio-georss-gdacs`

## Usage
See below for examples of how this library can be used. After instantiating a 
particular class - feed or feed manager - and supply the required parameters, 
you can call `update` to retrieve the feed data. The return value 
will be a tuple of a status code and the actual data in the form of a list of 
feed entries specific to the selected feed.

Status Codes
* _OK_: Update went fine and data was retrieved. The library may still 
  return empty data, for example because no entries fulfilled the filter 
  criteria.
* _OK_NO_DATA_: Update went fine but no data was retrieved, for example 
  because the server indicated that there was not update since the last request.
* _ERROR_: Something went wrong during the update

**Parameters**

| Parameter          | Description                               |
|--------------------|-------------------------------------------|
| `home_coordinates` | Coordinates (tuple of latitude/longitude) |

**Supported Filters**

| Filter     |                     | Description |
|------------|---------------------|-------------|
| Radius     | `filter_radius`     | Radius in kilometers around the home coordinates in which events from feed are included. |
| Categories | `filter_categories` | Array of category names. Only events with a category matching any of these is included. Supported/known categories are "Drought", "Earthquake", "Flood", "Tropical Cyclone", "Tsunami", "Volcano" |

**Example**
```python
import asyncio
from aiohttp import ClientSession
from aio_georss_gdacs import GdacsFeed
async def main() -> None:
    async with ClientSession() as websession:    
        # Home Coordinates: Latitude: -33.0, Longitude: 150.0
        # Filter radius: 500 km
        feed = GdacsFeed(websession, 
                         (-33.0, 150.0), 
                         filter_radius=500)
        status, entries = await feed.update()
        print(status)
        print(entries)
asyncio.get_event_loop().run_until_complete(main())
```

## Feed entry properties
Each feed entry is populated with the following properties:

| Name             | Description                                                                                   | Feed attribute                |
|------------------|-----------------------------------------------------------------------------------------------|-------------------------------|
| geometries       | All geometry details of this entry (except bounding boxes).                                   | `georss:point`                |
| coordinates      | Best coordinates (latitude, longitude) of this entry.                                         | `georss:point`                |
| external_id      | The unique public identifier for this incident.                                               | `guid`                        |
| title            | Title of this entry.                                                                          | `title`                       |
| attribution      | Attribution of the feed.                                                                      | n/a                           |
| distance_to_home | Distance in km of this entry to the home coordinates.                                         | n/a                           |
| category         | The alert level of the incident.                                                              | `gdacs:alertlevel`            |
| description      | The description of the incident.                                                              | `description`                 |
| alert_level      | Alert level ("Red", "Orange", "Green").                                                       | `gdacs:alertlevel`            |
| country          | Country where incident happened.                                                              | `gdacs:country`               |
| duration_in_week | Duration of the incident in full weeks.                                                       | `gdacs:durationinweek`        |
| event_id         | Event ID (numerical).                                                                         | `gdacs:eventid`               |
| event_name       | Short event name.                                                                             | `gdacs:eventname`             |
| event_type_short | Short event type ("DR, "EQ", "FL", "TC", "TS", "VO").                                         | `gdacs:eventtype`             |
| event_type       | Long event type ("Drought", "Earthquake", "Flood", "Tropical Cyclone", "Tsunami", "Volcano"). | `gdacs:eventtype`             |
| from_date        | Date and time this incident started.                                                          | `gdacs:fromdate`              |
| icon_url         | Icon URL.                                                                                     | `gdacs:icon`                  |
| is_current       | Whether this incident is current.                                                             | `gdacs:iscurrent`             |
| population       | Exposed population.                                                                           | `gdacs:population`            |
| severity         | Severity of the incident.                                                                     | `gdacs:severity`              |
| temporary        | Whether this incident is temporary.                                                           | `gdacs:temporary`             |
| to_date          | Date and time this incident ended.                                                            | `gdacs:todate`                |
| version          | Version of the incident in this feed.                                                         | `gdacs:version`               |
| vulnerability    | Vulnerability score (textual or numerical).                                                   | `gdacs:vulnerability`         |


## Feed Manager

The Feed Manager helps managing feed updates over time, by notifying the 
consumer of the feed about new feed entries, updates and removed entries 
compared to the last feed update.

* If the current feed update is the first one, then all feed entries will be 
  reported as new. The feed manager will keep track of all feed entries' 
  external IDs that it has successfully processed.
* If the current feed update is not the first one, then the feed manager will 
  produce three sets:
  * Feed entries that were not in the previous feed update but are in the 
    current feed update will be reported as new.
  * Feed entries that were in the previous feed update and are still in the 
    current feed update will be reported as to be updated.
  * Feed entries that were in the previous feed update but are not in the 
    current feed update will be reported to be removed.
* If the current update fails, then all feed entries processed in the previous
  feed update will be reported to be removed.

After a successful update from the feed, the feed manager provides two
different dates:

* `last_update` will be the timestamp of the last update from the feed 
  irrespective of whether it was successful or not.
* `last_update_successful` will be the timestamp of the last successful update 
  from the feed. This date may be useful if the consumer of this library wants 
  to treat intermittent errors from feed updates differently.
* `last_timestamp` (optional, depends on the feed data) will be the latest 
  timestamp extracted from the feed data. 
  This requires that the underlying feed data actually contains a suitable 
  date. This date may be useful if the consumer of this library wants to 
  process feed entries differently if they haven't actually been updated.
