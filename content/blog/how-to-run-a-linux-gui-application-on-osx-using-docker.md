---
title: "How to Run a Linux GUI Application on OSX Using Docker"
description: "This guide enables running Linux GUI applications directly on macOS by utilizing Docker alongside X11 forwarding tools. The technique applies to any graphical Linux application within containerized environments."
tags:
  - Docker
  - MacOS
  - X11
  - GUI
date: 2015-05-13
author: "Gavin Fleming"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="How to Run a Linux GUI Application on OSX Using Docker"
    subtitle="Docker"
    class="is-primary"
    sub-block-side="bottom"
>}}
This guide enables running Linux GUI applications directly on macOS by utilizing Docker alongside X11 forwarding tools.
{{< /block >}}

## Overview

The article addresses running Linux GUI applications on macOS through Docker. The setup requires:

- Installing Homebrew
- Installing socat
- Installing XQuartz
- Installing Docker (via Kitematic beta)
- Obtaining a Docker image with desired GUI application
- Running the container with display forwarding

## Installation Steps

### Homebrew Installation

```bash
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

### socat Installation

```bash
brew install socat
```

XQuartz is installed from the official package. Kinematic serves as the Docker client for macOS.

### Retrieving QGIS Docker Image

```bash
docker pull kartoza/qgis-desktop
```

## Running QGIS

Four startup steps are required:

1. Start socat
2. Launch XQuartz
3. Open Kinematic
4. Run the QGIS container

### socat Command

```bash
socat TCP-LISTEN:6000,reuseaddr,fork UNIX-CLIENT:"$DISPLAY"
```

### QGIS Container Launch

```bash
docker run --rm -e DISPLAY=192.168.0.3:0 \
    -i -t -v /Users/timlinux:/home/timlinux \
    kartoza/qgis-desktop qgis
```

The article demonstrates how "QGIS (from a Linux container)" can execute on macOS desktops, with applications for testing Docker-orchestrated environments.
