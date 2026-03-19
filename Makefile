COMPOSE := docker compose

.PHONY: help up down build restart logs init-db reset-db shell ps

help:
	@echo "Available targets:"
	@echo "  make up       - Build and start containers"
	@echo "  make down     - Stop and remove containers"
	@echo "  make build    - Build containers"
	@echo "  make restart  - Restart containers"
	@echo "  make logs     - Follow logs from all services"
	@echo "  make init-db  - Create database tables"
	@echo "  make reset-db - Drop and recreate database tables"
	@echo "  make shell    - Open a shell in web container"
	@echo "  make ps       - Show running services"

up:
	$(COMPOSE) up --build -d

down:
	$(COMPOSE) down

build:
	$(COMPOSE) build

restart:
	$(COMPOSE) restart

logs:
	$(COMPOSE) logs -f

init-db:
	$(COMPOSE) exec web flask --app wsgi:app init-db

reset-db:
	$(COMPOSE) exec web flask --app wsgi:app reset-db

shell:
	$(COMPOSE) exec web sh

ps:
	$(COMPOSE) ps
