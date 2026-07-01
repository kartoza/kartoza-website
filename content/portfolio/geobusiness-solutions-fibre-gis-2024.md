---
client: ''
date: '2025-01-17'
description: 'Kartoza was subcontracted by GeoBusiness Solutions in Namibia to create
  a service that would automatically ingest uploaded shapefiles into a Postgres database
  and then serve the resulting vector data '
erpnext_id: 86r8k6q8tl
erpnext_modified: '2026-06-04 14:35:53.248712'
github: https://github.com/kartoza/Paratus
reviewedBy: Automated Check
reviewedDate: '2026-06-19'
services: []
tags:
- Project
technologies:
- QGIS
- Qgis server
- PostgreSQL / PostGIS
- Docker
- Python
thumbnail: https://erp.kartoza.com/files/geobusiness_solutions_cover.png
title: GeoBusiness Solutions Fibre GIS 2024
---

{{< block
    title="GeoBusiness Solutions Fibre GIS 2024"
    subtitle="Project"
    class="is-primary"
    sub-block-side="bottom"
>}}
Kartoza was subcontracted by GeoBusiness Solutions in Namibia to create a service that would automatically ingest uploaded shapefiles into a Postgres database and then serve the resulting vector data on a QGIS Server based API.
{{< /block >}}

## Overview

Kartoza was subcontracted by GeoBusiness Solutions in Namibia to create a service that would automatically ingest uploaded shapefiles into a Postgres database and then serve the resulting vector data on a QGIS Server based API. The service was created in order to allow Paratus Namibia, an internet service provider, to track queries from potential customers.

The python code handles the ingestion and processing of shapefiles to then be stored in a Postgres database. QGIS Server is used to display and edit the data. The setup of QGIS Server was done using a Docker package. API calls are used to make changes to the data stored in the database. The entire system is hosted on the end client's (Paratus) infrastructure.

![](/files/TWNKSZQ.png)

## Technologies

- QGIS
- Qgis server
- PostgreSQL / PostGIS
- Docker
- Python

## Source Code

[GitHub](https://github.com/kartoza/Paratus)
