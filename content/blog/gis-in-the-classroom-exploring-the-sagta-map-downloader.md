---
author: Admire Nyakudya
date: '2022-12-13'
description: GIS is part of the school Geography curriculum in South Africa. Teachers
  need to grasp GIS concepts and teach them in the classroom. Geograp
erpnext_id: /blog/conference/gis-in-the-classroom-exploring-the-sagta-mapdownloader
erpnext_modified: '2022-12-13'
reviewedBy: Automated Check
reviewedDate: '2026-04-13'
tags:
- Conference
thumbnail: /img/blog/erpnext/Blog Post with the Author Instagram (7).png
title: GIS in the classroom - Exploring the SAGTA Map Downloader
---

# Overview

The [FOSS4G](<https://2022.foss4g.org>) conference was in full swing in 2022 after a hiatus due to Covid 19. The conference allows users from accross the globe to meet and share as per the philosophy of FOSS (Free and Open Source Software). I was quite privileged to present the work I have been doing with Geography Teachers in southern Africa.

[SAGTA](<https://sagta.org.za/>) (the Southern African Geography Teachers Association) is a network for professional growth of Geography teachers in southern Africa. Geography teachers are at the core of the SAGTA Map Downloader tool that Kartoza has been developing and maintaing since early 2020. The Map Downloader allows teachers or students to do the following:

  * Download topographic or orthophoto maps that emulate official South African 1:50000 topographical maps or 1:10000 orthophoto maps
  * Download 'hybrid' style maps that are a composite of topographic and orthophoto layers
  * Annotate maps and print various layouts
  * Include optional elements in the the online view and printed versions of the maps



## Software Stack

The SAGTA MapDownloader is powered by [Lizmap Webclient](<https://github.com/3liz/lizmap-web-client>). Other software in the stack includes: * [PostgreSQL](<https://www.postgresql.org/>) * [PostGIS](<https://postgis.net/>) * [GeoServer](<https://geoserver.org/>) * [MapProxy](<https://mapproxy.org/>) * [QGIS Desktop](<https://qgis.org/en/site/>) * [QGIS Server](<https://docs.qgis.org/3.22/en/docs/server_manual/index.html>)

**Deployed software Stack**

![deployed_stack](https://kartoza.erpnext.com/files/Screenshot%20from%202022-09-26%2014-30-41.png)

## Key Features of the tool

## Print AOI (area of interest) on the various map layouts

A user can choose a custom area on the map and print to pdf or various image types.

![map_layout](https://kartoza.erpnext.com/files/print_layout.png)

### Print layouts with magnetic declination and custom grids

This is available on the topographic map layout. The topographic layouts depict the 1:50000 topographic maps provided by the national mapping agency, [NGI](<https://ngi.dalrrd.gov.za/>). These mainly depict the natural and man made features by means of symbols and colour, with elevation represented by spot-heights and contours. The magnetic declination is calculated dynamically using logic from the [NOAA online tool](<https://www.ngdc.noaa.gov/geomag/calculators/magcalc.shtml>), which is wrapped into a QGIS Server Python plugin. The custom grids are also calculated by a QGIS Server plugin as this functionality is not natively available in QGIS.

![mag_decl](https://kartoza.erpnext.com/files/decl-grid.png)

## Elevation profile

This allows users to draw a line on the map along which they would like to see a cross-section. A cross-section, or profile, is calculated with the corresponding values being shown in a plot. This feature mainly uses [lizmap-altiProfil](<https://github.com/arno974/lizmap-altiProfil>), which interpolates a digital elevation model stored in the PostgreSQL database to get the values along the section chosen by the user.

![elevation profile](https://kartoza.erpnext.com/files/profile0ddcc7.png)

## Redlining

User can choose to draw custom shapes to annotate a specific area of interest. These will be visible on the printed map layouts.

![redlining](https://kartoza.erpnext.com/files/redlining.png)

## Map Layouts

There are three main options available for users to explore * Topographic map * Orthophoto map * Hybrid map (consists of blended (composite) orthophoto and topographic map)

The public Lite version has only the topographic maps with limited features. To access the other maps and all features you need to be a member of [SAGTA](<https://sagta.org.za/>). 

The map downloader has gone a long way to assist geography teachers in setting Geography assessments and for general classroom or homework use. The usage of the tool has been very high and it is continually evolving as new features from the software stacks become available or as new feature requests come in from users.
