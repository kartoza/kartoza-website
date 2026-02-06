---
title: "Vector Tiles Rendering from PostgreSQL"
description: "Renders vector tiles from a PostgreSQL database using Martin with OpenLayers V6 styling and Docker OSM integration."
thumbnail: "/img/gallery/vector-tiles.png"
tags:
  - Vector Tiles
  - PostgreSQL
  - Martin
  - OpenLayers
date: 2020-01-01
mapUrl: "https://maps.kartoza.com/MartinDemo/"
---

{{< block
    title="Vector Tiles from PostgreSQL"
    subtitle="High-performance vector tile rendering with Martin and OpenLayers"
    class="is-primary"
    sub-block-side="bottom"
    link="https://maps.kartoza.com/MartinDemo/"
    link-text="View Live Map"
>}}
Demonstrating vector tile rendering from a PostgreSQL database using Martin, styled with OpenLayers V6.
{{< /block >}}

## Overview

This demo renders vector tiles from a PostgreSQL database using [Martin](https://github.com/maplibre/martin), a PostGIS vector tile server. The map uses OpenLayers V6 for styling and rendering, with data sourced via Docker OSM integration for up-to-date OpenStreetMap data.

![Vector Tiles Demo](/img/gallery/vector-tiles.png)

## Technology

- **Martin** - PostGIS vector tile server
- **PostgreSQL/PostGIS** - Spatial database
- **OpenLayers V6** - Web mapping library
- **Docker OSM** - OpenStreetMap data integration

## Links

- [View Live Map](https://maps.kartoza.com/MartinDemo/)
