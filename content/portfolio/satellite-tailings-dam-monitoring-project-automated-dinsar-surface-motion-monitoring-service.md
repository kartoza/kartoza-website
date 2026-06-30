---
client: EOIntelligence LTD
date: '2025-01-16'
description: EOIntelligence, in partnership with Kartoza (Pty) Ltd., has developed
  a fully automated, satellite-based monitoring service for tailings storage facilities
  (TSFs), mine waste dumps, pit slopes, and ot
erpnext_id: krtoiprsqr
erpnext_modified: '2026-06-04 14:33:06.672438'
github: ''
reviewedBy: Automated Check
reviewedDate: '2026-06-19'
services:
- GIS Desktop Development
- GIS Web Development
- GIS Analysis
tags:
- Project
technologies:
- G3W Suite
- QGIS
thumbnail: https://erp.kartoza.com/files/Satellite_Tailings_cover.png
title: 'Satellite Tailings Dam Monitoring Project: Automated dInSAR Surface Motion
  Monitoring Service'
---

{{< block
    title="Satellite Tailings Dam Monitoring Project: Automated dInSAR Surface Motion Monitoring Service"
    subtitle="Project"
    class="is-primary"
    sub-block-side="bottom"
>}}
EOIntelligence, in partnership with Kartoza (Pty) Ltd., has developed a fully automated, satellite-based monitoring service for tailings storage facilities (TSFs), mine waste dumps, pit slopes, and other critical mining infrastructure. The service uses Differential Synthetic Aperture Radar Interferometry (dInSAR) on Sentinel-1 data to deliver millimetre-accurate surface deformation measurements at a fraction of the cost and effort of traditional ground-based surveys.
{{< /block >}}

## Overview

Results are delivered through two complementary channels:

  1. A professionally formatted PDF report containing executive alerts, velocity maps, time-series plots, quality metrics, and interpretation notes.
  2. An interactive web-GIS interface (G3W) where clients can explore the data themselves, query point time series, toggle layers, and export subsets.

The entire process is triggered by a simple KML polygon upload, making the service accessible even to users without remote-sensing expertise.

### **Minimum Viable Product Workflow (Automated End-to-End)**

Clients (or channel partners) supply a KML file defining the Area of Interest (AOI). The system:

  1. Ingests the KML and automatically selects the 20 most recent Sentinel-1 LOS scenes.
  2. Downloads and pre-processes auxiliary data (Copernicus DEM, ERA5 atmospheric corrections, precise orbits).
  3. Executes the full dInSAR processing chain with automatic reference-point selection.
  4. Performs ascending + descending orbit processing where available, enabling 2-D decomposition of vertical and horizontal motion.
  5. Clips all output layers to the client AOI.
  6. Generates a standardised PDF report in OpenDocument format, auto-populated with maps, graphs, coherence statistics, and alert tables.
  7. Publishes velocity, coherence, and time-series layers to a dedicated G3W instance.
  8. Creates a unique username/password for the client, valid for 30 days.

The report and login credentials are automatically forwarded to the channel partner, who handles client communication, final QA, invoicing, and customer support, earning a 30 % commission.

### **Visualisation on G3W Web-GIS**

The G3W platform provides an intuitive, browser-based experience:

  1. Single-click layer activation (velocity, coherence, time-series points, background imagery).
  2. RGB velocity symbology: red = movement away from sensor, green = stable, blue = movement towards sensor.
  3. Interactive time-series graphs: click any measurement point to view displacement history.
  4. Layer options: opacity slider, attribute table, WMS URL export.
  5. Thematic grouping and permission controls ensure each client sees only their AOI.

Administrators can quickly create new projects, upload QGIS projects, manage users/groups, and perform quality checks via the same web interface (full guidance provided in the G3W User & Administrator Manual).

![](/files/qAd6Hsy.png)

![](/files/rFGuKP3.png)

### **Key Benefits for Mining Operations**

  1. **Safety & Compliance** — Early detection of millimetre-scale movement enables proactive risk management and regulatory reporting.
  2. **Cost Efficiency** — No need for repeated drone or terrestrial surveys over large areas; one subscription covers continuous monitoring.
  3. **Scalability** — The same workflow supports single TSFs or entire mining complexes across multiple sites.
  4. **Rapid Turnaround** — From KML upload to report + live web-GIS in a fully automated pipeline.
  5. **Quality Assurance** — Every dataset includes comprehensive coherence and error statistics so engineers can assess reliability.
  6. **User-Friendly Delivery** — Mine managers receive both a ready-to-share PDF and a live web viewer—no specialist software required.

### **Business Model & Partnership**

The service is offered through authorised channel partners. Partners manage client relationships, customise reports if needed, and invoice end-users while the automated backend handles all data processing and delivery. Partners receive 30 % commission on each completed AOI package. New instances are provisioned instantly, and the system supports both one-off and subscription monitoring contracts.

### **Technical Summary**

  1. Satellite: Sentinel-1 A/B (C-band, 6–12-day revisit).
  2. Processing: Full-resolution dInSAR with atmospheric correction and automatic reference-point optimisation.
  3. Output formats: GeoTIFF velocity/coherence layers, shapefiles, PDF report (ODT), G3W web project.
  4. Accuracy: Typically < 5 mm/yr standard deviation on coherent surfaces (validated against corner reflectors and GNSS where available).

![](/files/CyjNarA.png)

### **Conclusion**

The EOIntelligence–Kartoza Satellite Tailings Dam Monitoring Service transforms how mines monitor critical infrastructure. By combining the unparalleled coverage of Sentinel-1 with fully automated processing and professional visualisation tools, the service delivers actionable intelligence directly to the people who need it—mine managers, tailings engineers, and survey teams—while keeping operational overhead to a minimum.

Channel partners benefit from a high-margin, low-effort value-added service that strengthens client relationships and opens new revenue streams in the growing field of remote mine monitoring.

## Client

EOIntelligence LTD

## Technologies

- G3W Suite
- QGIS
