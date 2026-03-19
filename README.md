# budget-tracker

An app for tracking household spending and budgeting.

## User Stories

- create a user account
- link user accounts in a household
- upload credit card statements and store encrypted data in database
- query database for info
- visualize weekly, monthly, and yearly spending by category and user

## Stack

- Flask (app factory pattern)
- Flask-SQLAlchemy + Flask-Migrate
- PostgreSQL (via Docker Compose)

## Project structure

```
.
├── app/
│   ├── __init__.py
│   ├── extensions.py
│   ├── models.py
│   └── routes.py
├── config.py
├── docker-compose.yml
├── requirements.txt
└── wsgi.py
```

## Run with Docker (app + database)

### 1) Create environment file

```bash
cp .env.example .env
```

### 2) Build and start containers

```bash
docker compose up --build -d
```

### 3) Initialize database tables

```bash
docker compose exec web flask --app wsgi:app init-db
```

The API is available at `http://localhost:5000`.

## Run locally (without Docker app container)

### 1) Start PostgreSQL

```bash
docker compose up -d
```

### 2) Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

### 4) Configure environment variables

```bash
cp .env.example .env
```

Default database URL in `.env`:

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/budget_tracker
```

### 5) Initialize database

```bash
flask --app wsgi:app init-db
```

### 6) Run the app

```bash
flask --app wsgi:app run --debug
```

## Endpoints

- `GET /` -> basic API message
- `GET /health` -> health check
