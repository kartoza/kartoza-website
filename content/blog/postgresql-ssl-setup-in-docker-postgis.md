---
title: "PostgreSQL SSL Setup in Docker-postgis"
description: "Kartoza's Docker-based PostGIS image includes SSL support and demonstrates progressive complexity from automatic to manual certificate management."
tags:
  - PostGIS
  - PostgreSQL
  - Docker
  - SSL
  - Security
date: 2021-05-31
author: "Admire Nyakudya"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="PostgreSQL SSL Setup in Docker-postgis"
    subtitle="PostGIS"
    class="is-primary"
    sub-block-side="bottom"
>}}
Kartoza's Docker-based PostGIS image includes SSL support and demonstrates progressive complexity from automatic to manual certificate management.
{{< /block >}}

## Introduction

The piece addresses database infrastructure approaches, noting that "Databases are the cornerstone of most web applications and also act as a central repository for the storage of data."

## Main Content

Kartoza offers a Docker-based PostGIS image for PostgreSQL deployment. The default configuration includes SSL support via pre-generated certificates, though it doesn't enforce SSL connections by default.

The team introduced an environment variable `FORCE_SSL=TRUE` to mandate encrypted connections, eliminating manual configuration edits to `pg_hba.conf` during redeployment.

## Setup Instructions

### Basic SSL Configuration

```bash
docker run -p 25433:5432 -e FORCE_SSL=TRUE --name ssl -d kartoza/postgis:13-3.1
```

**QGIS Connection Setup** requires configuring SSL Mode to 'Require.'

## Custom Certificate Implementation

The process involves:

1. Creating a bash script generating OpenSSL certificates
2. Running the container with volume mounts
3. Creating an `ssl.conf` configuration file specifying certificate paths
4. Copying the configuration into the running container
5. Restarting the service
6. Extracting root certificates for client-side authentication
7. Configuring QGIS with SSL mode set to 'verify-full'

The detailed walkthrough demonstrates progressive complexity from automatic to manual certificate management.
