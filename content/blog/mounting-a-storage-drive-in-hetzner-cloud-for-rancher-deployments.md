---
title: "Mounting a Storage Drive in Hetzner Cloud for Rancher Deployments"
description: "This article builds upon an earlier blog post by Tim Sutton on using-a-sambacifs-mount-as-a-docker-volume."
tags:
  - Hosting
  - Docker
  - Rancher
date: 2019-04-11
author: "Admire Nyakudya"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="Mounting a Storage Drive in Hetzner Cloud for Rancher Deployments"
    subtitle="Hosting"
    class="is-primary"
    sub-block-side="bottom"
>}}
This article builds upon an earlier blog post by Tim Sutton on using-a-sambacifs-mount-as-a-docker-volume.
{{< /block >}}

## Mounting Storage Drives for Rancher

The article expands on a previous discussion regarding storage driver implementations. Key changes since the earlier post include Hetzner's introduction of cloud storage comparable to Amazon S3.

### Problem Statement

The deployment utilizes docker-geoserver, docker-postgis, and docker-sftp-backup through Rancher orchestration. These services require substantial storage due to GeoServer's data directory containing raster images.

### Storage Calculation Metrics

| Variable | Number to Keep | Total Size |
|----------|---|---|
| Daily backups | 2 | 20 GB |
| Monthly backups | 6 | 60 GB |
| Yearly backups | 1 | 10 GB |

These calculations assumed individual backups of approximately 8GB, potentially growing to 10GB.

### Setup Steps

1. Log into hosting provider (hetzner.de)
2. Navigate to volumes section for your server
3. Select appropriate storage size
4. Attach storage driver to server instance
5. Reset root password for console access
6. Login via console
7. Access attached volume configuration
8. Execute:
   ```bash
   sudo mkfs.ext4 -F /dev/disk/by-id/scsi-0HC_Volume_2339452
   ```
9. Navigate to Rancher and upgrade container
10. Set mount point to `/mtn/HC_Volume_2339452:/backups` (Hetzner mounts to `/mnt/HC_Volume_unique_number`)
