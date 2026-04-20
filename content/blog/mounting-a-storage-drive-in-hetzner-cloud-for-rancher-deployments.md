---
author: Admire Nyakudya
date: '2019-04-11'
description: This article builds upon an earlier blog post by Tim Sutton on using-a-sambacifs-mount-as-a-docker-volume.
erpnext_id: /blog/uncategorised/mounting-a-storage-drive-in-hetzner-cloud-for-rancher-deployments
erpnext_modified: '2019-04-11'
reviewedBy: Automated Check
reviewedDate: '2026-04-13'
tags:
- Uncategorised
thumbnail: /img/blog/erpnext/volumes-server.png
title: Mounting a Storage Drive in Hetzner Cloud for Rancher Deployments
---

This article builds upon an earlier blog post by Tim Sutton on [using-a-sambacifs-mount-as-a-docker-volume](<https://kartoza.com/en/blog/using-a-sambacifs-mount-as-a-docker-volume/>). In the previous article, Tim described the process of mounting a storage driver in detail.

What has necessitated this article is the recent changes in what hetzner offers to configure a storage driver. In this article, I will describe the process of mounting a storage driver in hetzner cloud to use in rancher V1.1. Yes, we are still using rancher v1 in favour of the new shiny rancher 2.

**The problem**

In the last article, Tim articulated our workflow and our reasons for wanting to use storage drivers. I will just clarify what has changed since the last article.

Hetzner now provides cloud storage option equivalent to Amazon S3 which we now use presents for application stacks which need larger amounts of storage. In this deployment, we have utilized

[docker-geoserver](<https://github.com/kartoza/docker-geoserver>) ,[docker-postgis](<https://github.com/kartoza/docker-postgis>) and [docker-sftp-backup](<https://github.com/kartoza/docker-sftp-backup>) deployed through rancher orchestration. These services require substantial space due to the GeoServer data directory storing raster images. In this setup, we will be adding extra storage to manage PostGIS backs. Using the same setup we could expand the storage space for our GeoServer container.

1\. Login into the hosting provider ([http://hetzner.de](<http://hetzner.de>)).

2\. Select your server and then navigate to the volumes section.

![volumes](/img/blog/erpnext/volumes-server.png)

3\. Select an appropriate size to buy. Since our backup strategy uses the docker-sftp-backup we need to identify how much storage space we need. So in order to do this, I have decided on the following metrics

Variable | Number to keep | Total Size  
---|---|---  
DAILY number of daily backups to keep | 2 | 20 g  
MONTHLY number of monthly backups to keep | 6 | 60  
YEARLY number of yearly backups to keep | 1 | 10  
  
The numbers above are based inspecting a manual backup which is roughly about 8gig and I then assumed in the future the backup would grow up to 10gig.

4\. Attach your storage driver to your specific server instance.

5\. Reset your root password so that you can login to the server.

![password](/img/blog/erpnext/root-password.png)

6\. Use the console to login into the server.

![root-console](/img/blog/erpnext/root-console.png)

7\. Click on the attached volume and select show configuration.

![config](/img/blog/erpnext/volume-config.png)

8\. In the server, console add the first line from the configuration ie `sudo mkfs.ext4 -F /dev/disk/by-id/scsi-0HC_Volume_2339452`

9\. Navigate to rancher and upgrade your container.

10\. In the volumes section choose the mount point to be `/mtn/HC_Volume_2339452:/backups`. Hetzner always mounts the storage driver to `/mnt/HC_Volume_unique_number`
