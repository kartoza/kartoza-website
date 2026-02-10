---
title: "PostGIS"
description: "Production-ready PostGIS database with automatic clustering, replication, and backup support."
thumbnail: "/img/docker/postgis.png"
dockerhub: "https://hub.docker.com/r/kartoza/postgis"
github: "https://github.com/kartoza/docker-postgis"
pulls: "21M+"
stars: 198
tags:
  - Database
  - PostGIS
  - PostgreSQL
upstream:
  name: "PostGIS"
  url: "https://postgis.net/"
  description: "PostGIS is a spatial database extender for PostgreSQL object-relational database."
date: 2024-01-01
weight: 1
---

## Overview

The Kartoza PostGIS Docker image provides a production-ready PostgreSQL database with the PostGIS spatial extension pre-installed and configured. It's the most popular geospatial database container on Docker Hub with over 21 million pulls.

## Features

- **Multiple PostgreSQL versions** - Support for PostgreSQL 12, 13, 14, 15, and 16
- **PostGIS extensions** - Includes PostGIS, PgRouting, and other spatial extensions
- **Replication support** - Built-in master/slave replication configuration
- **Automatic backups** - Integration with pg-backup container
- **SSL/TLS support** - Secure database connections out of the box
- **Health checks** - Built-in health check endpoints

## Quick Start

### Basic Usage

```bash
docker run -d \
  --name postgis \
  -e POSTGRES_USER=docker \
  -e POSTGRES_PASS=docker \
  -e POSTGRES_DBNAME=gis \
  -p 5432:5432 \
  kartoza/postgis:16-3.4
```

### With Persistent Storage

```bash
docker run -d \
  --name postgis \
  -e POSTGRES_USER=docker \
  -e POSTGRES_PASS=docker \
  -e POSTGRES_DBNAME=gis \
  -v postgis_data:/var/lib/postgresql \
  -p 5432:5432 \
  kartoza/postgis:16-3.4
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
      - ALLOW_IP_RANGE=0.0.0.0/0
    volumes:
      - postgis_data:/var/lib/postgresql
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U docker"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgis_data:
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `POSTGRES_USER` | Database superuser name | `docker` |
| `POSTGRES_PASS` | Database superuser password | `docker` |
| `POSTGRES_DBNAME` | Default database name | `gis` |
| `ALLOW_IP_RANGE` | IP range for connections | `0.0.0.0/0` |
| `POSTGRES_MULTIPLE_EXTENSIONS` | Additional extensions to install | - |
| `REPLICATION` | Enable replication | `false` |

## Available Tags

- `16-3.4` - PostgreSQL 16 with PostGIS 3.4 (recommended)
- `15-3.4` - PostgreSQL 15 with PostGIS 3.4
- `14-3.4` - PostgreSQL 14 with PostGIS 3.4
- `13-3.4` - PostgreSQL 13 with PostGIS 3.4

## Upstream Project

This image packages [PostGIS](https://postgis.net/), the spatial database extender for PostgreSQL. PostGIS adds support for geographic objects allowing location queries to be run in SQL.

We gratefully acknowledge the PostGIS project and the PostgreSQL Global Development Group for their excellent work on these foundational open source projects.
