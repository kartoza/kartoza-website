---
title: "Docker OSM"
description: "Create a local mirror of OpenStreetMap data for anywhere in the world with automatic updates."
thumbnail: "/img/docker/docker-osm.png"
dockerhub: "https://hub.docker.com/r/kartoza/docker-osm"
github: "https://github.com/kartoza/docker-osm"
pulls: "300K+"
stars: 8
tags:
  - OpenStreetMap
  - Database
  - ETL
upstream:
  name: "OpenStreetMap"
  url: "https://www.openstreetmap.org/"
  description: "OpenStreetMap is a collaborative project to create a free editable map of the world."
date: 2024-01-03
weight: 3
---

## Overview

Docker OSM provides an easy way to set up a local mirror of OpenStreetMap data for any region in the world. It handles downloading, importing, and continuously updating OSM data into a PostGIS database, ready for use with rendering, routing, or analysis applications.

## Features

- **Any region** - Download and import OSM data for any area of the world
- **Automatic updates** - Continuously sync with OSM minutely/hourly/daily diffs
- **PostGIS ready** - Data imported into a fully-featured PostGIS database
- **Imposm3 import** - Fast and flexible import using imposm3
- **Custom schemas** - Define your own mapping for the import
- **Clip to boundary** - Limit data to a specific polygon

## Quick Start

### Basic Usage

```bash
# Clone the repository
git clone https://github.com/kartoza/docker-osm.git
cd docker-osm

# Copy and edit the environment file
cp .env.example .env
# Edit .env to set your region and preferences

# Start the stack
docker-compose up -d
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
      - osm_db_data:/var/lib/postgresql

  imposm:
    image: kartoza/docker-osm:imposm-latest
    environment:
      - POSTGRES_USER=docker
      - POSTGRES_PASS=docker
      - POSTGRES_DBNAME=gis
      - POSTGRES_HOST=db
      - POSTGRES_PORT=5432
      - CLIP=yes
      - QGIS_STYLE=yes
    volumes:
      - osm_import_data:/home/settings
      - osm_cache:/home/cache
    depends_on:
      - db

  osmupdate:
    image: kartoza/docker-osm:osmupdate-latest
    environment:
      - MAX_DAYS=100
      - DIFF=day
    volumes:
      - osm_import_data:/home/settings
    depends_on:
      - imposm

volumes:
  osm_db_data:
  osm_import_data:
  osm_cache:
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `POSTGRES_USER` | Database username | `docker` |
| `POSTGRES_PASS` | Database password | `docker` |
| `POSTGRES_DBNAME` | Database name | `gis` |
| `POSTGRES_HOST` | Database host | `db` |
| `CLIP` | Clip data to boundary | `no` |
| `QGIS_STYLE` | Generate QGIS styling | `yes` |
| `DIFF` | Update frequency (minute/hour/day) | `day` |

## Workflow

1. **Download** - Fetch OSM PBF file for your region
2. **Import** - Load data into PostGIS using imposm3
3. **Update** - Continuously apply diffs to keep data current
4. **Style** - Optional QGIS project with pre-configured styling

## Use Cases

- **Basemap rendering** - Generate tiles for your own basemap
- **Geocoding** - Build address search functionality
- **Routing** - Create a routing database with PgRouting
- **Analysis** - Analyze OSM data for your area of interest
- **Offline maps** - Host OSM data in air-gapped environments

## Upstream Project

This image works with [OpenStreetMap](https://www.openstreetmap.org/) data, the free wiki world map. OSM is a collaborative project to create a free editable geographic database of the world.

We gratefully acknowledge the OpenStreetMap Foundation and the millions of contributors who make this incredible dataset possible.
