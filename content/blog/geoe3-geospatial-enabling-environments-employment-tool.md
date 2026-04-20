---
title: "GEOE3: Geospatial Enabling Environments for Employment Spatial Tool"
description: "A powerful QGIS plugin that analyses spatial barriers to women's employment and business opportunities, helping policymakers create more inclusive workplaces."
tags:
  - QGIS
  - Plugin
  - Gender
  - Spatial Analysis
date: 2024-03-23
author: "Jeff Osundwa"
thumbnail: "/blog/img/geoe3-banner.png"
reviewedBy: "Jeff Osundwa"
reviewedDate: "2026-03-23"
---

{{< block
    title="GEOE3: Geospatial Enabling Environments for Employment Spatial Tool"
    subtitle="QGIS Plugin"
    class="is-primary"
    sub-block-side="bottom"
 >}}
GEOE3 (formerly GEEST) is a powerful open-source spatial mapping tool developed by the World Bank that enables comprehensive analysis of how various spatial factors influence women's employment and business opportunities.
{{< /block >}}

## Overview

**GEOE3 (Geospatial Enabling Environments for Employment Spatial Tool)** is a user-friendly QGIS plugin that analyses how spatial factors influence women's economic participation across regions. Originally developed by the World Bank and Kartoza under the name GEEST, GEOE3 provides a comprehensive framework for gender-informed spatial analysis.

The tool helps identify key areas for intervention and enables data-driven decisions toward creating more equitable job opportunities for women across different regions.

## Key Features

GEOE3 analyses **15 spatially varying factors** across three key dimensions, each scored on a 0-5 scale:

### Contextual Factors

The Contextual Dimension refers to laws and policies that shape workplace gender discrimination, financial autonomy, and gender empowerment:

- **Workplace Discrimination** - Laws addressing gender biases that hinder women's career advancement, using the WBL 2024 Workplace Index
- **Regulatory Frameworks** - Laws protecting women's employment rights, childcare support, and parental leave (WBL Pay & Parenthood Index)
- **Financial Inclusion** - Laws concerning women's access to financial resources for starting businesses (WBL Entrepreneurship Index)

### Accessibility Factors

The Accessibility Dimension evaluates women's daily mobility and access to essential services using OpenStreetMap data:

- **Women's Travel Patterns** - Access to everyday services (kindergartens, primary schools, groceries, pharmacies, green spaces) with 5 subfactors
- **Access to Public Transport** - Proximity to bus stops, train stations, and other transport facilities
- **Access to Health Facilities** - Distance to clinics, hospitals, and healthcare services
- **Access to Education and Training Facilities** - Proximity to universities and technical training centres
- **Access to Financial Facilities** - Distance to banks and financial institutions

### Place Characterisation

The Place Characterisation Dimension refers to the social, environmental, and infrastructural attributes of locations:

- **Active Transport** - Walkability and cycling infrastructure
- **Safety** - Perceived public safety based on street lighting and nighttime illumination
- **FCV (Fragility, Conflict & Violence)** - Analysis of conflict and political instability using ACLED data
- **Education** - Proportion of women with higher education attainment
- **Digital Inclusion** - Availability of digital infrastructure and internet access
- **Environmental Hazards** - Vulnerability to natural disasters (floods, droughts, landslides, fires, tropical cyclones)
- **Water Sanitation** - Access to clean water and sanitation facilities

All factors can be weighted according to local context, and results can be exported for further analysis in QGIS or other GIS software.

## Installation

Installing GEOE3 in QGIS is straightforward:

1. Open QGIS on your computer
2. Navigate to **Plugins** → **Manage and Install Plugins**
3. Search for "GEOE3" or "Geospatial Enabling Environments"
4. Click **Install Plugin**
5. Once installed, access GEOE3 from the **Plugins** menu or toolbar

The plugin is also available on GitHub for manual installation or development purposes.

## Use Cases

### Urban Planning

GEOE3 enables urban planners to identify and address spatial barriers to women's economic participation by mapping infrastructure gaps, service accessibility, and transportation networks.

### Regional Development

GEOE3 helps regional development agencies target resources for gender-equitable growth by identifying areas with the greatest potential for women's economic empowerment.

### Research and Policy Making

Researchers and policymakers can leverage GEOE3's analytical capabilities to inform gender-responsive policies and track progress toward gender equality goals.

## Conclusion

GEOE3 is a game-changer for gender-aware geospatial analysis. By making spatial data accessible and actionable, it empowers decision-makers to build more inclusive communities and workplaces.

For more information, visit the [official documentation](https://worldbank.github.io/GEOE3/) or contribute to the project on [GitHub](https://github.com/worldbank/GEOE3).
