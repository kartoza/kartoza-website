---
client: ''
date: '2025-01-15'
description: 'For ease of deployment Kartoza maintains pre-built, auto-updating images
  on Docker Hub. When there

  is a change in the Docker code in the tracked GitHub repositories, Docker Hub picks
  them up

  and updat'
erpnext_id: p4td9oq1ol
erpnext_modified: '2026-06-04 14:30:15.530750'
github: ''
reviewedBy: Automated Check
reviewedDate: '2026-06-19'
services: []
tags:
- Project
technologies:
- Docker
thumbnail: https://erp.kartoza.com/files/C3HzwGI.png
title: KARTOZA DOCKER HUB
---

{{< block
    title="KARTOZA DOCKER HUB"
    subtitle="Project"
    class="is-primary"
    sub-block-side="bottom"
>}}
For ease of deployment Kartoza maintains pre-built, auto-updating images on Docker Hub. When there
is a change in the Docker code in the tracked GitHub repositories, Docker Hub picks them up
and updates the images.
{{< /block >}}

## Overview

Our preferred means of packaging and deploying systems is with Docker containers. To this end we maintain several of our own repositories or modified forks of other repositories. These repositories contain the Dockerfiles and the related configuration components required to build each Docker image. You can browse our published docker images here. Our more popular images (namely, our PostGIS and GeoServer images) have been downloaded millions of times!

  

When there is a change in the Docker code in the GitHub repositories listed [here](<https://hub.docker.com/search?q=kartoza>), Docker Hub picks them up and updates the images.

  

![](https://kartoza.com/files/C3HzwGI.png)

## Technologies

- Docker
