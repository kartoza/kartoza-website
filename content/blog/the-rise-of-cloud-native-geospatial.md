---
author: Jeff Osundwa
date: '2026-09-25'
description: The geospatial world is changing fast as cloud-native tools reshape spatial
  data storage, discovery, and analysis.
erpnext_id: /blog/cloud-native-gis/the-rise-of-cloud-native-geospatial
erpnext_modified: '2026-09-25'
reviewedBy: Automated Check
reviewedDate: '2026-09-01'
tags:
- Cloud Native Gis
thumbnail: /img/blog/erpnext/cloud-native.png
title: The Rise of Cloud-Native Geospatial
---

For most of GIS history, the workflow has been the same: find a dataset, download it, unzip it, load it into your desktop software, and then work with it locally. It is a process that has served us well for decades, but it breaks down the moment your datasets are measured in terabytes, your users are spread across continents, and your analysis needs to be reproducible and collaborative.

A quiet revolution has been building in the geospatial community over the past few years. It does not have a single flagship product or a dominant vendor behind it. Instead, it is a collection of open specifications, open source tools, and a shift in thinking about how geospatial data should live in the world. This movement is called cloud-native geospatial, and it is changing the game.

## What Does Cloud-Native Geospatial Actually Mean?

![Hero image](/img/blog/erpnext/cloud-native.png)

At its core, cloud-native geospatial is about designing data formats and workflows for the reality that data lives on the internet, not on your hard drive. Traditional geospatial formats like Shapefiles and standard GeoTIFFs were designed for local access. To use them, you need the entire file on your machine. A Shapefile is actually a bundle of at least three files (and often more), and a standard GeoTIFF stores its pixel data in a way that requires reading the whole file to access even a small region.

Cloud-native formats flip this model. They are designed so that a client can make small, targeted HTTP range requests to read just the portion of the data it needs, without downloading the entire file. This means you can visualise a satellite image covering all of Africa without ever downloading more than the pixels visible in your current map viewport. You can run a spatial query on a vector dataset containing millions of features stored in an object bucket, pulling only the rows that intersect your area of interest.

The paradigm shift is simple but profound: instead of moving data to compute, you move compute to data.

## The Key Formats and Specifications

Several specifications have emerged that, taken together, form the cloud-native geospatial stack. None of them are proprietary, and all of them are designed to interoperate.

### Cloud Optimized GeoTIFF (COG)

The [Cloud Optimized GeoTIFF](<https://www.cogeo.org/>) is perhaps the most mature and widely adopted cloud-native format. It is a regular GeoTIFF with a specific internal layout: the image is organised into tiles, and an internal directory (the IFD hierarchy) is placed at the beginning of the file so that a client can quickly discover which byte ranges correspond to which tiles and overview levels. The result is that any HTTP client can stream just the pixels it needs.

COGs have been supported natively in QGIS since version 3.2, and GDAL has been able to read them over HTTP via the `/vsicurl/` virtual filesystem for even longer. Today, most major satellite imagery providers, including Sentinel, Landsat, and the commercial constellations, distribute their data as COGs. At Kartoza, we have been working with COGs in our projects for years, and our [STAC API Browser plugin](<https://kartoza.com/plugins/stac-api-browser/>) loads them directly into QGIS as map layers.

### GeoParquet

If COG solved cloud-native raster, [GeoParquet](<https://geoparquet.org/>) is doing the same for vector data. Parquet is a columnar storage format originally developed in the big data world (Apache Hadoop, Spark, and so on). GeoParquet extends it with a geometry column encoded as Well-Known Binary (WKB), making it a first-class geospatial format.

The advantages are significant. Columnar storage means that a query touching only a few attributes does not need to read the entire row for every feature. Parquet files are splittable, so they can be processed in parallel. And because Parquet is already the de facto format in the data engineering world, GeoParquet slots naturally into modern data pipelines built around tools like DuckDB, Apache Arrow, and Polars.

### STAC (SpatioTemporal Asset Catalog)

Formats solve the storage problem, but you still need a way to find the data you need. [STAC](<https://stacspec.org/>) provides a standardised way to describe and catalogue geospatial assets. A STAC item is a GeoJSON feature with metadata about a spatiotemporal asset: its bounding box, temporal extent, and links to the actual data files (which are often COGs or other cloud-native formats). STAC collections group related items, and STAC APIs provide RESTful search endpoints.

STAC has become the lingua franca for earth observation data discovery. Microsoft Planetary Computer, AWS Open Data, Google Earth Engine, and most national space agencies now expose their archives through STAC APIs. Kartoza developed the [QGIS STAC API Browser plugin](<https://kartoza.com/blog/qgis-stac-api-plugin/>) with funding from Microsoft, and we have seen firsthand how STAC transforms the data discovery workflow from a tedious exercise in navigating download portals into a seamless search-and-load experience inside QGIS itself.

### Zarr and Cloud-Optimised Data Cubes

For multidimensional data, time series, and climate model outputs, [Zarr](<https://zarr.dev/>) has emerged as a cloud-native alternative to NetCDF and HDF5. Zarr stores data as chunked, compressed arrays that can be read in parallel from object storage. Combined with the [Xarray](<https://docs.xarray.dev/>) ecosystem in Python, it enables efficient analysis of massive gridded datasets without loading them into memory.

The [Virtualizarr](<https://virtualizarr.readthedocs.io/>) project takes this further by creating virtual Zarr stores that reference existing NetCDF or GRIB files without copying or converting them, making it possible to treat legacy archives as cloud-native data cubes.

### Apache Iceberg and Icechunk

[Apache Iceberg](<https://iceberg.apache.org/>) is a table format that brings schema evolution, time travel, and ACID transactions to data lakes. While not geospatial-specific, it is increasingly used as the storage layer for large-scale geospatial analytics pipelines. [Icechunk](<https://icechunk.io/>) extends this concept to Zarr-based data, providing versioned, transactional access to multidimensional arrays.

Both are early-stage in the geospatial context, but they represent where the field is heading: geospatial data living in proper data lake architectures, with all the governance, versioning, and scalability benefits that entails.

## The Tools Making It Real

Formats and specifications are only useful if there are tools to work with them. Fortunately, the tooling ecosystem has matured rapidly.

**GDAL Virtual Filesystems** remain the unsung hero of cloud-native geospatial. The `/vsicurl/`, `/vsis3/`, `/vsigs/`, and `/vsiaz/` drivers allow GDAL (and by extension, QGIS, PostGIS, and most open source geospatial software) to read data directly from HTTP endpoints and cloud object stores as if they were local files. This single capability underpins much of the cloud-native stack.

**DuckDB Spatial** has been a revelation. DuckDB is an in-process analytical database (think SQLite for OLAP workloads), and its spatial extension can read GeoParquet files directly from S3, run spatial queries with SQL, and return results in milliseconds. At FOSDEM 2026, the [ClickHouse](<https://clickhouse.com/>) team showed similar capabilities, running analytics over Apache Iceberg tables and GeoParquet files at massive scale. These tools are collapsing the distance between data engineering and geospatial analysis.

**The Python Ecosystem** continues to lead in analysis tooling. Libraries like [stackstac](<https://stackstac.readthedocs.io/>) can take a STAC search result and lazily load it as an Xarray DataArray backed by COGs in cloud storage. [rioxarray](<https://corteva.github.io/rioxarray/>) provides rasterio-powered geospatial operations on Xarray datasets. [PDAL](<https://pdal.io/>) handles point cloud data with similar cloud-native sensibilities.

**QGIS** itself is meeting cloud-native halfway. Beyond native COG support and the STAC plugin, QGIS can connect to WMS/WMTS services that are themselves backed by cloud-native data stores, creating a bridge between the familiar desktop GIS experience and modern cloud infrastructure.

## Why This Matters

The shift to cloud-native geospatial is not just a technical curiosity. It has real implications for how organisations work with spatial data.

**Democratisation of Access.** When data lives behind a download portal, access is gated by bandwidth, storage, and patience. Cloud-native formats allow anyone with an internet connection to query petabyte-scale datasets from a laptop. This is transformative for researchers, NGOs, and organisations in regions where high-speed connectivity and large storage are not a given.

**Reproducibility.** When your analysis references data by URI rather than relying on a local copy, your workflow is inherently reproducible. Anyone can run the same code against the same data without needing to replicate your local file structure.

**Cost Reduction.** Traditional geospatial pipelines involve copying data from a source, storing it locally, and then processing it. Cloud-native workflows eliminate the copy step entirely. You pay for compute and egress, not for redundant storage.

**Scalability.** Cloud-native formats are designed for parallel access and distributed processing. Whether you are analysing a single Sentinel-2 scene or processing a decade of archive data across an entire continent, the same tools and patterns apply.

## What is Still Difficult?

It would be disingenuous to suggest that cloud-native geospatial has solved everything. Several challenges remain.

**Authentication and Authorisation.** Most cloud-native tooling assumes either fully public data or simple token-based auth. Enterprise environments with complex identity management, SAML/OIDC federation, and fine-grained access control still require significant integration work.

**Latency in Developing Regions.** Cloud-native workflows depend on reliable, low-latency internet connections. In many parts of Africa, South America, and Southeast Asia, the round-trip time to major cloud regions can make interactive cloud-native analysis frustrating. Edge caching and regional data replicas help, but they add complexity.

**Tooling Maturity.** While the core tools are solid, the ecosystem is still young. Error messages can be cryptic, documentation is scattered, and the learning curve for someone coming from a traditional GIS background is steep. The gap between "possible" and "easy" is still wide.

**Inertia.** Shapefiles and GeoTIFFs are deeply embedded in workflows, training materials, and institutional knowledge. Convincing organisations to change how they store and share data is as much a cultural challenge as a technical one.

## Where Kartoza Fits

At Kartoza, we have been active participants in the cloud-native geospatial movement from its early days. We built the QGIS STAC API Browser plugin, bringing cloud-native data discovery directly into the desktop GIS environment. We maintain Docker images for PostGIS, GeoServer, and other components of the open source geospatial stack, and we are actively exploring how to integrate cloud-native formats into these services.

Our [managed hosting platform](<https://kartoza.com/hosting/>) is being built with cloud-native geospatial as a first-class citizen. We see a future where our customers can spin up a GeoServer instance pre-configured to serve data from COGs in object storage, or a DuckDB-powered analytics endpoint that queries GeoParquet files in place, without needing to manage the underlying infrastructure.

We are also watching the emergence of Apache Iceberg and Icechunk with great interest, particularly for clients managing large, versioned geospatial datasets in biodiversity monitoring, climate analysis, and environmental management.

## The Hybrid Future

Cloud-native geospatial is not going to replace your desktop GIS. QGIS is not going away, and there will always be workflows that benefit from having data locally. But cloud-native is giving GIS a superpower: the ability to work with data at a scale and with a fluidity that was simply impossible a few years ago.

The future is hybrid. Your field survey data lives in a GeoPackage on your laptop. Your satellite imagery archive lives as COGs in an S3 bucket, catalogued by STAC. Your vector analytics run as SQL queries over GeoParquet in DuckDB. Your time series analysis uses Zarr and Xarray. And all of it is accessible from the same QGIS window, the same Python notebook, or the same web application.

The pieces are here. The specifications are open. The tools are free. The only thing left is to start using them.

If you are exploring cloud-native geospatial for your organisation and need help navigating the technology choices, [get in touch](<https://kartoza.com/contact-us/>). We would love to help you build a solution that works.
