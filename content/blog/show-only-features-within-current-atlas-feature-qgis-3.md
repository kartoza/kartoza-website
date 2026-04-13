---
author: Admire Nyakudya
date: '2019-05-15'
description: In our endless endeavour to spread QGIS, I was invited to conduct QGIS
  training at the Surveyor General Department in Swaziland.
erpnext_id: /blog/qgis/show-only-features-within-current-atlas-feature-qgis-3
erpnext_modified: '2019-05-15'
reviewedBy: Automated Check
reviewedDate: '2026-04-13'
tags:
- Qgis
thumbnail: /img/blog/erpnext/intersects.png
title: Show Only Features Within Current Atlas Feature - QGIS 3
---

In our endless endeavour to spread QGIS, I was invited to conduct QGIS training at the [Surveyor General Department](<http://www.gov.sz/index.php/ministries-departments/ministry-of-natural-resources/surveyor-general>) in Swaziland.

Whilst teaching about map composer and atlas we wanted to show features that are within a polygon extent. A quick google search showed us that this had been answered by [Underdark](<https://gis.stackexchange.com/questions/260392/show-only-features-within-current-atlas-feature>) but her answer included showing intersecting features. In our case, we only wanted to show features that were within a polygon. 

I initially tried to use the solution that had been suggested by Underdark but the results were unsatisfactory. After trying the Underdark solution I could get the following result:

![Layer Intersects](/img/blog/erpnext/intersects.png)

Then I thought I could just do an intersection between the Atlas geometry and the feature geometry I wanted. This solution does not work because QGIS returns a geometry collection and apparently QGIS cannot handle it properly.

The solution I finally came up with included the earlier solution from Underdark.

`CASE`  
` WHEN within( $geometry , @atlas_geometry ) = 1 THEN intersects( $geometry , @atlas_geometry )`  
`ELSE NULL`  
`END`

The result I get is satisfactory but I would still prefer if I could use an intersection so that I can get the part of the polygon that intersects the poly rather than excluding it.

![Layer within](/img/blog/erpnext/within.png)
