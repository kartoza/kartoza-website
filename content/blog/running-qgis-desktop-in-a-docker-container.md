---
title: "Running QGIS Desktop in a Docker Container"
description: "An exploration of containerizing QGIS Desktop using Docker, outlining advantages, limitations, and implementation steps."
tags:
  - QGIS
  - Docker
  - Container
date: 2014-07-16
author: "Gavin Fleming"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="Running QGIS Desktop in a Docker Container"
    subtitle="QGIS"
    class="is-primary"
    sub-block-side="bottom"
>}}
An exploration of containerizing QGIS Desktop using Docker, outlining advantages, limitations, and implementation steps.
{{< /block >}}

## Introduction

The author expresses enthusiasm for Docker technology, noting he has followed its development since its announcement. He and Richard Duivenvoorde experimented with containerizing QGIS Desktop, achieving a working setup in approximately 30 minutes.

## Why Use QGIS in Docker?

The piece outlines seven key advantages:

### 1. Application Sandboxing

Isolating QGIS prevents interference with other applications and allows precise resource allocation.

### 2. OS Flexibility

Users on CentOS or Arch Linux can leverage Ubuntu packages without replacing their operating system.

### 3. Multiple Versions

Different QGIS versions can run simultaneously in separate containers, eliminating complex path configurations.

### 4. Profile Variation

Custom plugin configurations can be maintained across different Docker images for different workflows.

### 5. Stable Deployment

A containerized setup remains unaffected by host system upgrades, simplifying enterprise distribution.

### 6. Packaged Distribution

Similar to Windows installers, well-configured Docker images can be shared and deployed reliably.

### 7. Clean Testing Environments

Containers can be destroyed and recreated for reproducible testing.

## Limitations Acknowledged

- Added learning complexity with Docker integration
- Containers lack persistence; plugins disappear after shutdown (though Docker volumes address this)
- Potential performance overhead concerns, though testing revealed negligible differences

## Setup Instructions

Installation requires:

- Docker installation via `sudo apt-get install docker.io`
- Cloning the GitHub repository containing the Dockerfile
- Running the build script to generate the `kartoza/qgis-desktop` image

The process automatically creates a desktop launcher, adds a PATH entry to `.bashrc`, and places a `.desktop` shortcut in the applications menu.

## Implementation Details

When launched, the script starts a new container, mounts the home directory, and displays QGIS on the desktop as a native application.

### Known Issues

- QGIS runs as root, potentially corrupting file permissions
- Uses `xhost +` for display access, raising security considerations for some users
- Only home folder access available; other host directories remain inaccessible

## Future Development

The roadmap includes adding support for OrtheoToolBox, SAGA, GRASS, MMQGIS, MrSid, ECW, and ESRI FGDB to create a "batteries included" distribution. Community contributions via pull requests are welcomed.
