---
client: Spinning Your Web Pty Ltd
date: '2025-01-20'
description: Kartoza was contracted by Spinning Your Web Pty Ltd (SYW) to further
  develop the mapping functionality for EVS ForestWatch Mobile Fire Alert & Monitoring
  Solution.
erpnext_id: ql87t8nvni
erpnext_modified: '2026-06-04 14:49:55.461581'
github: https://github.com/kartoza/EVS
reviewedBy: Automated Check
reviewedDate: '2026-07-01'
services: []
tags:
- Project
technologies: []
thumbnail: https://erp.kartoza.com/files/EVS_fireweb_cover.png
title: EnviroVision Map Integration with FireWeb
---

{{< block
    title="EnviroVision Map Integration with FireWeb"
    subtitle="Project"
    class="is-primary"
    sub-block-side="bottom"
>}}
Kartoza was contracted by Spinning Your Web Pty Ltd (SYW) to further develop the mapping functionality for EVS ForestWatch Mobile Fire Alert & Monitoring Solution.
{{< /block >}}

## Overview

The primary focus was on front-end work of the platform.

  

The functionality for the EVS Mobile Mapping feature, was divided into three main areas:

  1. **Default Map:** This involves displaying sites, weather stations, and alarms from tables on a map with unique icons. Alarms show on the mapping interface with a dotted line to the site that identified and reported the report with a click through link to the alarm interface. This task was primarily pulling the information out of the local database and presenting it correctly on the mapping interface.
  2. **Map Interactions:** This involves adding various interactive features to the map interface, accessible through a drop-down menu.

The interactions include:

  1. **Center On** : Centering the map on the user's location (or custom location override) or defined regions of interest.
  2. **All Features** : Displaying all sites, weather stations, and alarms on the map.
  3. **What Can See** : Showing the closest four sites to a selected custom point or the user's location, along with camera images and weather conditions.
  4. **Cameras:** Displaying a list of cameras from a database, centering the map on a selected camera, and providing access to camera images and information.
  5. **Weather Stations:** Displaying a list of weather stations from a database, centering the map on a selected station, and providing weather details.
  6. **Base Layer Toggle:** Allowing users to switch between hybrid, satellite, and street view base layers.
  7. **Regions of Interest:** This involves users drawing polygons on a map in the settings module. Currently, these regions are stored in a database. The remaining work to complete this functionality includes:
  8. **Storage:** This involves processing existing regions of interest in a database and transferring them to the FireWeb API, as well as retrieving them from the FireWeb API upon authentication.
  9. **Auto Plot** (with an option to increase size by a buffer). This includes:
  10. Auto plot by favorite group - Selecting all cameras within a favorite group and displaying a visible polygon. Users should be able to save, edit, and delete the region of interest from the auto-plot.
  11. Auto plot region - Selecting cameras within an instance or region and displaying a visible polygon. Users should be able to save, edit, and delete the region of interest from the auto-plot.
  12. The ability to edit and delete a region of interest.

  

![https://kartoza.com/files/EVS_fireweb_5.png](https://kartoza.com/files/EVS_fireweb_5.png)   ![https://kartoza.com/files/EVS_fireweb_6.png](https://kartoza.com/files/EVS_fireweb_6.png)

## Client

Spinning Your Web Pty Ltd

## Source Code

[GitHub](https://github.com/kartoza/EVS)
