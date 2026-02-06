---
title: "Setting up Geogig in a Production Environment"
description: "The piece addresses a long-standing need in geospatial work: versioning spatial data."
tags:
  - Docker
  - GeoGig
  - PostGIS
  - GeoServer
date: 2018-06-25
author: "Admire Nyakudya"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="Setting up Geogig in a Production Environment"
    subtitle="Docker"
    class="is-primary"
    sub-block-side="bottom"
>}}
The piece addresses a long-standing need in geospatial work: versioning spatial data.
{{< /block >}}

## Introduction

The piece addresses a long-standing need in geospatial work: "versioning spatial data." LocationTech's GeoGig tool, which originated as geogit, enables this capability with seamless GeoServer integration. The author notes that Kartoza employs Docker for service orchestration, which forms the foundation of their technical approach.

## Core Concept

GeoGig borrows its fundamental operations from Git's code-versioning methodology, applying these principles to geographic datasets.

## Implementation Steps

### Repository Setup

The guide directs users to clone the docker-geogig repository and launch services using docker-compose.

### Docker Configuration

The provided docker-compose.yml file orchestrates three services:
- PostgreSQL/PostGIS database (version 9.5-2.2)
- GeoServer instance (version 2.13.0)
- GeoGig service (version 1.2.0 with DATABASE backend)

### Data Import

After containers initialize, users import spatial data from PostGIS into GeoGig's version control system using pg import functionality.

### Version Control Operations

Changes are tracked through standard add and commit workflows, with modifications stored in PostgreSQL's backend storage.

### Remote Access

The setup enables serving versioned data through GeoServer over HTTP, allowing network-based operations like cloning, pushing, and pulling—useful for distributed team workflows.
