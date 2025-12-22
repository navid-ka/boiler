# ===============================
# Project Makefile
# ===============================

PROJECT_NAME := amphora
COMPOSE := docker compose

# -------------------------------
# Core commands
# -------------------------------
all: up

up:
	$(COMPOSE) up -d

.PHONY: help up down restart logs ps build rebuild

help:
	@echo ""
	@echo "Available commands:"
	@echo "  make up           Start all services"
	@echo "  make down         Stop all services"
	@echo "  make restart      Restart all services"
	@echo "  make build        Build containers"
	@echo "  make rebuild      Rebuild containers (no cache)"
	@echo "  make logs         Follow logs"
	@echo "  make ps           Show running containers"
	@echo "  make prune	       Delete DB"
	@echo ""


down:
	$(COMPOSE) down

restart:
	$(COMPOSE) down
	$(COMPOSE) up -d

build:
	$(COMPOSE) up -d --build

rebuild:
	$(COMPOSE) build --no-cache

logs:
	$(COMPOSE) logs -f

ps:
	$(COMPOSE) ps

# -------------------------------
# Backend (FastAPI)
# -------------------------------

.PHONY: backend backend-shell backend-logs backend-test

backend:
	$(COMPOSE) up -d backend

backend-shell:
	$(COMPOSE) exec backend sh

backend-logs:
	$(COMPOSE) logs -f backend

backend-test:
	$(COMPOSE) exec -e PYTHONPATH=/app backend pytest -v

# -------------------------------
# Frontend (Vite / React)
# -------------------------------

.PHONY: frontend frontend-shell frontend-logs frontend-install

frontend:
	$(COMPOSE) up -d frontend

frontend-shell:
	$(COMPOSE) exec frontend sh

frontend-logs:
	$(COMPOSE) logs -f frontend

frontend-install:
	$(COMPOSE) exec frontend npm install

# -------------------------------
# DynamoDB
# -------------------------------

.PHONY: db db-logs

db:
	$(COMPOSE) up -d dynamodb-local

db-logs:
	$(COMPOSE) logs -f dynamodb-local

# -------------------------------
# Nginx
# -------------------------------

.PHONY: nginx nginx-logs

nginx:
	$(COMPOSE) up -d nginx

nginx-logs:
	$(COMPOSE) logs -f nginx

# -------------------------------
# Clean up
# -------------------------------

.PHONY: clean prune

clean:
	$(COMPOSE) down -v

prune:
	docker system prune -af --volumes
