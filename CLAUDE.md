# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Django REST API backend for chriskumm.com. The Django project package is named `drf_project`. The API is served at `api.chriskumm.com`.

## Commands

```bash
# Install dependencies
poetry install

# Run development server (ASGI via Daphne)
poetry run python manage.py runserver

# Run all tests
poetry run python manage.py test

# Run tests for a specific app
poetry run python manage.py test art

# Run a single test
poetry run python manage.py test art.tests.SomeTestCase.test_method

# Check formatting
poetry run black --check .

# Format code
poetry run black .

# Check for pending migrations
poetry run python manage.py makemigrations --check --dry-run

# Apply migrations
poetry run python manage.py migrate

# Load fixture data for a test server
python manage.py testserver art/fixtures/art_standard.json

# Dump app data to fixture (run from WSL, not PowerShell)
poetry run python manage.py dumpdata art -o art/fixtures/art_standard.json
```

## Architecture

### Django Apps

- **`drf_project/`** — Project settings, root URL config, ASGI config, and custom logging. URLs are prefixed: `admin/`, `api/art/`, `api/ai-chat/`.
- **`core/`** — Custom user model (`CoreUser` extends `django_modern_user.ModernUser`), custom admin site. `AUTH_USER_MODEL = "core.CoreUser"`.
- **`art/`** — InstaArt REST API (DRF). Models: `Artist`, `Location`, `Style`, `Piece`. `Piece` auto-generates a base64 thumbnail on save via a `post_save` signal in `art/signals.py`. Uses DRF serializers and fixtures in `art/fixtures/`.
- **`ai_chat/`** — REST endpoint (`POST /api/ai-chat/`) that proxies to OpenAI chat completions. Protected by Google reCAPTCHA verification (bypassed in DEBUG mode). Uses a singleton `SystemMessage` model (via `django-solo`) as the system prompt.
- **`ai_pals/`** — WebSocket consumer (`CritterGenerationConsumer`) that streams OpenAI GPT-3.5-turbo text and DALL-E 3 image generation for a "critter generator" feature. Uses Django Channels over ASGI.

### Key Design Decisions

- **ASGI server**: Daphne is listed first in `INSTALLED_APPS` to run as the ASGI server, supporting both HTTP and WebSockets.
- **Channel layers**: Uses `InMemoryChannelLayer` (no Redis required for development or small deployments).
- **CORS**: All origins allowed in DEBUG mode; production restricts to `chriskumm.com` and specific Vercel domains.
- **Environment config**: All secrets loaded via `python-decouple` from `.env`. Copy `.env.example` to `.env` and fill in values. Required keys: `SECRET_KEY`, `DEBUG`, `TIME_ZONE`, `OPENAI_API_KEY`, `RECAPTCHA_SECRET_KEY`, `ABUSEIPDB_API_KEY`, `EMAIL_HOST`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`.
- **Formatting**: Black is enforced via pre-commit hooks and CI. Migrations are excluded from Black formatting.
- **Fixtures**: `media/fixture/` contains media files for fixtures and is tracked in git. Load with `testserver` to get a safe copy of data.
