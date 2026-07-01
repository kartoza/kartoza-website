---
client: ''
date: '2025-01-16'
description: 'The REZoning tool (https://rezoning.energydata.info/ ) is an interactive,
  web-based platform designed to identify, visualise, and rank zones that are most
  suitable for the development of solar, wind, '
erpnext_id: jn1ik04sdf
erpnext_modified: '2025-07-30 18:58:08.319378'
github: ''
reviewedBy: Automated Check
reviewedDate: '2026-07-01'
services: []
tags:
- Project
technologies:
- AWS
- Javascript
thumbnail: https://erp.kartoza.com/files/2i9eMT3.png
title: REZoning (ESMAP)
---

{{< block
    title="REZoning (ESMAP)"
    subtitle="Project"
    class="is-primary"
    sub-block-side="bottom"
>}}
The REZoning tool (https://rezoning.energydata.info/ ) is an interactive, web-based platform designed to identify, visualise, and rank zones that are most suitable for the development of solar, wind, or offshore wind projects. Custom spatial filters and economic parameters can be applied to meet users needs or to represent a specific country context. The REZoning tool is powered by global geospatial datasets and uses baseline industry assumptions as default values for economic calculations.
{{< /block >}}

## Overview

The REZoning platform version 1.0 was developed and deployed by [devseed](<https://developmentseed.org/>), working in partnership with Derilinx. Kartoza was contracted to extend the platform and implement a number of additional features for a version 2.0 deployment. The application is a complex and multifaceted web application

which consumes and analyzes multiple preprocessed data stores against the criteria specified by users in the front-end, and then processes and retrieves these results to display for end users.

  

Kartoza was contracted to:

  1. **** Update the database for the REZoning platform
  2. Include the countries that were omitted in v.1.0
  3. Update the data layers for which more up-to-date information is available: e.g Land Use/ Land Cover dataset (_[https://esa-worldcover.org/en](<https://esa-worldcover.org/en>)_)
  4. Improve existing features
  5. Update the export function to include, for each zone, the resulted values after the application of each filter: wind speed interval, average distance to, etc.
  6. Only display contextual layers that have been used for filtering; remove all other contextual layers from the list
  7. Ensure that the resulted “suitable areas” are displayed only for the Area of Interest
  8. Improve EXPORT outputs, by adding more information/ additional outputs
  9. Add various other new features
  10. Update About page of the tool and the documentation to reflect the new changes

  

![](/files/2i9eMT3.png)

  

![](/files/4ryn9Hr.png)

## Technologies

- AWS
- Javascript
