---
title: "PG Backup"
description: "Automated PostgreSQL backup container with local and remote storage support."
thumbnail: "/img/docker/pg-backup.png"
dockerhub: "https://hub.docker.com/r/kartoza/pg-backup"
github: "https://github.com/kartoza/docker-pg-backup"
pulls: "262K+"
stars: 7
tags:
  - Backup
  - PostgreSQL
  - Database
upstream:
  name: "PostgreSQL"
  url: "https://www.postgresql.org/"
  description: "PostgreSQL is a powerful, open source object-relational database system."
date: 2024-01-05
weight: 5
---

## Overview

The Kartoza PG Backup container provides automated PostgreSQL database backups with support for local and remote storage. It's designed to work seamlessly with our PostGIS container but supports any PostgreSQL database.

## Features

- **Scheduled backups** - Cron-based backup scheduling
- **Multiple databases** - Backup one or all databases
- **Compression** - Gzip compression for storage efficiency
- **Retention policy** - Automatic cleanup of old backups
- **Remote storage** - Support for SFTP and S3 backends
- **Restore support** - Easy restore from backup files

## Quick Start

### Basic Usage

```bash
docker run -d \
  --name pg-backup \
  --link postgis:db \
  -e POSTGRES_HOST=db \
  -e POSTGRES_USER=docker \
  -e POSTGRES_PASS=docker \
  -e POSTGRES_PORT=5432 \
  -v pg_backups:/backups \
  kartoza/pg-backup
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

  backup:
    image: kartoza/pg-backup
    environment:
      - POSTGRES_HOST=db
      - POSTGRES_USER=docker
      - POSTGRES_PASS=docker
      - POSTGRES_PORT=5432
      - DUMPPREFIX=PG_db
      - CRON_SCHEDULE=0 3 * * *
      - REMOVE_BEFORE=7
    volumes:
      - pg_backups:/backups
    depends_on:
      - db

volumes:
  postgis_data:
  pg_backups:
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `POSTGRES_HOST` | Database host | `db` |
| `POSTGRES_USER` | Database user | `docker` |
| `POSTGRES_PASS` | Database password | `docker` |
| `POSTGRES_PORT` | Database port | `5432` |
| `POSTGRES_DBNAME` | Database to backup (blank for all) | - |
| `CRON_SCHEDULE` | Backup schedule (cron format) | `0 0 * * *` |
| `REMOVE_BEFORE` | Days to keep backups | `7` |
| `DUMPPREFIX` | Backup filename prefix | `PG` |
| `STORAGE_BACKEND` | Storage type (FILE/S3/SFTP) | `FILE` |

## Backup Schedule Examples

```bash
# Daily at midnight
CRON_SCHEDULE="0 0 * * *"

# Every 6 hours
CRON_SCHEDULE="0 */6 * * *"

# Weekly on Sunday at 2am
CRON_SCHEDULE="0 2 * * 0"

# Monthly on the 1st at 3am
CRON_SCHEDULE="0 3 1 * *"
```

## Remote Storage

### S3 Backend

```yaml
environment:
  - STORAGE_BACKEND=S3
  - AWS_ACCESS_KEY_ID=your_key
  - AWS_SECRET_ACCESS_KEY=your_secret
  - AWS_DEFAULT_REGION=us-east-1
  - AWS_BUCKET_NAME=my-backups
```

### SFTP Backend

```yaml
environment:
  - STORAGE_BACKEND=SFTP
  - SFTP_HOST=backup.example.com
  - SFTP_USER=backup
  - SFTP_PASSWORD=secret
  - SFTP_DIR=/backups
```

## Manual Backup & Restore

### Create Manual Backup

```bash
docker exec pg-backup /backup.sh
```

### Restore from Backup

```bash
# List available backups
docker exec pg-backup ls /backups

# Restore specific backup
docker exec -i postgis pg_restore \
  -U docker -d gis \
  < /path/to/backup.dmp
```

## Upstream Project

This image uses [pg_dump](https://www.postgresql.org/docs/current/app-pgdump.html) from the PostgreSQL project for creating database backups.

We gratefully acknowledge the PostgreSQL Global Development Group for their excellent database system.
