# BoltR — Project Overview (for developers and AI agents)

This document explains the project from scratch so a developer or an AI agent can understand the codebase, run it, and make changes without reading every file.

---

## 1. What This Project Is

**BoltR** is a **reconnaissance and vulnerability management platform** for offensive security:

- Users create **projects** and **targets** (domains/IPs).
- They run **scans** (subdomain discovery, port scan, endpoint crawl, Nuclei, etc.) via configurable **scan engines** (YAML-defined).
- Results are stored in the DB: **subdomains**, **endpoints**, **vulnerabilities**.
- The UI shows dashboards, tables, and reports; the **REST API** and **WebSockets** allow automation.

It is a **Django** app (Python) with **Celery** for async tasks, **PostgreSQL**, **Redis**, and a **Nginx**-based proxy. The frontend is server-rendered templates (Django + Bootstrap) plus jQuery and custom JS. This repo is a **fork of reNgine-ng** with BoltR branding, a dark theme, a second nav bar, and HackerOne settings removed.

---

## 2. Tech Stack (high level)

| Layer        | Technology |
|-------------|------------|
| Backend     | Django (Python), Django REST Framework, Celery |
| DB          | PostgreSQL |
| Cache / broker | Redis |
| Frontend    | Django templates, Bootstrap 5, jQuery, DataTables, SweetAlert2 |
| Static      | Collected into `staticfiles/` (Nginx or Django serves) |
| Deployment  | Docker Compose: `db`, `redis`, `celery`, `celery-beat`, `web`, `proxy`, optional `ollama` |
| Scan execution | Celery workers run tasks that invoke CLI tools (nuclei, subfinder, etc.) |

---

## 3. Repository Layout (what lives where)

```
boltr/
├── docker/                    # Docker Compose and service configs
│   ├── docker-compose.yml     # Main stack (db, redis, celery, web, proxy)
│   ├── web/                   # Web container Dockerfile and entrypoint
│   ├── celery/                # Celery worker image and config
│   ├── proxy/                 # Nginx config (rengine.conf)
│   └── ...
├── web/                       # Django application (the actual app)
│   ├── reNgine/               # Django project: settings, urls, wsgi, common_views
│   ├── api/                   # REST API (DRF), WebSockets
│   ├── dashboard/             # Dashboard views, onboarding
│   ├── scanEngine/            # Scan engines, wordlists, settings (proxy, report, etc.)
│   ├── startScan/             # Scan start/stop, history, subscans
│   ├── targetApp/             # Projects, targets, domains
│   ├── recon_note/            # To-do / notes
│   ├── templates/             # Global templates
│   │   └── base/              # Base layout, top_bar, top_nav, footer
│   ├── static/                # CSS, JS, images (source)
│   ├── config/                # Default scan engine YAMLs
│   └── ...
├── scripts/                   # Shell helpers
│   ├── install.sh             # Main installer
│   ├── restart_web.sh         # Restart web + proxy
│   ├── update.sh              # Update app
│   └── health_check.sh        # Health checks
├── .env-dist                  # Example env; copy to .env
├── install.sh                 # Entry point that sources scripts and runs install
├── README.md                  # User-facing readme
└── PROJECT_OVERVIEW.md        # This file
```

- **URLs**: Root URLs in `web/reNgine/urls.py`. App URLs: `dashboard/`, `target/`, `scanEngine/`, `scan/`, `api/`, etc.
- **Templates**: Base layout in `web/templates/base/`. App-specific templates under `web/<app>/templates/`.
- **Static**: Source in `web/static/`. Collected to `web/staticfiles/` (or env-equivalent). Custom CSS/JS: `web/static/custom/` (e.g. `custom.js`, `design_override.css`).
- **Config**: Scan engine definitions in `web/config/default_scan_engines/`. Environment in `.env` (from `.env-dist`).

---

## 4. How to Run It

- **Install (first time)**: `./install.sh` (from repo root). Ensures Docker, uses `.env`, builds/pulls and starts containers.
- **Restart web (after code/config change or 502)**: `./scripts/restart_web.sh`.
- **Access**: URL shown by installer (e.g. `https://127.0.0.1`). First visit: onboarding (admin user + first project).
- **Logs**: `docker compose -f docker/docker-compose.yml logs -f web` (or `celery`, `proxy`, etc.).
- **Tests**: `./scripts/run_tests.sh` or run Django tests inside the web container.

---

## 5. Key Entry Points (code)

- **Django project**: `web/reNgine/` — `settings.py`, `urls.py`, `wsgi.py`, `common_views.py` (e.g. permission_denied, page_not_found).
- **Main app URLs**: Included from `dashboard`, `targetApp`, `scanEngine`, `startScan`, `api`, etc.
- **Base template**: `web/templates/base/base.html` — includes `top_bar.html`, then `#wrapper`, then `content-page`. Second nav is **inside** `top_bar.html` (`.boltr-second-nav`), not a separate include.
- **Top bar / second nav**: `web/templates/base/_items/top_bar.html` — logo, search, user menu, and the horizontal nav row (Dashboard, Projects, Targets, Scan History, …).
- **Theme / layout CSS**: `web/static/custom/design_override.css` and critical inline styles in `base.html` (dark theme, `.boltr-second-nav`, `.boltr-nav-links`, content `margin-top`).
- **Custom JS**: `web/static/custom/custom.js` — toolbox, vuln tables, report to Hackerone (if used), and a small BoltR nav fix for legacy `.topnav` if present.
- **API**: `web/api/` — DRF views and routers; WebSocket consumers in `api/` for live updates.
- **Celery tasks**: Defined under `web/reNgine/tasks/` and related modules; invoked from `startScan` and scan engine logic.

---

## 6. Customizations in This Fork (quick reference)

- **Branding**: “rengine” / “reNgine-ng” → **BoltR** in UI, API title, reports, login, onboarding. Logo: `web/static/img/boltr-logo.png`.
- **Layout**: Horizontal layout (`data-layout-mode="horizontal"`). Second nav is a **second row inside the top bar** (`.boltr-second-nav` + `.boltr-nav-links`), not the original theme’s standalone `.topnav` block. Content area has `margin-top: 125px` so it clears both rows.
- **Theme**: Dark only; theme toggle removed. Overrides in `design_override.css` and inline critical CSS in `base.html`.
- **HackerOne settings**: Removed from UI and routing. The route `scanEngine/hackerone_settings` is **removed** in `web/scanEngine/urls.py`. Menu links to “Hackerone Settings” removed from `top_bar.html` and `top_nav.html`. The test `test_hackerone_settings_view` is skipped. “Report to Hackerone” in vuln UI and HackerOne team handle on targets may still exist elsewhere.
- **Debug**: No debug log endpoint or hardcoded paths left in the repo; `.cursor/` is in `.gitignore`.

---

## 7. Where to Change What

| Goal | Where to look |
|------|----------------|
| Change nav items (second bar) | `web/templates/base/_items/top_bar.html` — `.boltr-second-nav` and `.boltr-nav-links` |
| Change top bar (logo, search, user) | `web/templates/base/_items/top_bar.html` |
| Change global layout / theme | `web/templates/base/base.html` (inline critical CSS), `web/static/custom/design_override.css` |
| Change dashboard or onboarding | `web/dashboard/` (views, templates) |
| Add/change API endpoints | `web/api/urls.py`, `web/api/views.py` |
| Add/change scan engine logic | `web/scanEngine/`, `web/reNgine/tasks/` |
| Add/change scan start/stop UI | `web/startScan/` |
| Add/change project/target models or UI | `web/targetApp/` |
| Add/change static JS/CSS | `web/static/custom/` (then run collectstatic if needed) |
| Add/change URLs (non-API) | `web/reNgine/urls.py` or the relevant app’s `urls.py` |
| Environment / Docker | `.env`, `docker/docker-compose.yml`, `docker/web/`, `docker/proxy/` |

---

## 8. Important Conventions

- **Permissions**: Many views use `@has_permission_decorator` and permission tags in templates (`user|can:'...'`). Check `web/reNgine/roles.py` and app-level permissions for behavior.
- **Context**: Base context (e.g. `current_project`, `user`, `projects`) is provided by context processors; see `settings.TEMPLATES[].OPTIONS.context_processors`.
- **Static**: In production, run `collectstatic` and serve via proxy/whitenoise; in dev, Django can serve static files. Custom assets: `web/static/custom/` and `web/static/img/`.
- **No secrets in repo**: Use `.env` (from `.env-dist`); `.env` and `docker/secrets` are gitignored.

---

## 9. One-Paragraph Summary

BoltR is a Django-based recon platform (fork of reNgine-ng) that runs in Docker (PostgreSQL, Redis, Celery, Nginx). Users manage projects and targets, run configurable scans (subdomain/port/endpoint/vuln), and view results in a dark-themed UI. The fork customizes branding to BoltR, adds a second nav row inside the top bar, removes the HackerOne settings section, and uses a fixed dark theme. Main code lives under `web/` (reNgine project, api, dashboard, scanEngine, startScan, targetApp, templates, static); run with `./install.sh` and restart with `./scripts/restart_web.sh`.
