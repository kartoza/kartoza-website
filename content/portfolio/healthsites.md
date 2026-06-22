---
client: ''
date: '2022-08-02'
description: Kartoza, in collaboration with Mark Herringer, developed a free, curated,
  and canonical source of healthcare location data.
erpnext_id: b28b202dfc
erpnext_modified: '2025-01-08 12:42:55.473589'
github: https://github.com/healthsites/healthsites
reviewedBy: Automated Check
reviewedDate: '2026-06-19'
services: []
tags:
- Project
technologies:
- GeoDjango
- PostGIS
thumbnail: https://erp.kartoza.com/files/hs.io.png
title: Healthsites
---

{{< block
    title="Healthsites"
    subtitle="Project"
    class="is-primary"
    sub-block-side="bottom"
>}}
Kartoza, in collaboration with Mark Herringer, developed a free, curated, and canonical source of healthcare location data.
{{< /block >}}

## Overview

Kartoza developed this application in collaboration with Mark Herringer to facilitate the capture and management of a global health facility dataset. Healthsites.io, in partnership with the International Committee of the Red Cross and Médecins Sans Frontières, publishes healthcare location data that demands the highest standards of quality and accuracy.

Kartoza leveraged various innovative technologies, including docker-osm, which creates a concurrent mirror of OpenStreetMap.org tailored to specific features and attributes. As data is captured on Healthsites.io, it is immediately submitted to OpenStreetMap via their API and subsequently mirrored into a local PostgreSQL database.

![](/files/7zshHDu.png)

## Technologies

- GeoDjango
- PostGIS

## Source Code

[GitHub](https://github.com/healthsites/healthsites)
