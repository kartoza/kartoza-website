---
title: "Creating a Live, Topic Specific Mirror of OpenStreetMap in PostGIS"
description: "The article provides a walkthrough for establishing a live OSM mirror focused on particular geographic regions and feature types."
tags:
  - Docker
  - OpenStreetMap
  - PostGIS
  - GIS
date: 2019-04-29
author: "Tim Sutton"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="Creating a Live, Topic Specific Mirror of OpenStreetMap in PostGIS"
    subtitle="Docker"
    class="is-primary"
    sub-block-side="bottom"
>}}
The article provides a walkthrough for establishing a live OSM mirror focused on particular geographic regions and feature types.
{{< /block >}}

## Introduction

The article provides a walkthrough for establishing a live OSM mirror focused on particular geographic regions and feature types. Using Angola's building data as an example, the tutorial demonstrates how to continuously update a PostGIS database with new OpenStreetMap contributions, enabling offline analysis capabilities.

## Architecture Overview

An architectural diagram illustrates the system's underlying infrastructure. All code is available in the Kartoza GitHub repository (docker-osm).

## Implementation Steps

1. Identify the country/region PBF file
2. Optionally create a clip.shp file for the area of interest
3. Optionally create a mappings.yml file
4. Modify the sample project with selected options
5. Start the docker-compose project
6. Connect to PostGIS from QGIS
7. Run queries using dbmanager to create views
8. Use QGIS time manager plugin to animate temporal data

## Prerequisites

Users should be familiar with:
- Docker and docker-compose
- GNU make
- YAML file editing
- OSM data fundamentals
- PostGIS usage and QGIS connection protocols
- QGIS and its time manager plugin

## Quickstart: Angola Buildings Example

Download docker-osm-examples, navigate to the angola-buildings folder, and execute `make deploy`. The system initializes the PostGIS database, imports the country PBF file via imposm, and runs osm-enrich to add usernames and timestamps.

## Time Series Visualization

Create a PostgreSQL view filtering for complete OSMENRICH records, then apply QGIS's time manager plugin with monthly intervals. The "Accumulate features" option displays building progression chronologically.

## Credits

Development team: Tim Sutton, Etienne Trimaille, Irwan Fathurrahman, and Yarjuna Rohmat. Initial funding provided by Kartoza; subsequent support from WorldBank/GFDRR and DigitalSquare.
