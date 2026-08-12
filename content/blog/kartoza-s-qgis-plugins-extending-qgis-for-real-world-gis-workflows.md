---
author: Jeff Osundwa
date: '2026-08-14'
description: 'Discover Kartoza''s QGIS plugins: STAC API Browser, Species Explorer,
  SG Diagram Downloader, Trends.Earth and more — built for real-world GIS'
erpnext_id: /blog/qgis/kartozas-qgis-plugins-extending-qgis-for-real-world-gis-workflows
erpnext_modified: '2026-08-14'
reviewedBy: Automated Check
reviewedDate: '2026-08-12'
tags:
- Qgis
thumbnail: https://erp.kartoza.com/private/files/stac-api.png
title: 'Kartoza''s QGIS Plugins: Extending QGIS for Real-World GIS Workflows'
---

QGIS is powerful out of the box, but its real superpower is extensibility. For over a decade, Kartoza has been building, sponsoring, and maintaining QGIS plugins that solve genuine geospatial problems — from cadastral surveying in South Africa to monitoring land degradation for the United Nations Sustainable Development Goals. This post is a quick tour of the plugins we ship, where to find them, and how they fit into a modern open source GIS workflow.

## Discovering and Installing Plugins

The QGIS plugin ecosystem saw a major upgrade last year with the relaunch of the [QGIS Plugins website](<https://plugins.qgis.org>) and the launch of the [QGIS Hub](<https://hub.qgis.org>). We covered that in a [post at the time](<https://kartoza.com/blog/introducing-the-new-qgis-plugins-website-and-qgis-hub/>), but the short version: better categorisation, clearer plugin pages with ratings and download counts, and a dedicated home for sharing styles, 3D models, and project files.

To install any of the plugins below, open **Plugins → Manage and Install Plugins** in QGIS, search by name, and click **Install Plugin**.

## STAC API Browser

![stac-api-browser](https://erp.kartoza.com/private/files/stac-api.png)

The [STAC API Browser](<https://kartoza.com/plugins/stac-api-browser/>) brings cloud-native earth observation data discovery into QGIS. Developed by Kartoza with funding from Microsoft Planetary Computer, it lets you search STAC-compliant catalogs, filter by date and spatial extent, preview footprints, and load assets as Cloud Optimised GeoTIFF layers — without leaving your map canvas. Our [launch post](<https://kartoza.com/blog/qgis-stac-api-plugin/>) walks through the workflow in detail.

## Species Explorer

![species-explorer](https://erp.kartoza.com/private/files/species-explorer.png)

If biodiversity data is your focus, the [Species Explorer](<https://kartoza.com/plugins/species-explorer/>) fetches species occurrence records straight from the Global Biodiversity Information Facility (GBIF) into QGIS. Search by scientific or common name, refine by date range, and turn results into map layers ready for analysis or cartography. It is a handy companion for conservation, ecology, and environmental impact work.

## SG Diagram Downloader

![sg-diagram-downloader](https://erp.kartoza.com/private/files/sg-downloader.png)

Surveyors working with South African cadastral data will appreciate the [SG Diagram Downloader](<https://kartoza.com/plugins/sg-diagram-downloader/>). Sponsored by Kirchhoff Surveyors, it downloads official Surveyor General diagrams directly within QGIS — no more browser hopping, manual file naming, or broken download links. It is one of several Kartoza plugins tailored to African geospatial workflows.

## Trends.Earth

![trends-earth](https://erp.kartoza.com/private/files/trends-earth-plugin.png)

[Trends.Earth](<https://kartoza.com/plugins/trends-earth/>) takes on a broader mission: tracking land productivity, land cover, and soil organic carbon in support of UN Sustainable Development Goal 15.3 (Life on Land). Developed with Conservation International, it gives governments and researchers standardised, reproducible methods for monitoring land degradation neutrality.

## Specialised Applications Built as QGIS Plugins

Not every Kartoza QGIS extension lives in the public plugin repository. Some are deeper applications, listed on our [apps page](<https://kartoza.com/apps/>).

- **[SAGTA Map Exporter](<https://kartoza.com/apps/sagta/>)** — exports compliant cadastral and surveying maps according to South African Geomatics Technicians Association standards.
- **[Giswater](<https://kartoza.com/apps/giswater/>)** — models water supply and urban drainage networks inside QGIS, including running EPANET and SWMM simulations.

## Plugins and QGIS Server

A great plugin workflow often ends with publishing. The same rendering engine behind every plugin above also powers our production [QGIS Server Docker image](<https://kartoza.com/docker/qgis-server/>) — publish `.qgs`/`.qgz` projects as OGC-compliant web services with pixel-perfect fidelity to what you see on your desktop. It's the natural next step when a plugin-built project needs to reach a wider audience.

## Resources and Next Steps

- Grab the [QGIS Renderers Cheat Sheet](<https://kartoza.com/qgis-resources/>) for a quick reference on vector and raster styling.
- Developers curious about contributing to QGIS itself can follow our [Road to Nerdvana series](<https://kartoza.com/blog/qgis-road-to-nerdvana-episode-1-qgis-console-build/>), which documents building and patching QGIS from source.
- If your team needs guided learning, we run [QGIS training courses](<https://kartoza.com/training-courses/>) hosted at our Cape Town and Stellenbosch offices or remotely.

## Install One Today

Every plugin above is in the official QGIS plugin repository and is free and open source. Install the ones that fit your workflow, star them on [plugins.qgis.org](<https://plugins.qgis.org>), and file issues or feature requests on the linked GitHub repositories. QGIS is a community effort — Kartoza funds full-time QGIS staff through community donations, and every install, review, and contribution helps sustain that work.
