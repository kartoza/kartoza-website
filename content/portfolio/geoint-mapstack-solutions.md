---
client: ''
date: '2025-01-17'
description: 'This project was done to help enhance MapStack''s scalability for enterprise
  clients, improve its user interface and experience, and streamline deployment and
  content generation workflows.

  '
erpnext_id: 8g4k50rlbv
erpnext_modified: '2026-06-04 14:38:38.901399'
github: https://github.com/kartoza/MapSTACK-2.1
reviewedBy: Automated Check
reviewedDate: '2026-06-19'
services: []
tags:
- Project
technologies: []
thumbnail: https://erp.kartoza.com/files/mapstack_dashboard.png
title: GeoInt MapStack Solutions
---

{{< block
    title="GeoInt MapStack Solutions"
    subtitle="Project"
    class="is-primary"
    sub-block-side="bottom"
>}}
This project was done to help enhance MapStack's scalability for enterprise clients, improve its user interface and experience, and streamline deployment and content generation workflows.

{{< /block >}}

## Overview

This project focused on two key areas for MapStack: foundational improvements for enterprise readiness and a comprehensive UI/UX overhaul. The technical scope included transitioning to a horizontally scalable architecture with independent, organisation-partitioned instances managed by Nginx sidecar proxies. This allows for simplified integration within diverse enterprise infrastructures, addressing challenges with existing load balancers and firewalls. Furthermore, the project aims to automate templated analytics workflows, streamline deployment with Ansible and Docker Compose, and explore data sharing via foreign data wrappers in Geoserver. Concurrently, a significant effort is dedicated to refreshing the user interface and user experience, encompassing a login page revamp, a complete theme redesign, and updates to the navigation for maps, geostories, and dashboards. The project also investigates migrating charting and dashboard functionalities from MapStore to Superset for improved visualisation capabilities and adding PDF generation for GeoStories.  

  

**Key Components & Deliverables:**

  1. **Enterprise Scalability:**
  2. Design and implement a horizontally scalable architecture with organisation-partitioned MapStack instances.
  3. Integrate Nginx sidecar proxies for unified ingress management and simplified integration with enterprise infrastructure.
  4. Automate deployment processes using Ansible and Docker Compose.
  5. Implement data isolation between organisations, potentially leveraging foreign data wrappers for shared Geoserver layers.
  6. Prioritise removal of HTTPS dependency for easier firewall navigation within enterprise environments.
  7. **UI/UX Revitalisation:**
  8. Revamp the MapStack login page user interface.
  9. Execute a comprehensive UI/UX theme redesign.
  10. Update navigation for maps, geostories, and dashboards to improve user flow and discoverability.
  11. Evaluate and potentially migrate charting and dashboard capabilities from MapStore to Apache Superset for enhanced visualisation.
  12. **Automated Workflows:**
  13. Develop templated analytics workflows, encompassing data ingest/ETL, analytics processing, layer publication via Geoserver API, and templated map/dashboard generation via MapStore/Superset APIs.
  14. Introduce PDF generation functionality for GeoStories.
  15. **Infrastructure & Costing:**
  16. Develop detailed costing for "MapStack Improvements" and "MapStack UI/UX" projects, itemising staff hours for Senior, Developer, and UI/UX Designer roles, and including project management and hosting expenses.
  17. Adopt a phased deployment approach with dedicated testing and quality assurance stages.

**Technologies & Methodologies:**

  1. **Backend/GIS:** MapStore, GeoServer, PostgreSQL, Docker Compose, Ansible, Nginx
  2. **Frontend/UI:** (Implicitly JavaScript frameworks for UI, specific ones not named)
  3. **Analytics:** Apache Superset (potential migration target)
  4. **PDF Generation:** Gotenberg (Go container)
  5. **Project Management:** Agile approach with phased deliverables and cost estimations in time buckets.

**Impact & Benefits:**

  1. **Expanded Market Reach:** Positions MapStack for robust adoption within enterprise environments by addressing critical scalability, security, and integration requirements.
  2. **Enhanced User Engagement:** A modern and intuitive UI/UX will improve user satisfaction and increase the overall usability of the platform.
  3. **Increased Efficiency:** Automated analytics and streamlined deployment processes will reduce manual effort, accelerating content generation and client onboarding.
  4. **Improved Data Management:** Strategic data sharing and isolation methods will ensure secure and flexible data handling for multi-tenant environments.

  

![](https://kartoza.com/files/Dojk4KO.png)

## Source Code

[GitHub](https://github.com/kartoza/MapSTACK-2.1)
