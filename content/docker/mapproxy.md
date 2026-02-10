---
title: "MapProxy"
description: "Tile caching and proxying server for accelerating map services and creating tile caches."
thumbnail: "/img/docker/mapproxy.png"
dockerhub: "https://hub.docker.com/r/kartoza/mapproxy"
github: "https://github.com/kartoza/docker-mapproxy"
pulls: "292K+"
stars: 12
tags:
  - Caching
  - Tiles
  - WMS
upstream:
  name: "MapProxy"
  url: "https://mapproxy.org/"
  description: "MapProxy is an open source proxy for geospatial data. It caches, accelerates and transforms data from existing map services."
date: 2024-01-04
weight: 4
---

## Overview

The Kartoza MapProxy Docker image provides a ready-to-use tile caching and proxying server. MapProxy accelerates existing map services by caching tiles, and can serve those tiles via TMS, WMTS, or WMS interfaces.

## Features

- **Tile caching** - Cache tiles from WMS, TMS, or other sources
- **Multiple backends** - Support for filesystem, SQLite, S3, and more
- **Reprojection** - On-the-fly coordinate system transformation
- **Seeding** - Pre-generate tile caches for offline use
- **Compositing** - Merge multiple sources into single layers
- **Authentication** - Support for secured upstream services

## Quick Start

### Basic Usage

```bash
docker run -d \
  --name mapproxy \
  -v mapproxy_config:/mapproxy \
  -p 8080:8080 \
  kartoza/mapproxy
```

### With Custom Configuration

```bash
docker run -d \
  --name mapproxy \
  -v /path/to/mapproxy.yaml:/mapproxy/mapproxy.yaml \
  -v mapproxy_cache:/mapproxy/cache_data \
  -p 8080:8080 \
  kartoza/mapproxy
```

### Docker Compose

```yaml
version: '3.8'
services:
  mapproxy:
    image: kartoza/mapproxy
    environment:
      - PRODUCTION=true
      - RECREATE_CONFIG=false
    volumes:
      - ./mapproxy.yaml:/mapproxy/mapproxy.yaml
      - mapproxy_cache:/mapproxy/cache_data
    ports:
      - "8080:8080"

volumes:
  mapproxy_cache:
```

## Configuration Example

```yaml
# mapproxy.yaml
services:
  demo:
  tms:
    use_grid_names: true
  wms:
    md:
      title: MapProxy WMS
      abstract: Cached map services

layers:
  - name: osm
    title: OpenStreetMap
    sources: [osm_cache]

caches:
  osm_cache:
    grids: [webmercator]
    sources: [osm_source]
    cache:
      type: file
      directory_layout: tms

sources:
  osm_source:
    type: tile
    url: https://tile.openstreetmap.org/%(tms_path)s.png
    grid: webmercator

grids:
  webmercator:
    base: GLOBAL_WEBMERCATOR
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PRODUCTION` | Run in production mode | `false` |
| `RECREATE_CONFIG` | Regenerate config on startup | `true` |
| `PROCESSES` | Number of worker processes | `4` |
| `THREADS` | Threads per process | `8` |

## Seeding Tiles

Pre-generate tiles for offline use:

```bash
docker exec mapproxy mapproxy-seed \
  -f /mapproxy/mapproxy.yaml \
  -s /mapproxy/seed.yaml
```

## Use Cases

- **Accelerate WMS** - Cache slow WMS responses as tiles
- **Offline maps** - Pre-seed caches for disconnected environments
- **Tile format conversion** - Serve MVT from WMS sources
- **Load balancing** - Distribute requests across multiple sources
- **Protocol conversion** - Expose TMS as WMTS or vice versa

## Upstream Project

This image packages [MapProxy](https://mapproxy.org/), the open source proxy for geospatial data created by Omniscale.

We gratefully acknowledge the MapProxy developers for this excellent tile caching solution.
