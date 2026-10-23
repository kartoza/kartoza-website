---
author: Jeff Osundwa
date: '2026-09-25'
description: The geospatial world is undergoing a quiet revolution. Cloud-native formats
  and tools are reshaping how we store, discover, and analyse spatial data at scale.
draft: true
erpnext_id: /blog/cloud-native-gis/the-rise-of-cloud-native-geospatial
erpnext_modified: '2026-09-25'
reviewedBy: Automated Check
reviewedDate: '2026-10-23'
tags:
- Cloud Native Gis
thumbnail: /img/blog/erpnext/cloud-native.png
title: The Rise of Cloud-Native Geospatial
---

I started using GIS the way most people do: find a dataset, download it, unzip it, and load it into desktop software. It worked for years. It still works, until your datasets are measured in terabytes, your users span continents, and you need your analysis to be reproducible instead of locked to one machine.

Cloud-native geospatial is the emerging answer. There is no single flagship product or dominant vendor behind it, just open specifications, open source tools, and a change in how geospatial data is meant to live on the internet rather than on a hard drive.

## What does cloud-native geospatial actually mean?

Traditional formats were designed for local access. To open a Shapefile you need the whole bundle, it is really at least three files, often more. A standard GeoTIFF stores its pixels so that reading even a small region requires loading the whole file. All of this assumes the data is on your disk.

Cloud-native formats flip that. A client can make small, targeted HTTP range requests and read only the portion of the data it needs. You can view a satellite image covering all of Africa and download no more than the pixels in your current viewport. You can run a spatial query against a vector dataset with millions of features, pulling only the rows that intersect your area of interest, while the file sits in an object bucket. The data stays put; the computation moves to it.

## The key formats and specifications

Several specifications form the cloud-native geospatial stack. They are all open and designed to interoperate.

### Cloud Optimized GeoTIFF (COG)

The [Cloud Optimized GeoTIFF](<https://www.cogeo.org/>) is the most mature and widely adopted cloud-native format. It is a regular GeoTIFF with a specific internal layout: the image is tiled, and an internal directory sits at the start of the file, letting a client discover which byte ranges hold which tiles and overviews. An HTTP client can then stream just the pixels it needs.

QGIS has supported COGs natively since version 3.2, and GDAL could read them over HTTP through `/vsicurl/` even earlier. Most major satellite imagery providers, Sentinel, Landsat, and the commercial constellations, now distribute their data as COGs. We have used them at Kartoza for years; our [STAC API Browser plugin](</plugins/stac-api-browser/>) loads them straight into QGIS as map layers.

### GeoParquet

If COG solved cloud-native raster, [GeoParquet](<https://geoparquet.org/>) is doing the same for vector data. It extends Parquet, the columnar format from the big data world, Apache Hadoop and Spark and the rest, with a geometry column encoded as Well-Known Binary, making it a proper geospatial format.

Columnar storage means a query that touches only a few attributes does not read the whole row for every feature. Parquet files split for parallel processing. And because Parquet is already the default in data engineering, GeoParquet fits naturally into pipelines built around DuckDB, Apache Arrow, and Polars.

### STAC (SpatioTemporal Asset Catalog)

Formats solve storage; you still need to find the data. [STAC](<https://stacspec.org/>) standardises how geospatial assets are described and catalogued. A STAC item is a GeoJSON feature carrying metadata about an asset, its bounding box, temporal extent, and links to the actual data files, which are often COGs. STAC collections group related items, and STAC APIs expose RESTful search.

STAC has become the working language of earth observation data discovery. Microsoft Planetary Computer, AWS Open Data, Google Earth Engine, and most national space agencies publish archives through STAC APIs. We built the [QGIS STAC API Browser plugin](</blog/qgis-stac-api-plugin/>) with funding from Microsoft, and we have watched it turn what used to be a round trip to a download portal into a search-and-load step inside QGIS.

### Zarr and cloud-optimised data cubes

[Zarr](<https://zarr.dev/>) has emerged as the cloud-native alternative to NetCDF and HDF5 for multidimensional data, time series, and climate model output. It stores chunked, compressed arrays that can be read in parallel from object storage. Combined with the [Xarray](<https://docs.xarray.dev/>) ecosystem, it allows analysis of massive gridded datasets without loading them into memory.

The [Virtualizarr](<https://virtualizarr.readthedocs.io/>) project goes further: it builds virtual Zarr stores that reference existing NetCDF or GRIB files without copying or converting them, so legacy archives behave like cloud-native data cubes.

### Apache Iceberg and Icechunk

[Apache Iceberg](<https://iceberg.apache.org/>) is a table format that brings schema evolution, time travel, and ACID transactions to data lakes. It is not geospatial-specific, but it is increasingly the storage layer for large-scale geospatial analytics. [Icechunk](<https://icechunk.io/>) brings the same versioned, transactional idea to Zarr-based arrays.

Neither is mature in a geospatial context yet, but they point the direction of travel: geospatial data living in proper data lake architectures, with the governance and versioning that come with them.

## The tools making it real

Specifications only matter if the tools exist. The tooling has now caught up.

**GDAL virtual filesystems** are quietly the workhorse. The `/vsicurl/`, `/vsis3/`, `/vsigs/`, and `/vsiaz/` drivers let GDAL, and with it QGIS, PostGIS, and most open source geospatial software, read directly from HTTP endpoints and cloud object stores as if they were local files. A lot of the cloud-native stack rests on that one capability.

**DuckDB Spatial** has changed how vector analytics feel. DuckDB is an in-process analytical database, SQLite for OLAP, and its spatial extension reads GeoParquet directly from S3, runs SQL spatial queries, and returns results in milliseconds. At FOSDEM 2026 the [ClickHouse](<https://clickhouse.com/>) team demonstrated similar performance over Apache Iceberg tables and GeoParquet, at much larger scale. The distance between data engineering and geospatial analysis is collapsing.

**The Python ecosystem** still leads on analysis. [stackstac](<https://stackstac.readthedocs.io/>) takes a STAC search result and loads it lazily as an Xarray DataArray backed by COGs in cloud storage. [rioxarray](<https://corteva.github.io/rioxarray/>) adds rasterio-powered geospatial operations to Xarray. [PDAL](<https://pdal.io/>) handles point clouds with the same cloud-native sensibilities.

**QGIS** meets cloud-native halfway. Beyond native COG support and the STAC plugin, it can connect to WMS/WMTS services that are themselves backed by cloud-native stores, a bridge between the familiar desktop GIS and modern cloud infrastructure.

## Why this matters

The point is not abstract. When data lives behind a download portal, access is limited by bandwidth, storage, and patience. Cloud-native formats let anyone with a connection query petabyte-scale datasets from a laptop, a real difference for researchers, NGOs, and people working where high-speed connectivity and large storage are not a given.

The same applies to reproducibility. If an analysis references data by URI instead of a local copy, someone else can run the same code against the same data without recreating your file layout. Cost and scale follow: cloud-native workflows drop the copy-then-store step of the old pipeline, and the formats are built for parallel, distributed processing whether the job is one Sentinel-2 scene or a decade of archive over a whole continent.

## What is still hard

None of this is frictionless yet. The sticking points are practical.

Enterprise environments are the hard case for authentication. Most cloud-native tooling assumes either fully public data or simple token auth; complex identity management, SAML/OIDC federation, and fine-grained access control still need real integration work.

Latency is another. Cloud-native workflows depend on reliable, low-latency connections, and in parts of Africa, South America, and Southeast Asia the round trip to a major cloud region makes interactive use frustrating. Edge caching and regional replicas help, at the cost of complexity.

The tooling is also still young. The core tools are solid, but error messages can be cryptic and documentation is scattered; the learning curve from a traditional GIS background is steep. And the biggest blocker is inertia, Shapefiles and GeoTIFFs are embedded in workflows, training material, and institutional habit. Changing how an organisation stores data is a cultural problem as much as a technical one.

## Where Kartoza fits

We have been in the cloud-native space since its early days. We built the QGIS STAC API Browser plugin, bringing cloud-native discovery directly into the desktop GIS. We maintain Docker images for PostGIS, GeoServer, and other parts of the open source geospatial stack, and we are working on how to build cloud-native formats into those services.

Our [managed hosting platform](</hosting/>) treats cloud-native geospatial as a first-class concern. The direction we are building towards: a customer spins up a GeoServer instance pre-configured to serve COGs from object storage, or a DuckDB analytics endpoint that queries GeoParquet in place, without managing the infrastructure underneath.

We are also following Apache Iceberg and Icechunk closely, particularly for clients with large, versioned geospatial datasets in biodiversity monitoring, climate analysis, and environmental management.

## The hybrid future

Cloud-native geospatial is not replacing the desktop GIS. QGIS is not going anywhere, and plenty of workflows still want data locally. What it does is remove the old limit on scale and reuse.

The realistic setup a few years from now is mixed: field survey data in a GeoPackage on a laptop, a satellite archive as COGs in an S3 bucket catalogued by STAC, vector analytics as SQL over GeoParquet in DuckDB, time series in Zarr and Xarray, all reachable from the same QGIS window, Python notebook, or web application.

The specifications are open and the tools are there. The practical question is where to start, and that is usually specific to the datasets and users involved. If you are working through cloud-native geospatial for your organisation, [get in touch](</contact-us/>), we are happy to help you figure out a setup that works.
