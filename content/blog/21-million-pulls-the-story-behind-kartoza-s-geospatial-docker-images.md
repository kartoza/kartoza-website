---
author: Jeff Osundwa
date: '2026-08-21'
description: How a South African geospatial consultancy's Docker images became the
  backbone of open-source GIS infrastructure.
erpnext_id: /blog/docker/21-million-pulls-the-story-behind-kartozas-geospatial-docker-images
erpnext_modified: '2026-08-21'
reviewedBy: Automated Check
reviewedDate: '2026-08-12'
tags:
- Docker
thumbnail: /img/blog/erpnext/21-million-pulls.png
title: '21 Million Pulls: The Story Behind Kartoza''s Geospatial Docker Images'
---

![Hero image](/img/blog/erpnext/21-million-pulls.png)

If you have ever spun up a PostGIS database or deployed GeoServer in a container, there is a good chance you pulled an image built by Kartoza. As of mid-2026, our geospatial Docker images have been pulled over **21 million times** on Docker Hub. That number quietly astonishes even us. We are a small team based in Cape Town and Stellenbosch, yet our containers sit in CI pipelines, university labs, government servers, and humanitarian deployments on every continent.

This post tells the story of how that happened, what the images look like today, and what it takes to keep them running.

## How It Started

In 2014, Docker was still finding its footing and nobody in the geospatial world was shipping production containers. Tim Sutton, Kartoza co-founder, built the first `kartoza/qgis-desktop` image out of a practical need: running QGIS inside a container for testing plugins and automating workflows. Shortly after came `kartoza/postgis`, a PostGIS image that handled the tedious parts of database setup so teams could focus on spatial work instead of sysadmin chores.

These were not built as products. They were built because Kartoza needed them internally, and sharing them openly felt like the right thing to do in a community that had given us QGIS, PostGIS, and GeoServer for free. Over a decade later, that small act of sharing has become infrastructure.

## The Images Today

![Flow diagram](/img/blog/erpnext/21-million-pulls-docker-flow.png)

Kartoza now maintains seven Docker images, each targeting a different piece of the geospatial stack:

Image | Pulls | What it does  
---|---|---  
[PostGIS](<https://hub.docker.com/r/kartoza/postgis>) | 21M+ | Production-ready PostgreSQL with PostGIS, replication, and backup support  
[GeoServer](<https://hub.docker.com/r/kartoza/geoserver>) | 5.6M+ | OGC-compliant map server with clustering, GeoFence, and extensions  
[Docker OSM](<https://hub.docker.com/r/kartoza/docker-osm>) | 300K+ | Local OpenStreetMap mirror with automatic updates into PostGIS  
[MapProxy](<https://hub.docker.com/r/kartoza/mapproxy>) | 292K+ | Tile caching and proxying for accelerating map services  
[PG Backup](<https://hub.docker.com/r/kartoza/pg-backup>) | 262K+ | Automated PostgreSQL backups with S3, SFTP, and local storage  
[QGIS Server](<https://hub.docker.com/r/kartoza/qgis-server>) | 40K+ | Publish QGIS projects as OGC web services with pixel-perfect rendering  
[QGIS Desktop](<https://hub.docker.com/r/kartoza/qgis-desktop>) | 19K+ | Containerised QGIS for CI/CD, plugin testing, and headless processing  
  
Together they cover the full lifecycle: store spatial data in PostGIS, serve it through GeoServer or QGIS Server, cache tiles with MapProxy, mirror OpenStreetMap with Docker OSM, and back it all up with PG Backup. Every image is open source and hosted on [GitHub](<https://github.com/kartoza/>).

## What Makes Them Production-ready

There are plenty of Docker images that wrap a piece of software and call it a day. Kartoza's images go further because they were shaped by years of real deployments, not hypothetical use cases.

**Version Tracking.** When PostgreSQL 16 ships, or GeoServer releases a new stable version, the images follow. We maintain multiple version tags so teams can pin to a known-good release or track the latest.

**Environment-variable Configuration.** No need to bake custom images for basic setup. Database credentials, SSL toggles, replication settings, extension lists, and GeoServer clustering are all controlled through environment variables. A `docker-compose.yml` and a `.env` file is usually all you need.

**Operational Essentials Built In.** Health checks, SSL/TLS support, automated backup scheduling, and CORS configuration come pre-wired. These are the things that separate a demo container from something you would put behind a load balancer in production.

**Docker Compose Ready.** Every image ships with documented Compose examples showing how to wire the stack together. PostGIS talks to GeoServer, GeoServer talks to MapProxy, and PG Backup watches the database, all in a single `docker-compose up -d`.

## Who Uses Them?

The pull count tells part of the story, but the diversity of users is what makes it interesting.

Kartoza's own [geospatial hosting platform](<https://kartoza.com/blog/geospatial-hosting-taking-the-pain-out-of-hosting-your-gis-applications/>) runs on these images. We migrated from around 70 hand-managed servers to a Kubernetes-based infrastructure built on the same containers we publish publicly. Our hosting customers get the benefit of images that we use and trust ourselves.

Beyond that, the images show up in places we sometimes only learn about after the fact: university GIS courses where students need a local PostGIS instance in minutes, humanitarian organisations deploying GeoServer in field offices with limited connectivity, startups building location-based services who do not want to manage database infrastructure, and CI/CD pipelines where teams run spatial tests against a disposable PostGIS container on every pull request.

The [Docker OSM image](<https://kartoza.com/blog/creating-a-live-topic-specific-mirror-of-openstreetmap-in-postgis/>) in particular has found a niche with teams who need a local, continuously updated mirror of OpenStreetMap data without relying on external APIs.

## The Maintenance Burden

Open source infrastructure does not maintain itself. Every upstream release means updating Dockerfiles, testing compatibility, fixing breakages, and publishing new tags. Security advisories on base images or bundled libraries need prompt attention. Community issues and pull requests on GitHub need triage and review.

This work is funded through Kartoza's consulting and training revenue. There is no grant, no sponsorship line item, no paywall on the images. We absorb the maintenance cost because the ecosystem has given us far more than we give back, and because healthy infrastructure makes our own work easier. That said, every star, issue report, and pull request on GitHub helps. If you use these images, [starring the repositories](<https://github.com/kartoza/>) and filing issues when you find problems genuinely makes a difference.

## Getting Started

If you are new to the images, the quickest way in:

    docker pull kartoza/postgis:16-3.4

Browse all images on [Docker Hub](<https://hub.docker.com/search?q=kartoza>) or visit our [Docker images page](<https://kartoza.com/docker/>) for documentation, quick-start guides, and Compose examples for each image.

If your team needs to go deeper, our [Enterprise GIS training course](<https://kartoza.com/training-courses/enterprise-gis/>) covers the full PostGIS, GeoServer, and QGIS Server stack in a hands-on, five-day format. And if you would rather skip the self-hosting entirely, our [managed hosting service](<https://kartoza.com/hosting/>) deploys these same images with backups, monitoring, and support included.

QGIS is a community effort, and so is the infrastructure around it. These images exist because people built, tested, reported bugs, and contributed back. Twenty-one million pulls later, the community is very much alive. Install one today and let us know how it goes.
