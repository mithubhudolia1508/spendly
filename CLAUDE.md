# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Spendly** — a personal expense tracker web app targeted at Indian users (currency: ₹). Built with Flask + SQLite, Jinja2 templates, vanilla JS/CSS. No frontend build step.

## Commands

```bash
# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run (http://127.0.0.1:5001, debug mode on)
python3 app.py

# Tests
pytest
```

No linter is configured.

## Architecture

**Single-file backend:** All routes live in `app.py`. The app uses server-side rendering — Flask handlers render Jinja2 templates; there are no API/JSON endpoints.

**Templates** extend `templates/base.html`, which provides the navbar, footer, and Jinja2 `{% block %}` slots (`title`, `content`, `scripts`).

**Database** (`database/db.py`) is a planned SQLite module with three helpers: `get_db()`, `init_db()`, `seed_db()`. It is not yet implemented. The DB file `expense_tracker.db` is gitignored. `database/__init__.py` is an empty package init.

**Static assets:** All CSS is in `static/css/style.css` (single file, ~860 lines). `static/js/main.js` is currently an empty stub.

## Current State

The UI shell is complete (landing, login, register, terms, privacy pages). Backend is mostly stubs:

- `GET` routes for `/login`, `/register` render forms but have no `POST` handlers
- `/logout`, `/profile`, `/expenses/add`, `/expenses/<id>/edit`, `/expenses/<id>/delete` are all stub routes
- No session management or authentication logic exists yet
- Database schema and `db.py` helpers are TODO

Planned build order (referenced in code comments): database setup → auth (login/register/logout) → profile → expense CRUD.
