---
client: ''
date: '2025-01-16'
description: This project saw Kartoza partnering with Envirovision to fortify the
  technical foundation of their geospatial platform.
erpnext_id: kqkcjrivm9
erpnext_modified: '2026-06-04 14:33:04.258476'
github: https://github.com/kartoza/EVS
reviewedBy: Automated Check
reviewedDate: '2026-06-19'
services: []
tags:
- Project
technologies: []
thumbnail: https://erp.kartoza.com/files/EnviroVision.png
title: EnviroVision
---

{{< block
    title="EnviroVision"
    subtitle="Project"
    class="is-primary"
    sub-block-side="bottom"
>}}
This project saw Kartoza partnering with Envirovision to fortify the technical foundation of their geospatial platform.
{{< /block >}}

## Overview

Envirovision sought best-practice assistance in setting up its GeoNode infrastructure and needed robust documentation to ensure the long-term sustainability and operability of the system.

Kartoza’s involvement was a comprehensive effort to stabilise, modernise, and secure the platform, turning an existing codebase into a production-ready, easily managed system.

  1. Infrastructure Modernisation & Migration: The application was migrated to run efficiently within a single Docker instance, simplifying deployment and maintenance. The implementation included a customised GeoServer tuned for production use.
  2. Data Security and Redundancy: A crucial component was setting up automated backup and restore capabilities for the PostgreSQL database, which is vital to the application’s functionality. This was achieved by integrating specialised containers (`kartoza/postgis` and `kartoza/pg-backup`) into the system's orchestration.
  3. Integrated Authentication: Kartoza successfully integrated the GeoServer and GeoNode applications with Keycloak for streamlined and secure user authentication.
  4. Documentation and Best Practices: The team ensured the project was fully documented, providing clear guidance on how to set up and run the application, which enables Envirovision to manage and scale the platform effectively moving forward.

The foundational work on the original EnviroVision project led to further collaborative efforts, including integration projects like EnviroVision Map Integration with FireWeb. This initiative to create a stable, modern, and secure geospatial infrastructure has positioned Envirovision for continued growth and innovation within the environmental monitoring sector.

![](/files/EnviroVision2.png)

## Source Code

[GitHub](https://github.com/kartoza/EVS)
