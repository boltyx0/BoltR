# BoltR - Advanced Offensive Reconnaissance

<p align="center">
<img src=".github/images/banner-boltr.jpg" alt="BoltR" />
</p>

<p align="center">
  <a href="https://www.gnu.org/licenses/gpl-3.0" target="_blank"><img src="https://img.shields.io/badge/License-GPLv3-red.svg" alt="License: GPLv3" /></a>
</p>

**BoltR** is a web application reconnaissance platform for offensive security, penetration testing, and bug bounty. It automates and centralizes subdomain discovery, endpoint enumeration, vulnerability scanning, and reporting with configurable scan engines, database-backed recon data, and a dark-themed UI.

---

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Scripts](#scripts)
- [Customizations in This Fork](#customizations-in-this-fork)
- [Troubleshooting](#troubleshooting)
- [Documentation & Contributing](#documentation--contributing)
- [License](#license)

---

## Features

- **Reconnaissance**: Subdomain discovery, port scanning, endpoint enumeration, screenshot, and technology detection
- **Scan engines**: Configurable YAML-based engines (Nuclei, Subfinder, Amass, etc.) with custom tools
- **Projects & targets**: Organize work by project and target; track subdomains, endpoints, and vulnerabilities
- **Vulnerability management**: Store and triage findings; optional LLM-assisted report generation
- **Reporting**: Export to PDF and other formats
- **Toolbox**: Built-in utilities (Whois, CMS detection, CVE lookup, WAF detection)
- **API**: REST API and WebSocket for integrations and automation
- **Dark UI**: “Onyx / Deep Carbon” dark theme with pill-style navigation

---

## Requirements

- **Docker** 20.10+ and **Docker Compose** 1.28+ (or `docker compose` v2)
- **Git**
- Sufficient resources: multi-core CPU, 4GB+ RAM, and disk space for scan results and databases

**Security:** Do not commit `.env`; use `.env-dist` as a template and copy it to `.env`, then set your own passwords and keys.


---

## Scripts

| Script | Purpose |
|--------|--------|
| `./install.sh` | Full install: checks Docker, builds/pulls images, starts stack |
| `./scripts/restart_web.sh` | Restart web and proxy containers (use after 502 or config changes) |
| `./scripts/update.sh` | Update application (images and/or code) |
| `./scripts/health_check.sh` | Basic health checks (see `HEALTH_CHECK.md`) |
| `./scripts/run_tests.sh` | Run test suite |

---


## Troubleshooting

- **502 Bad Gateway after restarting the web container**  
  Restart the proxy so it re-resolves the web backend:
  ```bash
  ./scripts/restart_web.sh
  ```
  Or: `docker compose -f docker/docker-compose.yml restart web proxy`

- **Static files or UI not updating**  
  Ensure `collectstatic` has been run (e.g. inside the web container) and hard-refresh the browser (Ctrl+Shift+R). If using Docker, rebuild or ensure the `web` service uses the correct static volume/image.

- **Tools Arsenal – Netlas**  
  If you changed the Netlas tool to use `--update`, fix it in the UI (Modify Tool) or in the database so it uses the correct upgrade command.

- **Logs**  
  Use `docker compose -f docker/docker-compose.yml logs -f web` (or the relevant service) for application logs.


BoltR is a fork focused on branding, UI/UX, and operational customizations for offensive reconnaissance workflows.
