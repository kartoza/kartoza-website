---
title: "Playing with Foreign Data Wrappers in PostgreSQL"
description: "The author explored PostgreSQL's foreign data wrapper (FDW) capability to access MySQL table data."
tags:
  - Database
  - PostgreSQL
  - MySQL
date: 2014-08-16
author: "Gavin Fleming"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="Playing with Foreign Data Wrappers in PostgreSQL"
    subtitle="Database"
    class="is-primary"
    sub-block-side="bottom"
>}}
The author explored PostgreSQL's foreign data wrapper (FDW) capability to access MySQL table data.
{{< /block >}}

## Introduction

The author explored PostgreSQL's foreign data wrapper (FDW) capability to access MySQL table data. The primary motivation was leveraging PostgreSQL's superior and more current functions compared to MySQL, while needing MySQL data for views, lookups, and data-driven styling in Geoserver layers. "FDWs allow remote access to tables or queries from various external third-party databases or file structures."

## Implementation Workflow (Ubuntu 14.04)

### Installation of Dependencies

```bash
sudo apt-get install libpq-dev postgresql-server-dev-9.3
sudo apt-get install libmysqlclient-dev
```

### Clone and Build

```bash
git clone git@github.com:EnterpriseDB/mysql_fdw.git
cd mysql_fdw
export PATH=/usr/lib/postgresql/9.3/bin/:/usr/bin/mysql:$PATH
make USE_PGXS=1
sudo PATH=/usr/lib/postgresql/9.3/bin/:/usr/bin/mysql:$PATH make USE_PGXS=1 install
```

### Database Setup

```bash
createdb mysql_fdw
psql -c 'CREATE EXTENSION postgis;' mysql_fdw
```

```sql
CREATE EXTENSION mysql_fdw;
```

### Create Foreign Server

```sql
CREATE SERVER mysql_svr
FOREIGN DATA WRAPPER mysql_fdw
OPTIONS (address '127.0.0.1', port '3306');
```

### Define Foreign Table

```sql
CREATE FOREIGN TABLE local_cadastre (
sg21 character varying (255),
province character varying (255),
munname character varying (255)
)
SERVER mysql_svr
OPTIONS (query 'SELECT sg21,province munmane from test.cadastre limit 500;');
```

### User Mapping

```sql
CREATE USER MAPPING FOR PUBLIC
SERVER mysql_svr
OPTIONS (username 'user', password 'password123');
```

## Key Benefits

The author notes that FDWs enable dynamic data fetching from remote MySQL tables within PostgreSQL. For static data, creating a local copy allows application of PostgreSQL-specific functions. This approach supports legacy database environments where data remains external while leveraging modern PostgreSQL capabilities.
