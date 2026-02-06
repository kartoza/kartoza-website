---
title: "How To Create a QGIS PDF Report with a Few Lines Of Python"
description: "The piece addresses automating report generation to capture current data states."
tags:
  - FOSSGIS
  - QGIS
  - Python
date: 2015-03-01
author: "Gavin Fleming"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="How To Create a QGIS PDF Report with a Few Lines Of Python"
    subtitle="FOSSGIS"
    class="is-primary"
    sub-block-side="bottom"
>}}
The piece addresses automating report generation to capture current data states.
{{< /block >}}

## Introduction

The piece addresses automating report generation to capture current data states. A practical use case mentioned involves "capturing spatial data into a PostGIS database and want a snapshot of that every few hours expressed as a pdf report."

## Core Concept

The tutorial demonstrates generating PDFs by leveraging a QGIS project file (.qgs) combined with a QGIS layout template (.qpt file).

## Code Implementation

The author provides a Python script that:
- Initializes a QGIS application instance
- Loads a project from a specified path
- Reads template content from a .qpt file
- Creates a QgsComposition object from the template
- Implements string substitution mapping (e.g., replacing `[DATE_TIME_START]` with actual values)
- Sets map canvas and legend items
- Exports the composed layout as PDF

Key setup variables include `project_path = 'project.qgs'` and `template_path = 'template.qpt'`.

## Execution

The script runs via command line:

```bash
python generate_pdf.py
```

**Benefit:** This approach enables "all kinds of useful outputs without ever needing to open QGIS each time you generate the report."

## Additional Resources

The author references a Gist repository for potential future updates to the example code.
