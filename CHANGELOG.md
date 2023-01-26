# Changes

## 0.8 (26/01/2023)
* Added Python 3.11 support.
* Removed deprecated asynctest dependency.
* Bumped aio_georss_client to v0.11.
* Bumped library versions: black, dateparser.

## 0.7 (09/04/2022)
* Bump aio_georss_client to v0.10.
  This includes better error handling if the GDACS service returns invalid XML (which happens occasionally).
* Properly handle event type Wild Fire (WF).

## 0.6 (20/02/2022)
* No functional changes.
* Added Python 3.10 support.
* Removed Python 3.6 support.
* Bumped version of upstream GeoRSS library.
* Bumped library versions: black, flake8, isort.
* Migrated to github actions.

## 0.5 (07/06/2021)
* Add license tag (thanks @fabaff).
* Bump aio_georss_client to v0.7.
* Added Python 3.9 support.
* General code improvements.

## 0.4 (04/11/2020)
* Ignore bounding box geometry definition from feed when calculating distance
  and event's coordinates.

## 0.3 (21/01/2020)
* Extract event id from feed.

## 0.2 (21/01/2020)
* Improve extracting vulnerability information.
* Bump version of upstream library.
* Clear last timestamp when update fails.
* Swap long event type and abbreviated event type.

## 0.1 (07/01/2020)
* Initial release.
* Support for wide range of attributes from default GDACS GeoRSS feed.
