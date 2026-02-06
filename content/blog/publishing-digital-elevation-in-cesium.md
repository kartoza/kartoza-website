---
title: "Publishing Digital Elevation in Cesium"
description: "The piece explores visualizing terrain data using Cesium, noting that digital elevation data is now readily available from multiple sources."
tags:
  - GeoServer
  - Cesium
  - 3D
date: 2020-11-06
author: "Admire Nyakudya"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="Publishing Digital Elevation in Cesium"
    subtitle="GeoServer"
    class="is-primary"
    sub-block-side="bottom"
>}}
The piece explores visualizing terrain data using Cesium, noting that digital elevation data is now readily available from multiple sources.
{{< /block >}}

## Introduction

The piece explores visualizing terrain data using Cesium, noting that "Digital elevation data is now readily available from multiple sources." The author addresses a gap in available tutorials by providing a complete walkthrough for replicating elevation data visualization.

## Step-by-Step Process

### 1. Download Elevation Data

Sources include the SRTM 30m database and QGIS's SRTM Downloader plugin. The example uses a GeoTIFF file from Kartoza's Docker MapProxy repository.

### 2. Create Seamless Layers

Tools like `gdalbuildvrt` or `gdal_merge.py` merge individual elevation tiles into unified imagery.

### 3. Deploy GeoServer

The workflow uses the Kartoza GeoServer Docker image with the BIL extension installed via command-line deployment, enabling terrain rendering capabilities.

### 4. Publish DEM Data

Users configure BIL format settings when publishing raster layers within GeoServer's interface.

### 5. Test Preview Layer

Layer preview functionality validates successful raster layer configuration.

### 6. Configure Cesium Workshop

Downloads the Cesium workshop materials and modifies HTML/JavaScript files for minimal, focused implementation.

### 7. Implement App.js

A custom JavaScript file defines geographic boundaries and initializes a Cesium viewer with specific configuration options and terrain provider settings.

### 8. Add Terrain Provider

The Cesium-GeoserverTerrainProvider library enables integration between Cesium and GeoServer.

### 9. Deploy Web Server

Nginx Docker configuration serves the Cesium application with proper CORS headers and static file routing.

### 10. Access Visualization

Navigation to localhost:8091 displays interactive 3D terrain visualization.

### 11. Production Considerations

The author recommends replacing default Cesium Ion access tokens with production credentials.

## Technical Configuration

The article includes Docker Compose setup and Nginx configuration files demonstrating server deployment architecture and access control settings.
