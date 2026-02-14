# BoltR — Advanced Offensive Reconnaissance

<p align="center">
<img src=".github/images/banner-rengine-ng.png" alt="BoltR" />
</p>

<p align="center">
  <a href="https://www.gnu.org/licenses/gpl-3.0" target="_blank"><img src="https://img.shields.io/badge/License-GPLv3-red.svg" alt="License: GPLv3" /></a>
</p>

**BoltR** is a web application reconnaissance platform for offensive security, penetration testing, and bug bounty. It automates and centralizes subdomain discovery, endpoint enumeration, vulnerability scanning, and reporting with configurable scan engines, database-backed recon data, and a dark-themed UI.

This repository is a customized fork of [reNgine-ng](https://github.com/Security-Tools-Alliance/rengine-ng) (Next Generation), with branding, UI, and feature customizations suited for internal or team use.

**BoltR fork by [boltyx0](https://github.com/boltyx0).**

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

## Quick Start

1. **Clone the repository**
   ```bash
   git clone <YOUR_GITHUB_REPO_URL> boltr
   cd boltr
   ```

2. **Configure environment**
   ```bash
   cp .env-dist .env
   # Edit .env and set RENGINE_VERSION, secrets, and any optional variables (see Configuration).
   ```

3. **Install and run**
   ```bash
   chmod +x install.sh
   ./install.sh
   ```
   The installer checks Docker, builds/pulls images, and starts services. When it finishes, open the URL shown (e.g. `https://127.0.0.1`) and complete the onboarding (create admin user and first project).

---

## Installation

### Option A: Install script (recommended)

From the project root:

```bash
./install.sh
```

This will:

- Check Docker and Docker Compose
- Use `.env` for configuration
- Build or pull images and start all services (DB, Redis, Celery, web, proxy, etc.)

### Option B: Manual Docker Compose

```bash
cp .env-dist .env
# Edit .env as needed
docker compose -f docker/docker-compose.yml up -d
```

Wait for the web container to be healthy, then access the app via the proxy (default port 443 or as set in your setup).

### Updating

To pull new images and recreate containers:

```bash
./scripts/update.sh
```

Or follow the [update section in the wiki](https://github.com/Security-Tools-Alliance/rengine-ng/wiki/Installation#-updating-rengine-ng) and adapt for your fork.

---

## Configuration

- **`.env`**: Copy from `.env-dist` and set at least:
  - `RENGINE_VERSION` – image tag / version
  - Database and Redis credentials
  - Any proxy or TLS settings your deployment needs
- **Scan engines**: Managed from the UI (Scan Engine → Scan Engines) or by adding/editing YAML under `web/config/`.
- **Static files**: After changing CSS/JS in `web/static/`, run `collectstatic` inside the web container (or your deploy process) so the proxy serves updated assets.

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

## Customizations in This Fork

- **Branding**: Product name and UI branding set to **BoltR** (logo, titles, login, reports).
- **Layout**: Horizontal layout with a **second navigation bar** (Dashboard, Projects, Targets, Scan History, Vulnerabilities, To-do, Organization, Scan Engine, Settings) embedded in the top bar for consistent visibility.
- **Theme**: Dark “Onyx / Deep Carbon” theme (dark sidebar, cards, pill nav). Theme toggle removed; dark mode is default.
- **HackerOne settings**: The HackerOne settings page and menu entry have been **removed**. The route `/scanEngine/hackerone_settings` is disabled. “Report to Hackerone” from vulnerability views may still exist but is not configured via this settings section.
- **Misc**: API title set to “BoltR API”; user-facing strings and report text reference BoltR where appropriate.

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

---

## Documentation & Contributing

- **Upstream wiki**: Many concepts (engines, workflows, installation details) are documented in the [reNgine-ng Wiki](https://github.com/Security-Tools-Alliance/rengine-ng/wiki). Use it as a reference and adapt instructions to your fork.
- **Changelog**: See [CHANGELOG.md](CHANGELOG.md) and the [wiki changelog](https://github.com/Security-Tools-Alliance/rengine-ng/wiki/changelog/) for release notes.
- **Contributing**: See [CONTRIBUTING.md](CONTRIBUTING.md) for how to contribute to this project.

---

## License

This project is licensed under the **GPL-3.0** license. See [LICENSE](LICENSE) for the full text.

---

## Acknowledgments

- **BoltR**: This fork is maintained by [boltyx0](https://github.com/boltyx0).
- [reNgine](https://github.com/yogeshojha/rengine) by Yogesh Ojha
- [reNgine-ng](https://github.com/Security-Tools-Alliance/rengine-ng) (Next Generation) by Security Tools Alliance and contributors

BoltR is a fork focused on branding, UI/UX, and operational customizations for offensive reconnaissance workflows.
