---
title: "7 Tips for Making Productive Use of Docker"
description: "I have been using and learning docker since the early days after it was announced. The author reflects on mistakes made and provides practical guidance to help new Docker users avoid similar pitfalls."
tags:
  - Docker
  - DevOps
  - Containers
date: 2015-04-01
author: "Gavin Fleming"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="7 Tips for Making Productive Use of Docker"
    subtitle="Docker"
    class="is-primary"
    sub-block-side="bottom"
>}}
I have been using and learning docker since the early days after it was announced. The author reflects on mistakes made and provides practical guidance to help new Docker users avoid similar pitfalls.
{{< /block >}}

## Content

The author shares experience with Docker since its early announcement, offering guidance to new users. The seven key recommendations are:

### 1. Dense packing vs. microservers

Docker excels at consolidating many isolated services on single servers, though configuration management tools like Ansible may suit other deployment approaches.

### 2. Architecture as appliances

Avoid treating containers like virtual machines. Follow Unix philosophy by creating single-purpose appliances (PostGIS, uWSGI, MapServer, GeoServer each in separate containers) rather than bundling multiple services.

### 3. Stateless containers

Design containers for destruction and redeployment without data loss. Invest in robust images rather than individual containers. Mount databases and uploaded files as host volumes; store no generated data internally.

### 4. Use orchestration tools

Leverage Docker Compose (formerly Fig) with YAML configuration files instead of building custom orchestration. Combine with Makefiles for simplified administration.

### 5. Image publishing and versioning

Publish images to hub.docker.com with automated builds triggered by repository pushes and upstream updates. Tag versions for tracking stable configurations.

### 6. Layered image construction

Build progressively (Ubuntu base → add Python → add Django) to minimize configuration per image and maximize layer sharing across services.

### 7. Multi-host architecture planning

Plan carefully for multi-node services, as Docker lacks robust built-in networking. Consider virtual switches or independent host operation.
