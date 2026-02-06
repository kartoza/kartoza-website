---
title: "Using a Docker Compose-Based Python Interpreter in PyCharm"
description: "JetBrains recently enabled native Docker Compose interpreter support, resolving earlier limitations around environment variable handling."
tags:
  - Docker
  - Python
  - PyCharm
  - Django
date: 2020-12-07
author: "Rizky Maulana Nugraha"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="Using a Docker Compose-Based Python Interpreter in PyCharm"
    subtitle="Docker"
    class="is-primary"
    sub-block-side="bottom"
>}}
JetBrains recently enabled native Docker Compose interpreter support, resolving earlier limitations around environment variable handling.
{{< /block >}}

## Introduction

The author reflects on evolving development practices, noting that "back then the standard approach of attaching your debug interpreter was by creating a virtual environment in your python project." Previously, debugging containerized Django projects required SSH daemons and remote interpreter configuration. JetBrains recently enabled native Docker Compose interpreter support, resolving earlier limitations around environment variable handling.

## Key Improvements in PyCharm

Recent versions now support:

- Multiple Docker Compose recipes with local overrides
- Environment file inclusion
- Local-to-container directory mapping
- Native environment variable inheritance in run configurations

## Requirements

The tutorial assumes familiarity with:

- Git and GitHub workflows
- Docker and Docker Compose fundamentals
- Linux, macOS, or WSL environments
- Python and Django basics
- Debugging methodologies
- PyCharm Pro Edition

## Standard Setup Without IDE

The author provides a sample Django microservice repository demonstrating initial setup. Running `docker-compose up --build -d` deploys services without IDE dependencies, maintaining workflow independence. Configuration uses environment variables through `.env` files and `docker-compose.override.yml` templates, enabling declarative deployments.

## PyCharm Configuration Steps

### Docker Compose Integration

PyCharm's built-in Docker plugin enables visual service management through the Services tab, supporting deployment creation, status monitoring, and configuration updates.

### Python Interpreter Setup

Configure interpreters by specifying Docker Compose configuration files and service selection, allowing PyCharm to build custom container images with debugging helpers.

### Path Mapping

Establish mappings between host and container directories to enable proper code navigation and debugging synchronization.

### Django Integration

Enable Django support through project settings, allowing access to Django Shell and template debugging capabilities.

### Run Configuration

Create Django server configurations that utilize environment variables from `.env`, supporting both execution and debugging modes with real-time breakpoint attachment.

## Testing Capabilities

Developers can execute Django tests directly through context menus or run individual test methods using IDE shortcuts, eliminating lengthy command-line invocations.

## Optional Beta Features

PyCharm supports storing run configurations as shareable files within repositories, facilitating team collaboration. However, the feature currently lacks modular interpreter storage, limiting discoverability.

## Conclusion

This workflow demonstrates Docker-compose debugging without sacrificing IDE-independent development. The integration proves especially valuable for teams with developer turnover, as "everything has already been prepared from the start," enabling rapid onboarding through declarative configurations.
