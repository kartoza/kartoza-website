---
title: "GeoServer"
description: "Feature-rich GeoServer container with clustering support, GeoFence, and multiple extensions."
thumbnail: "/img/docker/geoserver.png"
dockerhub: "https://hub.docker.com/r/kartoza/geoserver"
github: "https://github.com/kartoza/docker-geoserver"
pulls: "5.6M+"
stars: 167
tags:
  - OGC Services
  - WMS
  - WFS
  - GeoServer
upstream:
  name: "GeoServer"
  url: "https://geoserver.org/"
  description: "GeoServer is an open source server for sharing geospatial data."
date: 2024-01-02
weight: 2
---

## Overview

The Kartoza GeoServer Docker image provides a production-ready GeoServer instance with clustering support, GeoFence security, and numerous pre-installed extensions. With over 5.6 million pulls, it's the go-to container for serving geospatial data via OGC standards.

## Features

- **Clustering support** - Run multiple GeoServer instances with shared configuration
- **GeoFence integration** - Advanced security and access control
- **Multiple extensions** - CSS styling, vector tiles, GDAL, and more
- **S3 storage** - Native support for cloud storage backends
- **CORS enabled** - Cross-origin requests configured out of the box
- **Automatic restart** - Watchdog for stable operation

## Quick Start

### Basic Usage

```bash
docker run -d \
  --name geoserver \
  -e GEOSERVER_ADMIN_PASSWORD=myawesomegeoserver \
  -p 8080:8080 \
  kartoza/geoserver:2.24.2
```

### With PostGIS Database

```bash
docker run -d \
  --name geoserver \
  -e GEOSERVER_ADMIN_PASSWORD=myawesomegeoserver \
  -e GEOSERVER_DATA_DIR=/opt/geoserver/data_dir \
  -v geoserver_data:/opt/geoserver/data_dir \
  -p 8080:8080 \
  --link postgis:postgis \
  kartoza/geoserver:2.24.2
```

### Docker Compose

```yaml
version: '3.8'
services:
  db:
    image: kartoza/postgis:16-3.4
    environment:
      - POSTGRES_USER=geoserver
      - POSTGRES_PASS=geoserver
      - POSTGRES_DBNAME=gis
    volumes:
      - postgis_data:/var/lib/postgresql

  geoserver:
    image: kartoza/geoserver:2.24.2
    environment:
      - GEOSERVER_ADMIN_USER=admin
      - GEOSERVER_ADMIN_PASSWORD=myawesomegeoserver
      - GEOSERVER_DATA_DIR=/opt/geoserver/data_dir
      - STABLE_EXTENSIONS=css-plugin,ysld-plugin,vectortiles-plugin
      - COMMUNITY_EXTENSIONS=ogcapi-plugin
    volumes:
      - geoserver_data:/opt/geoserver/data_dir
    ports:
      - "8080:8080"
    depends_on:
      - db

volumes:
  postgis_data:
  geoserver_data:
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GEOSERVER_ADMIN_USER` | Admin username | `admin` |
| `GEOSERVER_ADMIN_PASSWORD` | Admin password | `geoserver` |
| `GEOSERVER_DATA_DIR` | Data directory path | `/opt/geoserver/data_dir` |
| `STABLE_EXTENSIONS` | Comma-separated stable extensions | - |
| `COMMUNITY_EXTENSIONS` | Comma-separated community extensions | - |
| `CORS_ENABLED` | Enable CORS | `true` |
| `CLUSTERING` | Enable clustering | `false` |

## Available Extensions

### Stable Extensions
- `css-plugin` - CSS styling
- `ysld-plugin` - YSLD styling
- `vectortiles-plugin` - Vector tiles (MVT, GeoJSON, TopoJSON)
- `gdal-plugin` - GDAL raster formats
- `libjpeg-turbo-plugin` - Faster JPEG encoding
- `monitor-plugin` - Request monitoring

### Community Extensions
- `ogcapi-plugin` - OGC API Features/Tiles
- `s3-geotiff-plugin` - Cloud Optimized GeoTIFFs from S3

## Available Tags

- `2.24.2` - Latest stable (recommended)
- `2.23.4` - Previous stable
- `2.24.2-v2024.1.0` - Version pinned releases

## Upstream Project

This image packages [GeoServer](https://geoserver.org/), the open source server for sharing geospatial data. GeoServer implements OGC standards including WMS, WFS, WCS, and WPS.

We gratefully acknowledge the GeoServer project and the Open Source Geospatial Foundation (OSGeo) for their excellent work on this foundational open source project.
