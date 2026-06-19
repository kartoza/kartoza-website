---
client: ''
date: '2022-08-02'
description: InaSAFE is an open-source disaster planning tool that helps governments
  quickly model the potential impacts of floods, earthquakes, and other natural hazards.
  Kartoza developed the QGIS plugin, real-t
erpnext_id: ea6810a490
erpnext_modified: '2026-02-25 09:15:54.837116'
github: https://github.com/inasafe/inasafe
reviewedBy: Automated Check
reviewedDate: '2026-06-19'
services:
- Capacity Building and Training
- Support and Maintenance
- Software Development and Enhancement
- Governance and Sustainability
- Support and Promotion
tags:
- Project
technologies:
- InaSAFE
- QGIS
- Python
- GeoNode
thumbnail: https://erp.kartoza.com/files/InaSAFE.png
title: InaSAFE Disaster Scenario Contingency Planning Software
---

{{< block
    title="InaSAFE Disaster Scenario Contingency Planning Software"
    subtitle="Project"
    class="is-primary"
    sub-block-side="bottom"
>}}
InaSAFE is an open-source disaster planning tool that helps governments quickly model the potential impacts of floods, earthquakes, and other natural hazards. Kartoza developed the QGIS plugin, real-time analysis system, and web-based GeoSAFE interface to make impact assessments accessible to both technical and non-technical users. Today, InaSAFE supports national disaster management efforts by generating clear maps, reports, and recommended actions for faster, evidence-based decision-making.
{{< /block >}}

## Overview

InaSAFE is a free, open-source tool used to model and plan for natural disasters such as floods, earthquakes, volcanic eruptions, tsunamis, fires, and hurricanes. Initially supported by the Indonesian government with funding from Australia, InaSAFE combines hazard and exposure data to estimate the potential impact of disaster events and produce actionable reports. Kartoza has played a key role in designing, building, and maintaining the InaSAFE ecosystem, including the QGIS plugin, documentation, and supporting interfaces. The software generates clear maps, impact summaries, and recommended actions, helping disaster managers plan responses, allocate resources, and communicate risk to stakeholders.

  

### InaSAFE Plugin

  

The InaSAFE Desktop Plugin is the core interactive component of the system, distributed as a plugin for QGIS. Kartoza co-developed the plugin with DMInnovation to provide rapid scenario assessments using local hazard and exposure data. Users can run simulations directly on their computers, create impact maps, and export PDF reports that detail likely affected areas and estimated consequences, including infrastructure damage and expected casualties. Kartoza remains actively involved in developing new features, improving usability, and supporting the wider community of practitioners.

  

![](/files/c0LXW4k.png)

  

### InaSAFE Realtime

  

Kartoza also led the development of InaSAFE Realtime, an automated server-side deployment designed to deliver near real-time impact estimates after major disaster events. Built on top of InaSAFE libraries and enhancements to core QGIS functionality, the system ingests rapidly updating hazard data (such as earthquake shake maps or flood forecasts), runs automated impact calculations, and generates authoritative cartographic outputs within minutes. During this work, Kartoza contributed major improvements to the QGIS ecosystem, including raster rendering, Web Coverage Service (WCS) support, print composition, and Python bindings, to support fast, reliable automated map generation. The result is a robust system that can deliver actionable, time-critical information to national disaster management agencies and emergency operations centers.

  

![](/files/EBjqUJQ.png)

  

### GeoSAFE

  

To extend InaSAFE’s capabilities to a broader audience, Kartoza created GeoSAFE, a web-based interface that allows users to run InaSAFE analyses through a browser without needing desktop GIS software. Built on GeoNode, GeoSAFE centralizes data management and supports collaborative scenario planning across agencies and geographic regions. Kartoza also deployed full production GeoSAFE systems, including a national-scale implementation for INGC in Mozambique, where users can access hazard data, run impact models, and generate reports online. This work included integrating QGIS Server as a backend, enhancing GeoNode features, and using Docker-based orchestration tools to manage scalable deployments.

  

![](/files/KMKqkIc.png)

## Technologies

- InaSAFE
- QGIS
- Python
- GeoNode

## Source Code

[GitHub](https://github.com/inasafe/inasafe)
