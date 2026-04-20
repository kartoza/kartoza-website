---
author: Eli Volschenk
date: '2024-09-20'
description: In a world where data can make the difference between disaster and resilience,
  the small island nation of Dominica is making big strides. En
erpnext_id: /blog/geonode/revamping-dominicas-geospatial-future-inside-the-dominode-phase-2-project
erpnext_modified: '2024-09-20'
reviewedBy: Automated Check
reviewedDate: '2026-04-13'
tags:
- Geonode
thumbnail: /img/blog/erpnext/i3ktrwf.png
title: 'Revamping Dominica''s Geospatial Future: Inside the DomiNode Phase 2 Project'
---

![](/img/blog/erpnext/i3ktrwf.png)

_Dominica, officially named the Commonwealth of Dominica, is a small island nation located in the Caribbean._

  


In a world where data can make the difference between disaster and resilience, the small island nation of Dominica is making big strides. Enter the DomiNode Phase 2 project—a game-changing initiative transforming how Dominica handles and shares geospatial data. Spearheaded by the innovative teams at Kartoza and [Piensa](<https://piensa.co>), this project isn't just a technical upgrade, it's a vital enhancement for a nation dealing with the impacts of climate change and natural disasters. The objective of DomiNode is to be a central SDI (spatial data infrastructure) serving all Dominican government departments. An effective SDI facilitates spatial data and metadata storage, management and access.

  


## A New Era for DomiNode

If you've ever tried navigating a new city without a reliable map, you can appreciate how crucial good data is. For Dominica, this is even more vital. The DomiNode platform, originally developed with support from the World Bank’s Pilot Programme for Climate Resilience, was set to be overhauled in Phase 2 to tackle the challenges that emerged over the years. The goal was clear: modernise and optimise the platform to boost performance, security and data handling while ensuring users are trained and incentivised to use the platform on a regular basis, so it becomes an essential part of their daily workflow.

  


![](/img/blog/erpnext/543Demh.png)

_Lidar Map (Light Detection and Ranging Map) of Dominica, this map can be viewed on DomiNode platform._

  


Kartoza and Piensa rolled up their sleeves to tackle this task. Kartoza took charge of optimising the GIS aspects, ensuring that the data not only met modern standards but was also user-friendly. Meanwhile, Piensa focused on developing the updated GeoNode and infrastructure, creating a solid backbone for the revamped platform.

  


Although the previous incarnation of DomiNode was delivered successfully, it turned out to have some features that users didn't use or found too complex. So the objective of this phase was to simplify DomiNode into a read-only front-end for all official spatial data on the island. Our philosophy was to create static, cloud-optimised data stores that would be easy to update or overwrite from time to time, index them with STAC (spatio-temporal asset catalog) and use GeoNode purely to search, browse, preview and download data. At the same time, other STAC clients like QGIS and ArcGIS can find and pull data from the same catalog. This allows each department to continue doing their own thing with GIS as they see fit—all they need to do is drop updates of core data sets into the DomiNode object store from time to time.

![](/img/blog/erpnext/dB0AkRK.png)

## Why It Matters

So, why all the fuss about a GIS platform? For Dominica, the DomiNode is more than just a tech project—it's a lifeline. The platform helps various government departments, including disaster recovery teams, share and access vital geospatial data. This data is crucial for everything from urban planning to emergency response, especially in a country frequently hit by hurricanes and other climate-related challenges.

  


The project’s urgency was underscored by Hurricane Maria in 2017, which severely impacted Dominica's infrastructure and highlighted the need for a more robust and resilient data-sharing system. The updated DomiNode platform is designed to fill that gap, ensuring the island can better prepare for and respond to future disasters.

  


## Breaking Down the Tech

Let’s dive into what makes the updated DomiNode so impressive. The tech team didn't just update the software; they reimagined it. Here’s a glimpse at the high-tech solutions they brought on board:

  


**GeoNode Upgrade:** The core of the platform, GeoNode, was brought up to date to enhance user experience and data management. New modules were developed to turn it in a read-only front-end for cloud-optimised geospatial data. We disabled upload and editing functionality, removed the traditional data and service back-ends (PostGIS and GeoServer) and integrated a STAC client into the back-end. The DomiNode GeoNode now simply publishes whatever is in Dominica's STAC. Scheduled tasks crawl through the various static data stores and keep the STAC updated.

**Deployment** : As much as we like Kubenetes and cloud devops, this had to be a really simple on-island, on-premise implementation. So it's deployed in a NixOS environment with no devops bells and whistles, facilitating sustainable maintenance.

**MinIO:** This S3-emulating object store ensures data remains accessible even when the main platform is down—crucial for dealing with Dominica's frequent internet and power issues.

**STAC:** This tool helps organise and access data efficiently, integrating seamlessly with popular GIS tools like QGIS.

**GeoParquet:** By optimising data for the cloud, this technology improves performance and accessibility. All vector data are stored as GeoParquet files. No RDBMS!

**COG** (Cloud-optimised GeoTiff): All raster data—DEMs, orthos, satellite images—are stored as COGs

**COPC** (Cloud optimised point cloud): All point cloud data—mainly a Lidar survey of the island—are stored as COPCs

  


## Overcoming Challenges

Every project faces hurdles and DomiNode was no exception. Dominica's slower internet speeds and occasional power outages posed significant challenges. But innovation was the answer. The team implemented MinIO for data redundancy, allowing access even during outages. They also ensured that local intranet access could be utilised, keeping the data flowing even when external connections failed.

  


## The Ripple Effect

The impact of the DomiNode Phase 2 project goes beyond just technical improvements. It empowers Dominica's government to make better-informed decisions, particularly in the face of natural disasters. With enhanced data-sharing capabilities, the platform supports more effective planning and response strategies, ultimately contributing to the island’s resilience.

  


## Looking Ahead

The future looks bright for the DomiNode platform. As technology continues to advance, so too will the capabilities of Dominica’s geospatial infrastructure. Future plans include integrating even more cutting-edge tools and expanding the platform’s functionalities to meet evolving needs.

  


## Personal Reflections

While the tech team worked tirelessly to bring DomiNode to life, their journey was also marked by significant personal experiences. Two team members from South Africa travelled to Dominica to provide hands-on training, an aspect that highlighted the collaborative spirit of the project.

  


## Acknowledgments

Thank you to everyone that collaborated and a big shout-out to everyone involved in the DomiNode Phase 2 project, including the Government of Dominica, the World Bank and the dedicated teams from Kartoza and Piensa. Your hard work and innovation are paving the way for a more resilient and data-driven future for Dominica.

  


For more information on the DomiNode platform and its impact, have a closer look at [DomiNode](<http://dominode.dm>) itself.
