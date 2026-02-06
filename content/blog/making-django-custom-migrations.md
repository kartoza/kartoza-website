---
title: "Making Django Custom Migrations"
description: "The article explores using Django's makemigrations and migrate commands, specifically focusing on creating custom migrations when automatic generation doesn't meet project needs."
tags:
  - Python
  - Django
date: 2021-02-01
author: "Zulfikar Akbar Muzakki"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="Making Django Custom Migrations"
    subtitle="Python"
    class="is-primary"
    sub-block-side="bottom"
>}}
The article explores using Django's makemigrations and migrate commands, specifically focusing on creating custom migrations when automatic generation doesn't meet project needs.
{{< /block >}}

## Overview

The article explores using Django's `makemigrations` and `migrate` commands, specifically focusing on creating custom migrations when automatic generation doesn't meet project needs.

## Problem Statement

The developer needed to add `created_at` and `updated_at` DateTimeField columns to an existing database table called `FarmerSample`. The challenge involved populating these fields with meaningful data rather than accepting Django's default timestamp values.

The original model tracked observations with a `datum` field (DateField) representing when observations occurred—often days before database entry. Standard migration prompts would set timestamps to the migration execution time, which didn't reflect actual data chronology.

## Solution: Custom Migration with RunPython

Rather than creating a management command, the developer chose implementing a custom migration using Django's `RunPython` operation. This approach involves:

### Forward Function

```python
def set_created_at(apps, schema_editor):
    live_layer_db = schema_editor.connection.alias
    FarmerSample = apps.get_model("live_layer", "FarmerSample")

    for data in FarmerSample.objects.using(live_layer_db).all():
        datum_with_tz = datetime.combine(
            data.datum,
            time(0, 0),
            tzinfo=pytz.timezone(settings.TIME_ZONE)
        )
        created_at = datum_with_tz + timedelta(2)
        data.created_at = created_at
        data.save()
```

This function converts the DateField to timezone-aware DateTime, then sets `created_at` to two days after the observation date.

### Reverse Function

```python
def unset_created_at(apps, schema_editor):
    pass
```

The reverse function remains empty since unapplying the migration automatically removes added fields.

## Key Implementation Details

The migration operations include:
- `AddField` for both timestamp columns
- `RunPython(set_created_at, unset_created_at, atomic=True)`

Important considerations:
- Always provide both forward and reverse functions for reversibility
- The `atomic=True` parameter ensures database transaction safety
- Exit and re-enter the Django shell to verify changes (cached data displays outdated information)

## Results

After migration execution, records displayed properly configured timestamps with `created_at` reflecting observation dates plus two days and `updated_at` showing the migration completion time.

## Author Bio

Zakki is an Indonesian software developer based in Central Java with expertise in Python and Django development. His interest in GIS emerged from digital mapping exploration. Outside coding, he volunteers at community learning centers and enjoys motorcycling and documentaries.
