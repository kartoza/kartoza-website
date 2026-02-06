---
title: "Using a SAMBA/CIFS Mount as a Docker Volume"
description: "A technique for mounting Docker volumes on SMB endpoints, useful for non-latency-sensitive applications like backup storage."
tags:
  - Docker
  - SAMBA
  - CIFS
  - Storage
date: 2018-04-07
author: "Tim Sutton"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="Using a SAMBA/CIFS Mount as a Docker Volume"
    subtitle="Docker"
    class="is-primary"
    sub-block-side="bottom"
>}}
A technique for mounting Docker volumes on SMB endpoints, useful for non-latency-sensitive applications like backup storage.
{{< /block >}}

## Overview

The author acknowledges this approach is "probably not best practice" and recommends testing before implementation. He describes it as a temporary workaround rather than a long-term solution.

## The Problem

Hetzner's new cloud services lack storage options comparable to Amazon S3. While their legacy platform offers affordable storage via FTP or SMB, it doesn't support NFS (required by Rancher). The author needed a method to mount Docker volumes on SMB endpoints.

## Solution Architecture

The technique involves mounting a Docker volume's folder from external storage. It works best for non-latency-sensitive applications like backup storage, not databases.

**Target volume location:** `/var/lib/docker/volumes/db-backups/_data`

## Implementation Steps

### 1. Install CIFS utilities

```bash
apt-get install cifs-utils
```

### 2. Create credentials file

Create `/etc/backup-credentials.txt`:

```
username=someuser
password=somesecret
```

### 3. Add to `/etc/fstab`

```
//smb.host/path /var/lib/docker/volumes/db-backups/_data cifs rw,credentials=/etc/backup-credentials.txt,uid=0,gid=0,file_mode=0660,dir_mode=0770 0 0
```

### 4. Mount the volume

```bash
mount -a
```

### 5. Restart Docker containers

Restart Docker containers using the volume.

## Testing & Results

The author verified functionality by accessing the storage box via LFTP and confirming successful backup file creation.

## Summary

This technique provides cost-effective storage integration for Docker deployments but requires direct server administration, contradicting container orchestration best practices.
