---
client: World Bank
date: '2022-08-11'
description: GeoCRIS is a powerful geospatial analysis platform that enables users
  to visualise, analyse, and interpret geographic data, facilitating informed decision-making
  across various fields such as urban pl
erpnext_id: 7b31372bef
erpnext_modified: '2026-06-04 10:26:45.538752'
github: https://github.com/kartoza/geocris-inasafe-fba
reviewedBy: Automated Check
reviewedDate: '2026-06-19'
services: []
tags:
- Project
technologies:
- pyCSW
- Google Sheets
- QGIS
- Mapserver
- MapProxy
- pg_featureserv
- React
- Tegola
thumbnail: https://erp.kartoza.com/files/geocris.png
title: GeoCRIS
---

{{< block
    title="GeoCRIS"
    subtitle="Project"
    class="is-primary"
    sub-block-side="bottom"
>}}
GeoCRIS is a powerful geospatial analysis platform that enables users to visualise, analyse, and interpret geographic data, facilitating informed decision-making across various fields such as urban planning, environmental management, and resource allocation.
{{< /block >}}

## Overview

Kartoza was brought into support a larger team to deliver GeoCRIS, the spatial component of CRIS, the Caribbean Risk Information System of CDEMA (<https://cdema.org/cris/).> We built on the metadata management system (pyCSW and Google sheets), styled vector tile layers in QGIS, built a data validation QGIS plugin amongst other tasks.

  

Accurate, complete metadata and a functional CSW service are critical to the functioning of the system since the web app is driven by metadata. Available data, its description and its map service endpoints are all obtained by performing CSW queries on the metadata service. Using these, the web map dynamically offers the user whatever is available according to the metadatabase.

  

![](/files/Oaznbl6.png)

## Client

World Bank

## Technologies

- pyCSW
- Google Sheets
- QGIS
- Mapserver
- MapProxy
- pg_featureserv
- React
- Tegola

## Source Code

[GitHub](https://github.com/kartoza/geocris-inasafe-fba)
