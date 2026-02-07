---
title: "MapServer Demo"
description: "Demonstration of MapServer capabilities serving dynamic spatial data from a remote PostGIS database with real-time buffer calculations."
thumbnail: "/img/gallery/mapserver-demo.png"
tags:
  - MapServer
  - PostGIS
  - Dynamic Rendering
date: 2018-01-01
mapUrl: "https://maps.kartoza.com/MapServer%20Demo/"
---

## Overview

This demonstration showcases MapServer's ability to serve dynamic spatial data directly from a PostGIS database. The map features real-time buffer calculations and on-the-fly rendering, demonstrating the power of server-side spatial processing.

## Key Features

- **Dynamic rendering** - Data is rendered on-demand from the database
- **Real-time buffers** - Spatial calculations performed at request time
- **PostGIS integration** - Leveraging PostgreSQL's spatial capabilities
- **Performance** - Efficient handling of complex spatial operations

## Technology Stack

- **MapServer** - High-performance open source map server
- **PostgreSQL/PostGIS** - Enterprise spatial database
- **OpenLayers** - Web mapping client

## Use Cases

This approach is ideal for applications where:
- Data changes frequently and pre-rendering is impractical
- Complex spatial operations are required at display time
- Flexibility in styling and output formats is needed
- Integration with existing PostgreSQL infrastructure is desired
