---
client: ''
date: '2022-08-02'
description: Kartoza has worked on the Earth Observation National Eutrophication Monitoring
  Programme (EONEMP) and a Mobile Application for Cyanolakes.
erpnext_id: e130445b93
erpnext_modified: '2026-06-04 09:15:15.210813'
github: ''
reviewedBy: Automated Check
reviewedDate: '2026-06-19'
services: []
tags:
- Project
technologies:
- Python
- ESA toolkits for Sentinel data
- GDAL
- Mapserver
- PostGIS
- Django
- Bootstrap
- Leaflet
- ReactJS
thumbnail: https://erp.kartoza.com/files/eonemp.png
title: Cyanolakes
---

{{< block
    title="Cyanolakes"
    subtitle="Project"
    class="is-primary"
    sub-block-side="bottom"
>}}
Kartoza has worked on the Earth Observation National Eutrophication Monitoring Programme (EONEMP) and a Mobile Application for Cyanolakes.
{{< /block >}}

## Overview

# EONEMP

EONEMP (Earth Observation National Eutrophication Monitoring Programme) is a service that generates map layers and reports about the levels of eutrophication in water bodies in South Africa. It inherits from a research prototype by Dr Matthews that did the same for South African coastal waters.

  

Dr Matthews had developed algorithms for detecting cyanobacteria, chlorophyll-a and vegetation in the coastal waters off South Africa for his PhD. He contracted Kartoza, with funding from the Water Research Commission, to automate his image processing workflow and build a web interface to the data, for all dams in South Africa, for the benefit of the public and also to satisfy reporting requirements of the National Department of Water and Sanitation.

  

![](https://kartoza.com/files/eonemp.png)

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

For each reservoir in South Africa it processes Sentinel-3 scenes as soon as they are published and outputs derived spatial and statistical products that are automatically published on the EONEMP website (<http://eonemp.cyanolakes.com>)

  

Kartoza took the coastal water monitoring prototype and Sentinel-2 processing code and did the following:

  1. Developed the Django web application and front-end at <http://eonemp.cyanolakes.com>
  2. Developed MapServer web map services and SLD styles that provide the data layers in the EONEMP web application.
  3. Server side bash and Python scripting to fetch, process and publish Sentinel 3 scenes and derived data on a routine schedule.
  4. Refactoring research algorithms from Dr Matthews in Python into robust production code. This is the code that generates chlorophyll-a, cyanobacteria and other derived products from Sentinel-3 data.

  

# Mobile Application

The CyanoLakes Mobile App was designed to complement the existing web application, providing a mobile-friendly solution for organizations and offering paid-only features for the personal market. Built using React Native and integrating with the existing Django web REST API, its main goal is to display complex water quality information in an intuitive, easy-to-understand, minimalistic way, much like the Apple Weather app. The app features a List View showing a water conditions graphic, nutrient pollution level, and cyanobacteria risk level for water bodies, and a Main View that includes current status, historical data, chlorophyll-a concentration, and cell count. Paid features include an on/off alerts button for notifications about high-risk cyanobacteria blooms and a map feature displaying the location of these blooms.

  

![](https://kartoza.com/files/THsfWeY.png)   ![](https://kartoza.com/files/vxtBnLD.png)

## Technologies

- Python
- ESA toolkits for Sentinel data
- GDAL
- Mapserver
- PostGIS
- Django
- Bootstrap
- Leaflet
- ReactJS
