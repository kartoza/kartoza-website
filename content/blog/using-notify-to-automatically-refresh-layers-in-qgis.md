---
title: "Using NOTIFY to Automatically Refresh Layers in QGIS"
description: "This piece explores a powerful but underutilized QGIS feature that enables automatic layer refreshes triggered by PostgreSQL notifications."
tags:
  - PostGIS
  - QGIS
  - PostgreSQL
  - NOTIFY
date: 2019-04-01
author: "Tim Sutton"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="Using NOTIFY to Automatically Refresh Layers in QGIS"
    subtitle="PostGIS"
    class="is-primary"
    sub-block-side="bottom"
>}}
This piece explores a powerful but underutilized QGIS feature that enables automatic layer refreshes triggered by PostgreSQL notifications.
{{< /block >}}

## Content

This piece explores a powerful but underutilized QGIS feature developed by Oslandia that enables automatic layer refreshes triggered by PostgreSQL notifications. The capability became available in QGIS version 3.0.

## Core Concept

The article demonstrates implementing PostgreSQL NOTIFY functionality to automatically update QGIS layers when database changes occur, eliminating manual refresh requirements.

## Implementation Steps

### 1. Create a notification function

Create a function that sends NOTIFY signals to QGIS:

- Uses PL/pgSQL language
- Returns trigger type
- Executes NOTIFY qgis command

### 2. Add database triggers

Add database triggers on INSERT, UPDATE, or DELETE events to invoke the notification function.

### 3. Enable layer settings

Check the "refresh layer on notification" option in QGIS layer properties.

## Practical Application

Users can leave QGIS open and observe new features from other machines automatically displaying without manual intervention.

## Related Resources

The author references Oslandia's detailed documentation covering implementation specifics and triggering custom actions via NOTIFY signals.
