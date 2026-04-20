---
author: Andre Kruger
date: '2019-10-14'
description: Every now and then there might be a dispute about which is really the
  longest river in the world. As is shown in t
erpnext_id: /blog/qgis/the-longest-river-in-the-world
erpnext_modified: '2019-10-14'
reviewedBy: Automated Check
reviewedDate: '2026-04-13'
tags:
- Qgis
thumbnail: /img/blog/erpnext/OCk8lHE.jpg
title: The Longest River in the World
---

Every now and then there might be a dispute about which is really the longest river in the world. As is shown in this National Geographic [article](<https://www.nationalgeographic.com/science/2007/06/amazon-longer-than-nile-river/>). Even Wikipedia indicates that the fact that the Nile river is accepted as the longest river in the world as "disputed".

The main contender to take the crown as the longest river in the world is of course none other than the Amazon. As romantic as the National Geographic try to make it sound I don't believe a dispute like this will be settled with an overland expidition into the jungles of Peru or a hero's adventure looking for the source of the Nile in central Africa.

A challenge like this will probably be best answered by using remote sensing. There are of course many technicalities to determining the length of a river and not one sure answer. I will tackle this challenge by using the same dataset at the same resolution.

Let me take you through the steps I took to determine the length of the rivers myself.

  1. Download the 15 second (500m) vector river datasets from <https://www.hydrosheds.org/>.
  2. Copy the shapefiles into Geopackage. I want to make use of the spatial index.
  3. Using Python and the Fiona library I extracted the basins for the Nile and the Amazon by recusively walking upstream from an identified discharge river line. This is where the built-in spatial index in Geopackage helps a lot.
  4. I also had to extend the rivers to reach the ocean. The Amazon was extended by about 255km and the Nile was extended by 3km. The enourmous size of the Amazon near the mouth of the river complicates it for remote sensing and hydrologists to display it as a normal river hierarchy.
  5. Use GRASS's  _v.net_ tool in QGIS's processing toolbox to generate nodes for the river network.
  6. Calculate the length of each river edge using the  _$length_ function in the field calculator of QGIS. The wonderful thing about this function is that it will calculate the lengths of the river segments in metres even though your data is not projected.
  7. Recusively walking upstream calculate the distance of each node from the discharge node at the ocean using Jupyter, Python and Fiona.
  8. Back in QGIS sort the node's distance from furthest to zero for the discharge. Voilá, you have the length of the river and the ID of the node.
  9. Back in Jupyter load the river network into the NetworkX library and determine the route from the furthest node to the discharge.
  10. Extract and highlight the river segments that are part of the route.



![](/img/blog/erpnext/OCk8lHE.jpg)

  


Values in brackets are from alternative sources.

**RiverWikipedia Length (km)National Geograhic Article (km)HydroSHEDS Length (km)**|   
|   
|   
  
---|---|---|---  
Nile| 6 650 km (7 088)| 6 695 km| 6 827 km  
Amazon| 6 400 km (6 992)| 6 800 km| 6 230 km  
  
I don't think the Nile will be removed from its position as the longest river in the world any time soon.

P.S. I have also calculated the Strahler order of each river segment. But that might be a topic for another blog post.
