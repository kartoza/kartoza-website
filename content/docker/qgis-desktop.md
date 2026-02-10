---
title: "QGIS Desktop"
description: "Dockerised QGIS Desktop application for running QGIS in containerized environments."
thumbnail: "/img/docker/qgis-desktop.png"
dockerhub: "https://hub.docker.com/r/kartoza/qgis-desktop"
github: "https://github.com/kartoza/docker-qgis-desktop"
pulls: "19K+"
stars: 16
tags:
  - Desktop
  - QGIS
  - Development
upstream:
  name: "QGIS"
  url: "https://qgis.org/"
  description: "QGIS is a free and open-source cross-platform desktop geographic information system application."
date: 2024-01-07
weight: 7
---

## Overview

The Kartoza QGIS Desktop Docker image provides a containerized QGIS application that can be run on any Docker-enabled system. It's particularly useful for CI/CD pipelines, automated testing, plugin development, and running QGIS in headless mode.

## Features

- **Full QGIS Desktop** - Complete QGIS installation with all features
- **X11 forwarding** - Display QGIS GUI on your host system
- **Headless mode** - Run processing scripts without GUI
- **Plugin testing** - Ideal for QGIS plugin CI/CD
- **Consistent environment** - Same QGIS version across team
- **Multiple versions** - LTR and latest releases available

## Quick Start

### Run with GUI (X11 Forwarding)

```bash
# Allow local X connections
xhost +local:

# Run QGIS with display
docker run -it --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v $(pwd):/data \
  kartoza/qgis-desktop:3.34
```

### Run Headless (Processing)

```bash
docker run --rm \
  -v $(pwd):/data \
  kartoza/qgis-desktop:3.34 \
  qgis_process run native:buffer \
  --input=/data/input.shp \
  --distance=100 \
  --output=/data/output.shp
```

### Docker Compose

```yaml
version: '3.8'
services:
  qgis:
    image: kartoza/qgis-desktop:3.34
    environment:
      - DISPLAY=${DISPLAY}
    volumes:
      - /tmp/.X11-unix:/tmp/.X11-unix
      - ./projects:/data
      - qgis_config:/root/.local/share/QGIS
    network_mode: host

volumes:
  qgis_config:
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DISPLAY` | X11 display server | `:0` |
| `QT_X11_NO_MITSHM` | Fix for some X11 issues | `1` |
| `QGIS_PREFIX_PATH` | QGIS installation prefix | `/usr` |
| `PYTHONPATH` | Python module paths | - |

## Use Cases

### Plugin Development

```bash
# Mount plugin directory and run QGIS
docker run -it --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v ./my_plugin:/root/.local/share/QGIS/QGIS3/profiles/default/python/plugins/my_plugin \
  kartoza/qgis-desktop:3.34
```

### Automated Testing (CI/CD)

```yaml
# .github/workflows/test.yml
jobs:
  test:
    runs-on: ubuntu-latest
    container:
      image: kartoza/qgis-desktop:3.34
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: |
          xvfb-run pytest tests/
```

### Batch Processing

```bash
# Process multiple files
docker run --rm \
  -v $(pwd):/data \
  kartoza/qgis-desktop:3.34 \
  bash -c 'for f in /data/*.shp; do
    qgis_process run native:buffer \
      --input="$f" \
      --distance=50 \
      --output="/data/buffered_$(basename $f)"
  done'
```

### Python Scripting

```bash
docker run --rm \
  -v $(pwd):/data \
  kartoza/qgis-desktop:3.34 \
  python3 -c "
from qgis.core import QgsApplication, QgsVectorLayer
QgsApplication.setPrefixPath('/usr', True)
qgs = QgsApplication([], False)
qgs.initQgis()
layer = QgsVectorLayer('/data/input.shp', 'test', 'ogr')
print(f'Feature count: {layer.featureCount()}')
qgs.exitQgis()
"
```

## Available Tags

- `3.34` - QGIS 3.34 LTR (recommended)
- `3.36` - QGIS 3.36 latest
- `ltr` - Current Long Term Release
- `latest` - Newest QGIS release

## Upstream Project

This image packages [QGIS](https://qgis.org/), the free and open-source cross-platform desktop geographic information system.

We gratefully acknowledge the QGIS project, the Open Source Geospatial Foundation (OSGeo), and the thousands of contributors who make QGIS possible.
