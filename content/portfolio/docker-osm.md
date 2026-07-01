---
client: ''
date: '2025-01-15'
description: A docker compose project to setup an OSM PostGIS database with automatic
  updates from OSM periodically. The only files you need is a PBF file, geojson (if
  you intend to restrict data download to a sma
erpnext_id: ossu84ni22
erpnext_modified: '2026-06-04 14:29:24.100979'
github: https://github.com/kartoza/docker-osm
reviewedBy: Automated Check
reviewedDate: '2026-06-19'
services: []
tags:
- Project
technologies:
- PostGIS
- docker-osm
thumbnail: https://erp.kartoza.com/files/DockerOSM.png
title: DOCKER-OSM
---

{{< block
    title="DOCKER-OSM"
    subtitle="Project"
    class="is-primary"
    sub-block-side="bottom"
>}}
A docker compose project to setup an OSM PostGIS database with automatic updates from OSM periodically. The only files you need is a PBF file, geojson (if you intend to restrict data download to a smaller extent than the one specified by the PBF) and run the docker compose project.
{{< /block >}}

## Overview

This project lets users maintain their own PostGIS database of a custom subset of OpenStreetMap data and keep it up to date automatically via regular downloads of OSM diff files.

![](/files/BJt2vzp.png)

## Technologies

- PostGIS
- docker-osm

## Source Code

[GitHub](https://github.com/kartoza/docker-osm)
