---
title: "Installing QGIS on a Chromebook"
description: "How St Johns College in Johannesburg successfully deployed QGIS on Chromebook devices for their geography department."
tags:
  - QGIS
  - Education
  - Chromebook
  - Installation
date: 2022-05-24
author: "Gavin Fleming"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="Installing QGIS on a Chromebook"
    subtitle="QGIS"
    class="is-primary"
    sub-block-side="bottom"
>}}
How St Johns College in Johannesburg successfully deployed QGIS on Chromebook devices for their geography department.
{{< /block >}}

## Introduction

The piece describes how St Johns College in Johannesburg successfully deployed QGIS on Chromebook devices. After geography department notebooks containing QGIS were distributed during COVID lockdowns, the school sought an alternative solution using their existing Chromebook inventory.

## Context

"In 2021, all the Geography Department notebooks at St Johns College (Johannesburg), that had QGIS installed, were distributed to students during COVID lockdowns, so they were no longer available to the department."

Despite initial skepticism about Chromebooks' limited resources, the IT and geography departments proved QGIS could run effectively on these devices. Data sharing occurs through GeoPackages via Google Drive, enabling local access for users.

## Installation Steps

1. Enable Linux Development Environment (Beta) via Developers menu
2. Complete Linux setup prompts with correct username
3. Install Flatpak using: `sudo apt install flatpak`
4. Execute the installation script from OnTheLink
5. Follow menu prompts selecting Option 1 for updates and version selection
6. Confirm installation continuation and await completion
7. Close terminal upon completion

The solution demonstrates that resource-constrained devices can effectively support professional GIS applications when configured appropriately.
