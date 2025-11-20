# generic-bot (python:3.13)

FastAPI backend with PostgreSQL, Redis, Alembic migrations, and CI-ready structure.
Run locally:

docker compose up --build

Health Check:
http://localhost:8000/health


You are a senior software engineer. Explain the architecture, design, goals, and structure of the repository below. Be precise and concise, focusing on how requests flow through layers, where logic resides, and how to extend it.

Project name: generic_bot

High‑level purpose:
- Multi‑channel conversational bot for automotive use cases: pricing inquiries, service booking, test‑drive scheduling, lead capture, and FAQ responses.
- Intent‑driven routing with entity extraction and a simple knowledge base.

Primary entry points:
- HTTP API: `app/main.py`, `api/v1/webhook_router.py`, `api/v1/health.py`
- Console runner: `app/api/console_chat.py`

Configuration:
- App config: `app/config.py`
- Dependencies: `requirements.txt`
- Containers: `Dockerfile`, `docker-compose.yml`

Channels and I/O:
- WhatsApp: `channel_handlers/whatsapp_handler.py`, `connector/whatsapp_connector.py`, `clients/whatsapp_client.py`
- Console: `connector/console_connector.py`

Core services (NLU and orchestration):
- Intent classification: `services/intent_classifier.py`
- Entity extraction: `services/entity_extractor.py`
- Intent routing and orchestration: `services/intent_router.py`, `services/intent_engine.py`
- Knowledge lookups from FAQ: `services/knowledge_engine.py` using `knowledge/faq_knowledge.json`

Business logic per intent:
- Pricing: `intent_handlers/price_handler.py`
- Service: `intent_handlers/service_handler.py`
- Test drive: `intent_handlers/test_drive_handler.py`

Persistence layer:
- ORM models: `models/*.py` (e.g., `car_inventory.py`, `car_image.py`, `car_valuation.py`, `test_drive_booking.py`, `callback_request.py`, `whatsapp_log.py`)
- DB infrastructure: `db/base.py`, `db/base_class.py`, `db/session.py`, `db/deps.py`
- Repositories: `repositories/whatsapp_repository.py`, `repositories/deps.py`
- Migrations: Alembic in `alembic.ini` and `migrations/`

HTTP API surface:
- Health check: `api/v1/health.py`
- Webhook routing: `api/v1/webhook_router.py` dispatches to channel handlers

Request flow overview:
1. Inbound message arrives via HTTP webhook (`api/v1/webhook_router.py`) or console (`api/console_chat.py`).
2. Channel handler normalizes input (`channel_handlers/whatsapp_handler.py`) and delegates to a connector (`connector/*.py`).
3. Orchestrator invokes NLU pipeline: classify intent (`services/intent_classifier.py`), extract entities (`services/entity_extractor.py`), and route (`services/intent_router.py` / `services/intent_engine.py`).
4. Appropriate intent handler executes domain logic (`intent_handlers/*`), optionally queries knowledge base (`services/knowledge_engine.py`) or DB via repositories.
5. Response is sent back through the channel client (`clients/whatsapp_client.py`) or console, and interactions may be logged (`models/whatsapp_log.py`).

Design goals:
- Clear separation of concerns: API, channel adapters, NLU services, intent handlers, persistence.
- Extensibility: add new channels by implementing a connector, handler, and client; add new intents by creating a handler and registering it in the router.
- Testability: unit tests for NLU and knowledge components.
- Observability and auditability via message logging and models.

Testing:
- NLU and knowledge tests in `tests/` and `app/api/tests/` (e.g., `tests/test_entity_extractor.py`, `tests/test_intent_classifier.py`, `tests/test_knowledge_engine.py`).

How to extend:
- New intent: add `intent_handlers/<new_intent>_handler.py`, wire it in `services/intent_router.py`, update classifier training or rules, and add tests.
- New channel: implement `connector/<channel>_connector.py`, `channel_handlers/<channel>_handler.py`, and a client in `clients/`.
- New data entities: add models in `models/`, update `db/base.py`, create Alembic migration in `migrations/`.

Assumptions and stack:
- Python with ORM patterns (`db/*`, `models/*`) and Alembic migrations.
- Linux deployment supported; containerized via `Dockerfile` and `docker-compose.yml`.
