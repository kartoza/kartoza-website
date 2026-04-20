---
author: Admire Nyakudya
date: '2018-02-02'
description: Kartoza releases the CoGo Plugin for QGIS Kartoza recently published
  the CoGo Plugin (aka Parcel Plugin) in the QGIS plugin repository.
erpnext_id: /blog/qgis/a-new-plugin-to-manage-land-survey-parcels-in-qgis
erpnext_modified: '2018-02-02'
reviewedBy: Automated Check
reviewedDate: '2026-04-13'
tags:
- Qgis
thumbnail: /img/blog/erpnext/5qmnUx1.jpg
title: A New Plugin to Manage Land (survey) Parcels in QGIS
---

#### Kartoza releases the CoGo Plugin for QGIS

Kartoza recently published the CoGo Plugin (aka Parcel Plugin) in the QGIS plugin repository. This plugin expands the group of plugins designed to manage SDI (Spatial Data Infrastructure). CoGo ('coordinate geometry') refers to its ability to handle both types of coordinates used in land surveying, namely cartesian coordinates (x,y; long/lat) and polar coordinates (bearing and distance).

Kartoza began development of the plugin in 2012 as part of a project commissioned by [Spatial Matrix](<http://spatialmatrix.com/>) to facilitate the digitising of cadastral property records in Ogun State, Nigeria, where it was (and still is) successfully used in production. In 2016 the plugin was updated by Kartoza and deployed in Niger state, again by Spatial Matrix. In production use, it also helped identify surveying problems eg. land parcels that are overlapping and gaps between land parcels.

﻿Example of Survey Diagram

![](/img/blog/erpnext/5qmnUx1.jpg)

#### Why the CoGo plugin?

Cadastral surveying is concerned with the survey and demarcation of land for the purpose of defining parcels of land for registration in a land registry. Any survey that has to be captured in a GIS has to be a true reflection of what occurs on the ground and what is represented by survey diagrams. To do this, we needed to define a tool that allows beacons to be captured and edited, bearings and distances to be defined and then use these to automatically define the land parcels. The plugin supports multiple users working on the same PostGIS database. It facilitates efficient and accurate data capture by operators as well as bulk uploading of structured data.

#### Features of the plugin

  1. Supports PostgreSQL 9.6 and higher
  2. Runs materialised views and their triggers which increases speed for rendering data in QGIS
  3. A database manager which is linked to the default PostgreSQL database provider in QGIS
  4. Simple tool to set up the database and associated tables required by the plugin
  5. A simple user interface: Beacon Manager, Parcels Manager and Bearings and Distance Manager
  6. A custom topological model where the only simple geometries are beacons, while parcels are defined in views. Beacons defined by bearing and distance strictly honour change
  7. Sample survey diagram Composer templates for generating official survey diagrams from the now-digital survey data

Example Survey Diagram in map composer.

![](/img/blog/erpnext/RUnQFjB.png)

Much of the core plugin functionality is embedded in the PostgreSQL database. For users who are competent in SQL, it is an advantage as they can do clever SQL to derive more information from the land parcels that have been captured e.g. identifying overlapping parcels or interacting with the parcels in a web front-end. In Ogun State, a localised instance of [1Map](<https://www.1map.co.za/>) was used as a management and QA dashboard, as a public interface to the cadastre and as a tool for facilitating [charting](<https://oticsurveys.com/charting_in_lagos/>) at the front desk of the survey office. It ran live on the same database that the operators were working on with QGIS in the back office.

QGIS Plugin Manager

![](/img/blog/erpnext/bKemsNj.png)

CoGo Plugin icons

![](/img/blog/erpnext/dFpCiN0.png)

GIS has come a long way in alleviating paper formats for maps, survey diagrams, and this tool will be useful for Surveyors and users involved in SDI. Kartoza will strive to continuously improve the plugin when time and resources are available.

Find out more in the [User manual](<http://goo.gl/CY9TYn>)and the [repository.](<https://github.com/kartoza/parcel_plugin>)

####
