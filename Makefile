# Kartoza Hugo Website Makefile
# ==============================

COMPOSE := docker compose --env-file deployment/.env -f deployment/docker-compose.yml
COMPOSE_DEV := docker compose --env-file deployment/.env -f deployment/docker-compose.dev.yml

.PHONY: help serve build clean docker-serve docker-up docker-down docker-build docker-logs sync-blogs sync-blogs-dry-run list-blogs

# Default target
help:
	@echo "Kartoza Hugo Website"
	@echo "===================="
	@echo ""
	@echo "Available targets:"
	@echo "  serve             - Start Hugo development server"
	@echo "  build             - Build the Hugo site"
	@echo "  clean             - Clean build artifacts"
	@echo ""
	@echo "Docker:"
	@echo "  docker-serve      - Start Hugo dev server via Docker (http://localhost:1313)"
	@echo "  docker-up         - Build image and start site via Docker (http://localhost:8888)"
	@echo "  docker-down       - Stop and remove Docker containers"
	@echo "  docker-build      - Build the Docker image"
	@echo "  docker-logs       - Tail container logs"
	@echo ""
	@echo "ERPNext Blog Sync:"
	@echo "  sync-blogs        - Sync blogs from ERPNext (updates local files)"
	@echo "  sync-blogs-dry-run - Preview sync without making changes"
	@echo "  list-blogs        - List all blogs from ERPNext"
	@echo ""

# Hugo targets
serve:
	hugo server

build:
	hugo

clean:
	rm -rf public/

docker-serve:
	@test -f deployment/.env || cp deployment/.template.env deployment/.env
	$(COMPOSE) build
	$(COMPOSE_DEV) up --build

docker-up:
	@test -f deployment/.env || cp deployment/.template.env deployment/.env
	$(COMPOSE) up --build website

docker-down:
	$(COMPOSE) down

docker-build:
	$(COMPOSE) build

docker-logs:
	$(COMPOSE) logs -f

# ERPNext Blog Sync targets
sync-blogs:
	python3 scripts/fetch-erpnext-blogs.py

sync-blogs-dry-run:
	python3 scripts/fetch-erpnext-blogs.py --dry-run

list-blogs:
	python3 scripts/fetch-erpnext-blogs.py --list
