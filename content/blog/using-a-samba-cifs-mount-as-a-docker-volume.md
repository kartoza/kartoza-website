---
author: Tim Sutton
date: '2018-04-07'
description: I preface this article by saying that what I am showing here is probably
  not best practice and you should test to see if it works reliably f
erpnext_id: /blog/docker/using-a-samba-cifs-mount-as-a-docker-volume
erpnext_modified: '2018-04-07'
reviewedBy: Automated Check
reviewedDate: '2026-04-13'
tags:
- Docker
thumbnail: /img/blog/placeholder.png
title: Using a SAMBA/CIFS Mount as a Docker Volume
---

I preface this article by saying that what I am showing here is probably not best practice and you should test to see if it works reliably for you before taking this route. I should also mention that this is a hacky approach because it breaks our ‘never log on to a server’ rule, so it is not a long-term solution - it is a short-term hack until Hetzner adds a cloud storage offering to their cloud platform.

  


### The problem

Our hosting provider ([https://www.hetzner.com](<https://www.hetzner.com/>)) recently added new cloud services which provide compute server capacity. In our architectures, we use Docker and Rancher to deploy services onto these cloud servers. Hetzner doesn’t yet have any cloud storage option equivalent to Amazon S3 which presents a problem for application stacks which need larger amounts of storage. On their legacy platform, Hetzner does provide cheap storage which can be accessed by FTP or SMB. They don’t, however, provide NFS (which is supported by Rancher). So I looked for a way to support mounting docker volumes on SMB mount points.

  


The trick here is to mount the folder that a docker storage volume uses from an external storage device (in this example I am using a CIFS/SMB mount). Don’t try this for containers that need low latency (e.g. a bad idea for a database file system). It can be used when you want to store large amounts of data on cheaper, off-server storage (e.g. backups). In my application stack I have a volume for backups which can be found on the host system here:

  


`/var/lib/docker/volumes/db-backups/_data`

  


So my approach was to stop any containers using this volume, move any data out of the folder, mount the _data folder as an SMB volume and restart the containers using this volume. To start I logged in to the host and installed `cifs-utils` so that I can mount SMB volumes:

  


`apt-get install cifs-utils left`

  


Next create a credentials file in /etc/backup-credentials.txt

  


`username=someuser`

`password=somesecret`

  


Add this to `/etc/fstab`

  


`//smb.host/path /var/lib/docker/volumes/db-backups/_data cifs rw,credentials=/etc/backup-credentials.txt,uid=0,gid=0,file_mode=0660,dir_mode=0770 0 0`

  


Replace `//smb.host/path` with the server name and file share path. The second option is the path to the docker volume - you need to update that to match your volume that you are trying to mount from SMB. We also have to mount the volume as non utf-8 for now as the NLS kernel module is not available in the Hetzner cloud machines. After this I mounted the SMB volume using

  


`mount -a`

  


Next I restarted the docker containers that use that volume. To test I logged into the Hetzner storage box and watched the file system whilst triggering a backup from one of my docker containers:

  


lftp` -u `someuser smb`.host `

  


`lftp someuser@some.host:~> ls `

`drwxr-xr-x 3 someuser someuser 3 Apr 6 19:24 2018`

  


`lftp someuser@some.host:/> cd 2018/`

`lftp someuser@some.host:/2018> ls`

`drwxr-xr-x 2 someuser someuser 5 Apr 6 19:24 April`

  


`lftp someuser@some.host:/2018> cd April/`

`lftp someuser@some.host:/2018/April> ls`

`-rw-r--r-- 1 someuser someuser 2840559 Apr 6 19:24 PG_postgis_alaska.06-April-2018.dmp`

  


Everything worked perfectly and now my space limited server can make backups without using up local storage space!

  


### Summary:

  


This technique is a handy way to attach cheap storage into your cloud hosts that use docker, but be aware of the shortcomings - especially in the fact that it requires you to log in and administer the cloud host, rather than just let it be completely managed by Rancher.
