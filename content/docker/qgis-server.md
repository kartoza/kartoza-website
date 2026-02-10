---
title: "QGIS Server"
description: "Production-ready QGIS Server for publishing maps and OGC services from QGIS projects."
thumbnail: "/img/docker/qgis-server.png"
dockerhub: "https://hub.docker.com/r/kartoza/qgis-server"
github: "https://github.com/kartoza/docker-qgis-server"
pulls: "40K+"
stars: 15
tags:
  - OGC Services
  - WMS
  - WFS
  - QGIS
upstream:
  name: "QGIS Server"
  url: "https://qgis.org/"
  description: "QGIS Server provides OGC compliant map services using the QGIS rendering engine."
date: 2024-01-06
weight: 6
---

## Overview

The Kartoza QGIS Server Docker image provides a production-ready QGIS Server instance for publishing your QGIS projects as OGC web services. It uses the same rendering engine as QGIS Desktop, ensuring your maps look identical when published.

## Features

- **Pixel-perfect maps** - Identical rendering to QGIS Desktop
- **OGC compliant** - WMS, WFS, WCS, and WMTS support
- **QGIS projects** - Publish directly from .qgs/.qgz files
- **Print layouts** - GetPrint for high-quality map outputs
- **GetFeatureInfo** - Interactive querying of features
- **Multiple versions** - Support for QGIS LTR and latest releases

## Quick Start

### Basic Usage

```bash
docker run -d \
  --name qgis-server \
  -v /path/to/projects:/data \
  -e QGIS_PROJECT_FILE=/data/myproject.qgz \
  -p 80:80 \
  kartoza/qgis-server
```

### With PostGIS Database

```bash
docker run -d \
  --name qgis-server \
  -v /path/to/projects:/data \
  -e QGIS_PROJECT_FILE=/data/myproject.qgz \
  -e PGSERVICEFILE=/data/.pg_service.conf \
  -p 80:80 \
  --link postgis:postgis \
  kartoza/qgis-server
```

### Docker Compose

```yaml
version: '3.8'
services:
  db:
    image: kartoza/postgis:16-3.4
    environment:
      - POSTGRES_USER=docker
      - POSTGRES_PASS=docker
      - POSTGRES_DBNAME=gis
    volumes:
      - postgis_data:/var/lib/postgresql

  qgis-server:
    image: kartoza/qgis-server:3.34
    environment:
      - QGIS_PROJECT_FILE=/data/project.qgz
      - QGIS_SERVER_LOG_LEVEL=0
      - QGIS_SERVER_PARALLEL_RENDERING=true
      - QGIS_SERVER_MAX_THREADS=4
    volumes:
      - ./projects:/data:ro
    ports:
      - "80:80"
    depends_on:
      - db

volumes:
  postgis_data:
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `QGIS_PROJECT_FILE` | Path to QGIS project | - |
| `QGIS_SERVER_LOG_LEVEL` | Log level (0=INFO, 1=WARNING, 2=CRITICAL) | `0` |
| `QGIS_SERVER_PARALLEL_RENDERING` | Enable parallel rendering | `true` |
| `QGIS_SERVER_MAX_THREADS` | Maximum render threads | `4` |
| `PGSERVICEFILE` | PostgreSQL service file path | - |
| `QGIS_AUTH_DB_DIR_PATH` | Authentication database path | - |

## OGC Service URLs

Once running, access your services at:

```
# WMS GetCapabilities
http://localhost/qgis?SERVICE=WMS&REQUEST=GetCapabilities

# WMS GetMap
http://localhost/qgis?SERVICE=WMS&REQUEST=GetMap&LAYERS=mylayer&...

# WFS GetCapabilities
http://localhost/qgis?SERVICE=WFS&REQUEST=GetCapabilities

# Print/GetPrint (for print layouts)
http://localhost/qgis?SERVICE=WMS&REQUEST=GetPrint&TEMPLATE=MyLayout&...
```

## Performance Tuning

### Apache/mod_fcgid Configuration

```apache
# Increase for high-traffic sites
FcgidMaxProcesses 10
FcgidMinProcesses 2
FcgidMaxRequestsPerProcess 1000
```

### Project Optimization

1. **Use PostgreSQL** - Database layers are faster than files
2. **Simplify geometries** - Use ST_Simplify for display layers
3. **Create indexes** - Spatial indexes improve query performance
4. **Cache base layers** - Use MapProxy for static base layers

## Available Tags

- `3.34` - QGIS 3.34 LTR (recommended for production)
- `3.36` - QGIS 3.36 latest
- `ltr` - Always points to current LTR
- `latest` - Always points to newest release

## Upstream Project

This image packages [QGIS Server](https://qgis.org/), the server component of QGIS that provides OGC compliant map services.

We gratefully acknowledge the QGIS project and the Open Source Geospatial Foundation (OSGeo) for their excellent work on this foundational open source GIS platform.
