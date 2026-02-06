---
title: "Kartoza - Revamping Dominica's Geospatial Future: Inside the DomiNode Phase 2 Project"
description: "In a world where data can make the difference between disaster and resilience, the small island nation of Dominica is making big strides."
tags:
  - GeoNode
  - Climate Resilience
  - Disaster Management
date: 2024-09-20
author: "Eli Volschenk"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="Kartoza - Revamping Dominica's Geospatial Future: Inside the DomiNode Phase 2 Project"
    subtitle="GeoNode"
    class="is-primary"
    sub-block-side="bottom"
>}}
In a world where data can make the difference between disaster and resilience, the small island nation of Dominica is making big strides.
{{< /block >}}

## A New Era for DomiNode

The DomiNode platform, originally developed with World Bank support through the Pilot Programme for Climate Resilience, underwent significant modernization in Phase 2. The objective centered on enhancing performance, security, and data handling while ensuring users regularly adopted the platform into their workflows.

Kartoza and Piensa collaborated on this transformation. Kartoza optimized GIS components for modern standards and user-friendliness, while Piensa developed the updated GeoNode infrastructure. The team simplified DomiNode into a read-only front-end for official spatial data, employing static, cloud-optimized data stores indexed with STAC (spatio-temporal asset catalog). This approach allows government departments to manage their GIS work independently while sharing core datasets through DomiNode's object store.

## Why It Matters

For Dominica, DomiNode transcends technical infrastructure—it serves as critical infrastructure. Government departments, particularly disaster recovery teams, depend on the platform to access geospatial data essential for urban planning and emergency response. Hurricane Maria's 2017 devastation underscored the urgency for robust, resilient data-sharing systems capable of supporting disaster preparation and response.

## Breaking Down the Tech

**Key technological enhancements include:**

- **GeoNode Upgrade:** Transformed into a read-only front-end with disabled upload/editing, removed traditional backends (PostGIS, GeoServer), and integrated STAC client functionality
- **Deployment:** Implemented on NixOS for sustainable on-premise maintenance without complex DevOps requirements
- **MinIO:** S3-emulating object store ensuring data accessibility during outages
- **STAC:** Efficient data organization integrating with QGIS and ArcGIS
- **GeoParquet:** Cloud-optimized vector data storage eliminating RDBMS dependency
- **COG (Cloud-Optimised GeoTiff):** Raster data storage for DEMs, orthoimagery, satellite imagery
- **COPC (Cloud Optimised Point Cloud):** Lidar survey data storage

## Overcoming Challenges

Dominica's limited internet bandwidth and power vulnerabilities required innovative solutions. MinIO provided data redundancy, enabling access during disruptions. Local intranet access options maintained data availability when external connections failed.

## The Ripple Effect

Enhanced data-sharing capabilities empower Dominican government decision-making, particularly regarding natural disasters, supporting improved planning and response strategies that strengthen island resilience.

## Looking Ahead

Future development plans include integrating advanced tools and expanding platform functionalities to address evolving requirements.

## Acknowledgments

The project succeeded through collaboration among the Government of Dominica, World Bank, Kartoza, and Piensa teams, advancing the nation's geospatial capabilities and climate resilience.
