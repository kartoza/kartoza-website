---
title: "QGIS Road to Nerdvana Episode 2: QGIS QtCreator Build on Pop_OS! 20.04"
description: "Tim Sutton demonstrates how to use QtCreator to build QGIS within a graphical development environment."
tags:
  - QGIS
  - Development
  - QtCreator
date: 2020-10-16
author: "Seabilwe Tilodi"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="QGIS Road to Nerdvana Episode 2"
    subtitle="QGIS"
    class="is-primary"
    sub-block-side="bottom"
>}}
Tim Sutton demonstrates how to use QtCreator to build QGIS within a graphical development environment.
{{< /block >}}

## Overview

Tim Sutton demonstrates how to use QtCreator to build QGIS within a graphical development environment. The tutorial focuses on establishing 3D support capabilities.

## Installation Command

```bash
sudo apt install qtcreator
```

## CMake Configuration

```
Qt53DExtras_DIR /home/timlinux/dev/cpp/QGIS/external/qt3dextra-headers/cmake/Qt53DExtras
```

## Kit Management Settings

```
QT5_3DEXTRA_INCLUDE_DIR=/home/timlinux/dev/cpp/QGIS/external/qt3dextra-headers
QT5_3DEXTRA_LIBRARY=/usr/lib/x86_64-linux-gnu/libQt53DExtras.so
```

**Important Note:** Paths require adjustment to match local code repository locations.

## Dependency Resolution

Two error dialogs (missing pywebkit and jinja2) are resolved through:

```bash
sudo apt install python3-jinja2
sudo apt-get -y install python3-pyqt5.qtwebkit libqt5webkit5-dev
```

The article references "Episode 2 of our road to Nerdvana" available on YouTube for full video demonstration.
