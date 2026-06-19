---
client: ''
date: '2025-01-17'
description: 'Kartoza and Lutra worked together to undertake a key technical initiative:
  the integration of Mergin to create a robust and efficient workflow for mobile Geographical
  Information System (GIS) data col'
erpnext_id: bdt71lbl6v
erpnext_modified: '2026-06-04 14:39:46.849987'
github: ''
reviewedBy: Automated Check
reviewedDate: '2026-06-19'
services: []
tags:
- Project
technologies: []
thumbnail: https://erp.kartoza.com/files/Lutra-Mergin-1.png
title: Lutra-Mergin
---

{{< block
    title="Lutra-Mergin"
    subtitle="Project"
    class="is-primary"
    sub-block-side="bottom"
>}}
Kartoza and Lutra worked together to undertake a key technical initiative: the integration of Mergin to create a robust and efficient workflow for mobile Geographical Information System (GIS) data collection. 
{{< /block >}}

## Overview

This work was essential for enabling the mobile data collection application, Input, with enterprise-grade synchronisation capabilities.

  

The successful deployment of a touch-friendly mobile data collection app required a powerful, reliable solution for data synchronisation, server-side change management, and collaborative work. The team recognised that reliance on file-based data sets often leads to problems like data duplication, difficulty managing changes across multiple users, and challenges in resolving data conflicts when the same feature is edited concurrently. A platform was needed that was optimised for mobile devices, while remaining deeply integrated with the desktop GIS standard, QGIS.The Solution: Mergin Integration

  

The team strategically integrated Mergin to function as the backend synchronisation and storage hub. By building a workflow around Mergin, they established a system capable of:

  1. Server-Side Change Handling: Mergin manages the complexities of data changes, working with tools like Geodiff to ensure precise change detection for vector data, including both geometry and database attributes.
  2. Data Integrity and Security: The platform provides essential server-side features such as secure storage, authentication, and authorisation to ensure data is protected and available only to approved users.
  3. User-Friendly Interface and Data Sharing: Mergin offers a centralised system that simplifies the process of sharing project data across the team.

  

This integration established a clear, repeatable workflow for both field and office staff:

  1. Data Administrator: The administrator first prepares the QGIS project on the desktop, configuring forms, survey layers, and map themes. This project is then uploaded to the Mergin platform and shared with the field users.
  2. Surveyor: Using the Input mobile application, the surveyor downloads the project from Mergin, collects and edits data in the field, and uploads the changes back to Mergin for centralised synchronisation.

  

This successful integration allows for collaborative data collection where all sources of change, whether from the mobile Input app or the desktop QGIS application, are managed seamlessly, thereby eliminating data duplication and ensuring proper version control. The project demonstrates the team's ability to connect open-source GIS components into a complete, modern enterprise solution.

  

![](/files/LRRXOqb.png)
