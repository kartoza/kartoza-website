---
title: "The Kartoza Intern's Journey Creating a Field Survey with QGIS, Mergin and Input"
description: "Input represents a free and open-source application that extends QGIS capabilities to portable devices for fieldwork data gathering."
tags:
  - QGIS
  - Mergin
  - Input
  - Field Survey
  - FOSSGIS
date: 2021-05-17
author: "Amy Ternent"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="The Kartoza Intern's Journey Creating a Field Survey with QGIS, Mergin and Input"
    subtitle="QGIS"
    class="is-primary"
    sub-block-side="bottom"
>}}
Input represents a free and open-source application that extends QGIS capabilities to portable devices for fieldwork data gathering.
{{< /block >}}

## Introduction

Input represents a free and open-source application developed by Lutra Consulting that extends QGIS capabilities to portable devices for fieldwork data gathering. The Kartoza intern cohort undertook a practical challenge to master Input by designing a parks survey encompassing pathways, vegetation, and built infrastructure.

## Workflow Structure

The system operates through three interconnected components: Input (mobile field collection), Mergin (cloud synchronization and storage), and QGIS (desktop processing). Input functions as a mobile counterpart to QGIS, available at no cost for Android and iOS platforms.

## Getting Started with Mergin

Team members registered accounts on the Mergin cloud platform, which facilitates geospatial data administration and synchronization across devices. The Mergin plugin integrates directly into QGIS, enabling project creation, deletion, and data synchronization without leaving the desktop environment.

## QGIS Project Development

Creating a fieldwork project begins with establishing contextual framework through basemap layers. The team selected OpenStreetMap for urban context and added Google satellite and street-level imagery. For offline functionality, mapping services must be converted to MBTiles format.

## Data Schema and Layer Organization

Before implementing collection mechanisms, establishing clear data structure proves essential. The team discovered that organizing information into separate layers by category—rather than combining related data into single layers—improves efficiency and usability. Attribute fields define what information gets captured during surveys.

## Form Design

The Attributes Form tab contains a drag-and-drop interface for creating data entry workflows. Special functions include:

- `@mergin_username` automatically populates the data collector's identity
- `$now` generates automatic timestamps
- Value maps allow dropdown selections from predetermined options
- Constraints can enforce required fields

## Completing and Uploading Projects

Layer organization requires sequencing elements logically—points above lines, lines above polygons. Map themes separate online and offline basemap configurations. The Mergin plugin's browser panel facilitates uploading completed projects to the cloud infrastructure.

## Mobile Data Collection with Input

After downloading Input from app stores and logging in with Mergin credentials, users access projects through the projects tab. The More menu provides access to layer browsing, theme switching, and configuration options. Record buttons activate geometry collection tools, with GPS accuracy indicated by pointer color changes. Completed surveys synchronize back to the cloud when online connectivity resumes.

## Applications Beyond Parks

This workflow accommodates diverse geospatial applications—land tenure documentation, invasive species tracking, and large-scale multi-user initiatives all leverage the Input system's fundamental capabilities for location-based data capture.
