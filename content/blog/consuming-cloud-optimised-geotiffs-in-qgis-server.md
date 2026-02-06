---
title: "Consuming Cloud Optimised GeoTIFFs in QGIS Server"
description: "QGIS has been able to consume cloud optimised GeoTIFF (COG)s since v3.2, through the data source manager."
tags:
  - QGIS
  - Cloud
  - GeoTIFF
date: 2020-05-04
author: "Admire Nyakudya"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="Consuming Cloud Optimised GeoTIFFs in QGIS Server"
    subtitle="QGIS"
    class="is-primary"
    sub-block-side="bottom"
>}}
QGIS has been able to consume cloud optimised GeoTIFF (COG)s since v3.2, through the data source manager.
{{< /block >}}

## Introduction

"QGIS has been able to consume cloud optimised GeoTIFF (COG)s since v3.2, through the data source manager." The piece does not explain what COGs are, directing readers to other resources for that context.

## Overview

The article addresses cloud-based storage adoption through platforms like S3 and Google Cloud Storage. Traditional GIS formats struggle with efficient web map tile serving and on-the-fly data processing in cloud environments, typically requiring full downloads or format conversion before use.

The author outlines a process for "publishing a QGIS project with COG (in local storage) using QGIS Server," with plans to discuss COG processing via QGIS Server algorithms in future articles.

## Technical Implementation

### Docker Configuration

The setup uses a docker-compose file with two main services:
- **Transfer service:** Simulates cloud storage (S3/Google Cloud Storage)
- **QGIS Server service:** Version 3.8 with specific configurations for workers, logging, caching, and parallel rendering

### Workflow Steps

1. Downloaded a DEM layer and generated a COG following GDAL procedures
2. Uploaded the raster through the transfer interface
3. Accessed the layer via URL: `http://localhost:8080/KifYI/swellies.tif`
4. Added the raster using QGIS datasource manager
5. Created and configured a QGIS project for QGIS Server publication
6. Modified project URLs from localhost to the Docker service name (transfer)
7. Connected via WMS using: `http://localhost:8081/ows/?MAP=cogo.gqs`

## Technical Advantage

The diagram illustrates "HTTP GET range request" functionality, enabling QGIS Server to access specific image portions without downloading entire files—a key efficiency advantage over traditional approaches like GeoTrellis.
