<p align="center">
  <a href="https://kartoza.com">
    <img src="static/img/kartoza-logo.png" alt="Kartoza Logo" width="300">
  </a>
</p>

<h1 align="center">Kartoza Website v3.0.1</h1>

<p align="center">
  <strong>A Happy Life is a Mappy Life</strong>
</p>

<p align="center">
  <em>Official website for <a href="https://kartoza.com">Kartoza</a> - Open Source Geospatial Experts</em>
</p>

<p align="center">
  <a href="https://kartoza.com">
    <img src="https://img.shields.io/badge/Live_Site-kartoza.com-00A86B?style=for-the-badge&logo=google-chrome&logoColor=white" alt="Live Site">
  </a>
</p>

---

<p align="center">
  <img src="img/home-page.png" alt="Kartoza Website Screenshot" width="800">
</p>

---

## Table of Contents

- [Table of Contents](#table-of-contents)
- [About Kartoza](#about-kartoza)
  - [Our Vision](#our-vision)
  - [What We Do](#what-we-do)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
  - [Using Nix (Recommended)](#using-nix-recommended)
  - [Using Docker](#using-docker)
  - [Manual Setup](#manual-setup)
- [Project Structure](#project-structure)
- [Content Management](#content-management)
  - [Adding Content](#adding-content)
  - [Front Matter Example](#front-matter-example)
  - [Images](#images)
- [Development](#development)
  - [Available Commands](#available-commands)
  - [CI/CD Workflows](#cicd-workflows)
- [Scripts](#scripts)
  - [Content Creation Scripts](#content-creation-scripts)
  - [Stats Update Scripts](#stats-update-scripts)
  - [ERPNext Integration Scripts](#erpnext-integration-scripts)
  - [Git Hooks](#git-hooks)
  - [Branch Protection](#branch-protection)
  - [Neovim Integration](#neovim-integration)
- [Security](#security)
- [Contributing](#contributing)
  - [Code Style](#code-style)
- [License](#license)
- [Contact](#contact)
- [Acknowledgements](#acknowledgements)

---

<p align="center">
  <!-- CI/CD Status -->
  <a href="https://github.com/kartoza/kartoza-website/actions/workflows/github-pages.yml">
    <img src="https://github.com/kartoza/kartoza-website/actions/workflows/github-pages.yml/badge.svg" alt="Deploy to GitHub Pages">
  </a>
  <a href="https://github.com/kartoza/kartoza-website/actions/workflows/nix-build.yml">
    <img src="https://github.com/kartoza/kartoza-website/actions/workflows/nix-build.yml/badge.svg" alt="Nix Build">
  </a>
  <a href="https://github.com/kartoza/kartoza-website/actions/workflows/playwright-e2e.yml">
    <img src="https://github.com/kartoza/kartoza-website/actions/workflows/playwright-e2e.yml/badge.svg" alt="E2E Tests">
  </a>
  <a href="https://github.com/kartoza/kartoza-website/actions/workflows/pr-checks.yml">
    <img src="https://github.com/kartoza/kartoza-website/actions/workflows/pr-checks.yml/badge.svg" alt="PR Checks">
  </a>
</p>

<p align="center">
  <!-- Version & Release -->
  <a href="https://github.com/kartoza/kartoza-website/releases/latest">
    <img src="https://img.shields.io/github/v/release/kartoza/kartoza-website?style=flat&logo=github&label=Latest%20Release" alt="Latest Release">
  </a>
  <a href="https://github.com/kartoza/kartoza-website/releases">
    <img src="https://img.shields.io/github/release-date/kartoza/kartoza-website?style=flat&label=Released" alt="Release Date">
  </a>
  <a href="https://github.com/kartoza/kartoza-website">
    <img src="https://img.shields.io/github/repo-size/kartoza/kartoza-website?style=flat&label=Repo%20Size" alt="Repo Size">
  </a>
</p>

<p align="center">
  <!-- Tech Stack -->
  <img src="https://img.shields.io/badge/Hugo-0.147+-FF4088?style=flat&logo=hugo&logoColor=white" alt="Hugo">
  <img src="https://img.shields.io/badge/Bulma-CSS-00D1B2?style=flat&logo=bulma&logoColor=white" alt="Bulma CSS">
  <img src="https://img.shields.io/badge/Nix-Flakes-5277C3?style=flat&logo=nixos&logoColor=white" alt="Nix Flakes">
  <img src="https://img.shields.io/badge/Docker-Ready-2496ED?style=flat&logo=docker&logoColor=white" alt="Docker">
</p>

<p align="center">
  <!-- Project Health -->
  <a href="https://github.com/kartoza/kartoza-website/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/kartoza/kartoza-website?style=flat" alt="License">
  </a>
  <a href="https://github.com/kartoza/kartoza-website/commits/main">
    <img src="https://img.shields.io/github/last-commit/kartoza/kartoza-website?style=flat" alt="Last Commit">
  </a>
  <a href="https://github.com/kartoza/kartoza-website/graphs/commit-activity">
    <img src="https://img.shields.io/github/commit-activity/m/kartoza/kartoza-website?style=flat&label=Commits/Month" alt="Commit Activity">
  </a>
  <a href="https://github.com/kartoza/kartoza-website/graphs/contributors">
    <img src="https://img.shields.io/github/contributors/kartoza/kartoza-website?style=flat" alt="Contributors">
  </a>
</p>

<p align="center">
  <!-- Issues & PRs -->
  <a href="https://github.com/kartoza/kartoza-website/issues">
    <img src="https://img.shields.io/github/issues/kartoza/kartoza-website?style=flat" alt="Open Issues">
  </a>
  <a href="https://github.com/kartoza/kartoza-website/issues?q=is%3Aissue+is%3Aclosed">
    <img src="https://img.shields.io/github/issues-closed/kartoza/kartoza-website?style=flat&color=success" alt="Closed Issues">
  </a>
  <a href="https://github.com/kartoza/kartoza-website/pulls">
    <img src="https://img.shields.io/github/issues-pr/kartoza/kartoza-website?style=flat" alt="Open PRs">
  </a>
  <a href="https://github.com/kartoza/kartoza-website/pulls?q=is%3Apr+is%3Aclosed">
    <img src="https://img.shields.io/github/issues-pr-closed/kartoza/kartoza-website?style=flat&color=success" alt="Closed PRs">
  </a>
</p>

<p align="center">
  <!-- Community -->
  <a href="https://github.com/kartoza/kartoza-website/stargazers">
    <img src="https://img.shields.io/github/stars/kartoza/kartoza-website?style=flat&logo=github" alt="Stars">
  </a>
  <a href="https://github.com/kartoza/kartoza-website/network/members">
    <img src="https://img.shields.io/github/forks/kartoza/kartoza-website?style=flat&logo=github" alt="Forks">
  </a>
  <a href="https://github.com/kartoza/kartoza-website/watchers">
    <img src="https://img.shields.io/github/watchers/kartoza/kartoza-website?style=flat&logo=github" alt="Watchers">
  </a>
</p>

<p align="center">
  <!-- Security & Quality -->
  <a href="https://github.com/kartoza/kartoza-website/security/dependabot">
    <img src="https://img.shields.io/badge/Dependabot-enabled-success?style=flat&logo=dependabot&logoColor=white" alt="Dependabot">
  </a>
  <img src="https://img.shields.io/badge/Spell%20Check-British%20English-blue?style=flat&logo=googledocs&logoColor=white" alt="Spell Check">
  <img src="https://img.shields.io/badge/Markdown-Lint-blue?style=flat&logo=markdown&logoColor=white" alt="Markdown Lint">
  <img src="https://img.shields.io/badge/Pre--commit-enabled-brightgreen?style=flat&logo=pre-commit&logoColor=white" alt="Pre-commit">
</p>

<p align="center">
  <!-- Infrastructure -->
  <img src="https://img.shields.io/badge/nginx-1.28.2-009639?style=flat&logo=nginx&logoColor=white" alt="nginx">
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white" alt="Python">
  <a href="https://github.com/kartoza/kartoza-website/blob/main/flake.nix">
    <img src="https://img.shields.io/badge/Nix-Reproducible-5277C3?style=flat&logo=nixos&logoColor=white" alt="Nix Reproducible">
  </a>
</p>

---

## About Kartoza

<img align="right" src="static/img/kartoza-logo.png" width="120">

**Kartoza** is a global Free and Open Source GIS (FOSS GIS) service provider registered in South Africa and Portugal. We use GIS software to address location-related challenges for individuals, businesses, and governments worldwide.

### Our Vision

> Enable a world where spatial decision making tools are **universal**, **accessible** and **affordable** for everyone for the benefit of the planet and people.

### What We Do

- Custom GIS software development
- Geospatial data management & analysis
- Training & capacity building
- Support & maintenance for open source GIS

---

## Technology Stack

| Category | Technology |
|----------|------------|
| **Static Site Generator** | [Hugo](https://gohugo.io/) (Extended) |
| **CSS Framework** | [Bulma](https://bulma.io/) |
| **Theme** | Custom `hugo-bulma-blocks-theme` |
| **Development Environment** | [Nix Flakes](https://nixos.wiki/wiki/Flakes) |
| **Container Runtime** | Docker + nginx |
| **CI/CD** | GitHub Actions |
| **Testing** | Playwright E2E |

---

## Prerequisites

| Requirement | Version | Notes |
|-------------|---------|-------|
| **Hugo** | 0.147+ | Extended version required |
| **Nix** | 2.4+ | Optional, but recommended |
| **Docker** | 20.10+ | Optional, for containerized deployment |

> **Note**: Using Nix Flakes automatically provides all dependencies. No manual installation required.

---

## Quick Start

### Using Nix (Recommended)

```bash
# Enter the development environment
nix develop

# Start the development server
hugo server
```

### Using Docker

```bash
# Build and run with Docker Compose
docker-compose up --build
```

### Manual Setup

```bash
# Prerequisites: Hugo extended version
hugo version  # Should show "extended"

# Start development server
hugo server -D

# Build for production
hugo --minify
```

The site will be available at `http://localhost:1313`

---

## Project Structure

```
Kartoza-Hugo/
├── content/               # Markdown content files
│   ├── about/             # About page
│   ├── apps/              # Mobile and web applications
│   ├── blog/              # Blog posts
│   ├── careers/           # Job listings
│   ├── gallery/           # Image gallery
│   ├── portfolio/         # Project portfolio
│   ├── solutions/         # Solutions and services
│   ├── the_team/          # Team members
│   └── training-courses/  # Training offerings
├── layouts/               # Custom Hugo templates
├── static/                # Static assets (images, etc.)
├── themes/                # Hugo theme
├── deployment/            # Docker & nginx configs
├── scripts/               # Automation scripts
└── flake.nix              # Nix development environment
```

---

## Content Management

### Adding Content

| Content Type | Location | Command |
|--------------|----------|---------|
| Blog post | `content/blog/` | `hugo new blog/my-post.md` |
| Team member | `content/the_team/` | `hugo new the_team/name.md` |
| Portfolio item | `content/portfolio/` | `hugo new portfolio/project.md` |
| Training course | `content/training-courses/` | `hugo new training-courses/course.md` |

### Front Matter Example

```yaml
---
title: "My Blog Post"
date: 2024-01-15
draft: false
author: "Team Member"
tags: ["QGIS", "GIS", "Tutorial"]
thumbnail: "img/blog/my-post-thumbnail.png"
---
```

### Images

Place images in the `static/img/` directory and reference them in markdown:

```markdown
![Alt text](/img/blog/my-image.png)
```

---

## Development

### Available Commands

| Command | Description |
|---------|-------------|
| `hugo server` | Start development server with live reload |
| `hugo server -D` | Include draft content |
| `hugo --minify` | Build optimized production site |
| `nix build` | Build site using Nix |
| `nix run` | Build and serve site |

### CI/CD Workflows

| Workflow | Purpose |
|----------|---------|
| `github-pages.yml` | Deploy to GitHub Pages |
| `nix-build.yml` | Verify Nix build |
| `playwright-e2e.yml` | End-to-end tests |
| `update-contributors.yml` | Sync contributor data |
| `update-donors.yml` | Sync donor information |
| `update-gh-sponsors.yml` | Sync GitHub Sponsors |

---

## Scripts

The `scripts/` directory contains automation scripts for content management. All scripts require the Nix development environment (`nix develop`) for dependencies.

### Content Creation Scripts

Create new content pages with proper templates:

```bash
# Create new content (prompts for title/name)
./scripts/new-blog.sh "My Blog Post Title"
./scripts/new-app.sh "My App Name"
./scripts/new-plugin.sh "My QGIS Plugin"
./scripts/new-portfolio.sh "Project Name"
./scripts/new-team-member.sh "First Last"
./scripts/new-training.sh "Course Title"
./scripts/new-docker.sh "Docker Image Name"
```

### Stats Update Scripts

Fetch and update stats from Docker Hub and QGIS Plugin Repository:

```bash
# Update Docker Hub stats (pulls, stars)
./scripts/update-docker-stats.py
./scripts/update-docker-stats.py --dry-run  # Preview changes

# Update QGIS plugin stats (downloads, rating, votes, version)
./scripts/update-plugin-stats.py
./scripts/update-plugin-stats.py --dry-run  # Preview changes

# Update all stats at once
./scripts/update-all-stats.py
./scripts/update-all-stats.py --dry-run     # Preview changes
```

Output example:

```
======================================================
DOCKER HUB STATS UPDATE
======================================================
Image       Pulls               Stars         Status
            Old → New           Old → New
------------------------------------------------------
postgis     21M+ → 22M+         198 → 205     Updated
geoserver   5M+ → 5M+           89 → 89       No change
------------------------------------------------------
Total: 8 | Updated: 3 | Unchanged: 4 | Errors: 1
======================================================
```

### ERPNext Integration Scripts

Fetch content from ERPNext (erp.kartoza.com) and compare with local files.

**Environment variables** (optional, for private content):

```bash
export ERPNEXT_URL="https://erp.kartoza.com"
export ERPNEXT_API_KEY="your-api-key"
export ERPNEXT_API_SECRET="your-api-secret"
```

**Fetch blogs from ERPNext:**

```bash
# List available blogs
./scripts/fetch-erpnext-blogs.py --list

# Fetch new blogs (won't overwrite existing local files)
./scripts/fetch-erpnext-blogs.py
./scripts/fetch-erpnext-blogs.py --dry-run  # Preview only
```

**Fetch portfolio items from ERPNext:**

```bash
# List available portfolio items
./scripts/fetch-erpnext-portfolio.py --list

# Fetch new portfolio items
./scripts/fetch-erpnext-portfolio.py
./scripts/fetch-erpnext-portfolio.py --dry-run  # Preview only
```

**Compare local content with ERPNext:**

```bash
# Compare all content
./scripts/compare-erpnext-content.py

# Compare specific content types
./scripts/compare-erpnext-content.py --blogs
./scripts/compare-erpnext-content.py --portfolio

# Verbose output with diff preview
./scripts/compare-erpnext-content.py --verbose
```

Output example:

```
============================================================
BLOG COMPARISON
============================================================
File                Title                 Similarity  Status
------------------------------------------------------------
my-blog-post.md     My Blog Post          95%         Minor changes
another-post.md     Another Post          100%        Identical
local-only.md       Local Only            -           No ERPNext ID
------------------------------------------------------------
Total: 45 | Identical: 30 | Modified: 5 | No ERPNext link: 10
============================================================
```

### Git Hooks

The project includes pre-commit hooks that enforce quality standards.

**Install hooks:**

```bash
./scripts/install-hooks.sh
```

**Pre-commit checks:**

| Check | Description | Autofix |
|-------|-------------|---------|
| **Reviewer verification** | Content pages must have `reviewedBy` (git user) and `reviewedDate` (today) | No |
| **Markdown lint** | Validates markdown syntax and style | Yes |
| **Spell check** | British English spelling (cspell) | No |

**If the hook rejects your commit:**

1. **Reviewer issues**: Press `<leader>pr` in Neovim to update reviewer tags
2. **Markdown issues**: Run `<leader>pfl` to lint and fix, or fix manually
3. **Spelling issues**: Fix the spelling, or add valid words to `.cspell/project-words.txt`

**Bypass (not recommended):**

```bash
git commit --no-verify
```

### Branch Protection

The `main` branch is protected with the following rules:

- Changes must be made through pull requests
- Required status checks must pass:
  - Markdown Lint
  - Spell Check (British English)
  - Reviewer Verification
- At least 1 approving review required
- Stale reviews are dismissed on new commits

### Neovim Integration

If using Neovim with which-key, the `.nvim.lua` config provides shortcuts under `<leader>p`:

| Keys | Action |
|------|--------|
| **Hugo** | |
| `ps` | Start Hugo server |
| `pb` | Build site |
| **Review** | |
| `pl` | List unreviewed pages |
| `pr` | Update reviewer (current user + today) |
| `pa` | Approve file (new only) |
| **New content** (`pn`) | |
| `pnb` | New blog post |
| `pna` | New app |
| `pnp` | New plugin |
| `pnP` | New portfolio |
| `pnt` | New team member |
| `pnT` | New training course |
| `pnd` | New Docker image |
| **Insert shortcode** (`pi`) | |
| `pib` | Insert block |
| `pic` | Insert columns |
| `pir` | Insert rich box |
| `pit` | Insert tabs |
| `pis` | Insert spoiler |
| **Format/Lint** (`pf`) | |
| `pfl` | Lint file (markdownlint) |
| `pfL` | Lint all content |
| `pfp` | Format file (prettier) |
| `pfs` | Spell check file |
| `pfS` | Spell check all content |
| `pfa` | Run all checks on file |
| `pfw` | Add word under cursor to dictionary |
| **Update stats** (`pu`) | |
| `pud` | Update Docker stats |
| `pup` | Update Plugin stats |
| `pua` | Update all stats |

---

## Security

This project follows security best practices:

- **Dependency Auditing**: Regular CVE scanning of all dependencies
- **Container Security**: Hardened nginx configuration with non-root user
- **Automated Updates**: nixpkgs-unstable for latest security patches
- **HTTPS Enforced**: All deployments use TLS

See our security practices in [`flake.nix`](./flake.nix) and [`Dockerfile`](./deployment/docker/Dockerfile).

---

## Contributing

We welcome contributions! Here's how to get started:

1. **Fork** the repository
2. **Clone** your fork locally
3. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
4. **Make** your changes
5. **Test** locally with `hugo server`
6. **Commit** your changes (`git commit -m 'Add amazing feature'`)
7. **Push** to the branch (`git push origin feature/amazing-feature`)
8. **Open** a Pull Request

### Code Style

- Use Prettier for formatting (config in `.prettierrc.json`)
- Follow Hugo template best practices
- Keep commits atomic and well-described

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](./LICENSE) file for details.

---

## Contact

<p align="center">
  <a href="https://kartoza.com">
    <img src="https://img.shields.io/badge/Website-kartoza.com-00A86B?style=for-the-badge&logo=google-chrome&logoColor=white" alt="Website">
  </a>
  <a href="mailto:info@kartoza.com">
    <img src="https://img.shields.io/badge/Email-info@kartoza.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Email">
  </a>
  <a href="https://github.com/kartoza">
    <img src="https://img.shields.io/badge/GitHub-kartoza-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub">
  </a>
</p>

<p align="center">
  <a href="https://www.linkedin.com/company/kartoza">
    <img src="https://img.shields.io/badge/LinkedIn-Kartoza-0A66C2?style=flat&logo=linkedin&logoColor=white" alt="LinkedIn">
  </a>
  <a href="https://www.youtube.com/@kartaborolong">
    <img src="https://img.shields.io/badge/YouTube-Kartoza-FF0000?style=flat&logo=youtube&logoColor=white" alt="YouTube">
  </a>
</p>

---

## Acknowledgements

This project was originally derived from the [QGIS Hugo Website Theme](https://github.com/qgis/QGIS-Hugo-Website-Theme). We thank the QGIS community for their excellent work on the original Hugo theme and site structure that served as the foundation for this project.

---

<p align="center">
  Made with :heart: by <a href="https://kartoza.com">Kartoza</a> |
  <a href="https://github.com/sponsors/kartoza">Donate!</a> |
  <a href="https://github.com/kartoza/kartoza-website">GitHub</a>
</p>

<p align="center">
  <sub>🌍 Empowering the world with Open Source Geospatial Solutions since 2008.</sub>
</p>
