---
title: "Setting up a Fedora 21 QGIS Workstation"
description: "The author, a longtime Ubuntu user since version 4.10, describes his decision to transition to Fedora 21."
tags:
  - FOSSGIS
  - QGIS
  - Linux
date: 2014-12-24
author: "Gavin Fleming"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="Setting up a Fedora 21 QGIS Workstation"
    subtitle="FOSSGIS"
    class="is-primary"
    sub-block-side="bottom"
>}}
The author, a longtime Ubuntu user since version 4.10, describes his decision to transition to Fedora 21.
{{< /block >}}

## Overview

The author, a longtime Ubuntu user since version 4.10, describes his decision to transition to Fedora 21. He notes that "Ubuntu has been losing momentum" regarding support for cutting-edge Gnome desktop editions and developer workstation needs.

## Key Motivation

His primary interest involved testing QGIS performance under Wayland, the next-generation Linux graphics environment. Additionally, increased Docker usage throughout the previous year led him to conclude that the underlying Linux distribution mattered less for application deployment.

## Installation Focus

The article details setup procedures for a MacBook 13" laptop, documenting installation of:

- Docker
- QGIS compilation build chain
- PyCharm 4
- Shutter
- Skype
- QtCreator/QtDesigner
- btsync
- Google Chrome
- VLC and video codecs
- KeePassX
- Elegance Gnome theme

## Key Finding

The author reports the migration proved "fairly painless" and successfully replicated his Ubuntu application stack. However, setup complexity exceeded Ubuntu's in some cases, and he hadn't yet located binary packages for btsync-gtk-gui.

## Resource

A linked Gist provides the complete setup procedure, maintained with ongoing configuration adjustments.
