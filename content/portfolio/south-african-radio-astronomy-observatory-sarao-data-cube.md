---
client: ''
date: '2025-01-20'
description: Kartoza served as the technical lead for the Digital Earth South Africa
  Data Cube, implementing a national-scale Earth observation platform for SARAO and
  SANSA. The project delivered a fully operation
erpnext_id: m63641a6jb
erpnext_modified: '2026-06-04 14:40:56.818061'
github: ''
reviewedBy: Automated Check
reviewedDate: '2026-06-19'
services:
- System Configuration
- Algorithm Development
- Training Support
tags:
- Project
technologies:
- OpenDataCube
- Jupyter Notebook
- Python
- PostgreSQL / PostGIS
thumbnail: https://erp.kartoza.com/files/SARAO2.png
title: South African Radio Astronomy Observatory (SARAO) Data Cube
---

{{< block
    title="South African Radio Astronomy Observatory (SARAO) Data Cube"
    subtitle="Project"
    class="is-primary"
    sub-block-side="bottom"
>}}
Kartoza served as the technical lead for the Digital Earth South Africa Data Cube, implementing a national-scale Earth observation platform for SARAO and SANSA. The project delivered a fully operational Open Data Cube environment with data ingest, analysis tools, and scientific workflows to support advanced satellite data analysis.
{{< /block >}}

## Overview

Kartoza was appointed as the Technical Lead Resource for the Digital Earth South Africa (DESA) Data Cube project, a joint initiative between the South African Radio Astronomy Observatory (SARAO) and the South African National Space Agency (SANSA). The project aimed to establish a fully functional national-scale Earth observation data platform capable of ingesting, processing, analysing, and sharing large volumes of satellite imagery using high-performance computing infrastructure.

  

Kartoza led the design and implementation of the DESA Open Data Cube (ODC) environment on SANSA’s infrastructure. This included configuring the core ODC system, a PostgreSQL metadata database, and associated services such as datacube-explorer for data inspection and datacube-ows for serving products via OGC standards. A multi-tenant JupyterHub platform was also deployed, enabling scientists and analysts to interact with the data cube using notebooks for advanced analysis and application development.

  

As part of data preparation and management, Kartoza indexed early SPOT Analysis Ready Data (ARD) into the system and implemented the recommended EO3 metadata standard to ensure long-term compatibility and best practice alignment. A significant technical contribution was the implementation of the Crop Arable Land Fraction (CALF) algorithm in Python, developed from scratch based on theoretical documentation after the original C++ source code was found to be unavailable. This algorithm was fully integrated into the DESA analysis environment.

  

To support adoption and sustainability, Kartoza delivered extensive documentation and training materials, including customised sample notebooks adapted from Digital Earth Africa workflows and a detailed installation and operations guide. This work transformed DESA from a conceptual initiative into an operational scientific data platform, laying the foundation for long-term Earth observation analysis and decision support in South Africa.

  

  

![](/files/Hb6tHfQ.png)

## Technologies

- OpenDataCube
- Jupyter Notebook
- Python
- PostgreSQL / PostGIS
