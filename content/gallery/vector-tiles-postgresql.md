---
title: "Vector Tiles from PostgreSQL"
description: "High-performance vector tile rendering from PostgreSQL using Martin, styled with OpenLayers V6 and integrated with Docker OSM for live data."
thumbnail: "/img/gallery/vector-tiles.png"
tags:
  - Vector Tiles
  - PostgreSQL
  - Martin
  - OpenLayers
date: 2020-01-01
mapUrl: "https://maps.kartoza.com/MartinDemo/"
---

## Overview

This demonstration showcases modern vector tile rendering directly from a PostgreSQL database using Martin, a high-performance PostGIS vector tile server. The map leverages OpenLayers V6 for client-side styling and rendering, providing smooth, interactive performance.

## Technology Stack

- **Martin** - A blazing-fast PostGIS vector tile server written in Rust
- **PostgreSQL/PostGIS** - Enterprise-grade spatial database
- **OpenLayers V6** - Feature-rich web mapping library
- **Docker OSM** - Automated OpenStreetMap data integration

## Key Features

This approach enables dynamic vector tile generation without pre-rendering, allowing for real-time data updates and flexible styling. The combination of Martin and PostGIS delivers excellent performance even with large datasets.

## Use Cases

Vector tiles from PostgreSQL are ideal for:
- Real-time data visualisation
- Applications requiring frequent data updates
- Custom styling without tile regeneration
- Reducing storage requirements compared to raster tiles
