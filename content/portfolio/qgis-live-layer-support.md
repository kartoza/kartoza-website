---
client: ''
date: '2022-08-11'
description: 'Enhancing QGIS: Introducing Live Layers for Improved Battlefield Simulations'
erpnext_id: c5e6b88ec4
erpnext_modified: '2026-06-04 11:27:48.857869'
github: ''
reviewedBy: Automated Check
reviewedDate: '2026-06-19'
services:
- Development
- Consulting
tags:
- Project
technologies:
- C++
- QGIS
thumbnail: https://erp.kartoza.com/files/qgislivelayersupport_1.png
title: QGIS live layer Support
---

{{< block
    title="QGIS live layer Support"
    subtitle="Project"
    class="is-primary"
    sub-block-side="bottom"
>}}
Enhancing QGIS: Introducing Live Layers for Improved Battlefield Simulations
{{< /block >}}

## Overview

Saab Grintek are using QGIS for battlefield simulations and monitoring, Sensor and position updates streaming in to multiple layers was overwhelming QGIS because it was re-rendering the whole map canvas with each update. Saab Grintek therefore commissioned Kartoza to add the concept of a live layer to core QGIS. A live layer can update independently of the rest of the map. Kartoza in turn subcontracted much of the heavy lifting to our colleague and core QGIS developer, Nyall Dawson. This functionality was released as part of QGIS 3.

![](/files/qgislivelayersupport_1.png)

## Technologies

- C++
- QGIS
