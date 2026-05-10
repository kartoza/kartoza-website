# Kartoza Hugo Website Makefile
# ==============================

COMPOSE := docker compose --env-file deployment/.env -f deployment/docker-compose.yml
COMPOSE_DEV := docker compose --env-file deployment/.env -f deployment/docker-compose.dev.yml

.PHONY: help serve build clean docker-serve docker-up docker-down docker-build docker-logs \
       sync-all sync-blogs sync-blogs-dry-run list-blogs \
       sync-team sync-team-dry-run list-team \
       sync-portfolio sync-portfolio-dry-run list-portfolio \
       sync-training sync-training-dry-run list-training \
       sync-pages sync-pages-dry-run list-pages \
       sync-jobs sync-jobs-dry-run list-jobs

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
	@echo "ERPNext Content Sync:"
	@echo "  sync-all              - Sync all content from ERPNext"
	@echo ""
	@echo "  sync-blogs            - Sync blog articles from ERPNext"
	@echo "  sync-blogs-dry-run    - Preview blog sync without changes"
	@echo "  list-blogs            - List available blogs on ERPNext"
	@echo ""
	@echo "  sync-team             - Sync team members from ERPNext"
	@echo "  sync-team-dry-run     - Preview team sync without changes"
	@echo "  list-team             - List team members on ERPNext"
	@echo ""
	@echo "  sync-portfolio        - Sync portfolio items from ERPNext"
	@echo "  sync-portfolio-dry-run - Preview portfolio sync without changes"
	@echo "  list-portfolio        - List portfolio items on ERPNext"
	@echo ""
	@echo "  sync-training         - Sync training courses from ERPNext"
	@echo "  sync-training-dry-run - Preview training sync without changes"
	@echo "  list-training         - List training courses on ERPNext"
	@echo ""
	@echo "  sync-pages            - Sync standalone pages from ERPNext"
	@echo "  sync-pages-dry-run    - Preview pages sync without changes"
	@echo "  list-pages            - List pages to sync from ERPNext"
	@echo ""
	@echo "  sync-jobs             - Sync job opportunities from ERPNext"
	@echo "  sync-jobs-dry-run     - Preview jobs sync without changes"
	@echo "  list-jobs             - List job openings on ERPNext"
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

# ERPNext Content Sync targets

# Sync all content types
sync-all:
	python3 scripts/sync-erpnext-content.py

# Blog articles
sync-blogs:
	python3 scripts/fetch-erpnext-blogs.py

sync-blogs-dry-run:
	python3 scripts/fetch-erpnext-blogs.py --dry-run

list-blogs:
	python3 scripts/fetch-erpnext-blogs.py --list

# Team members
sync-team:
	python3 scripts/fetch-erpnext-team.py

sync-team-dry-run:
	python3 scripts/fetch-erpnext-team.py --dry-run

list-team:
	python3 scripts/fetch-erpnext-team.py --list

# Portfolio items
sync-portfolio:
	python3 scripts/fetch-erpnext-portfolio.py

sync-portfolio-dry-run:
	python3 scripts/fetch-erpnext-portfolio.py --dry-run

list-portfolio:
	python3 scripts/fetch-erpnext-portfolio.py --list

# Training courses
sync-training:
	python3 scripts/fetch-erpnext-training.py

sync-training-dry-run:
	python3 scripts/fetch-erpnext-training.py --dry-run

list-training:
	python3 scripts/fetch-erpnext-training.py --list

# Standalone pages (policies etc.)
sync-pages:
	python3 scripts/fetch-erpnext-pages.py

sync-pages-dry-run:
	python3 scripts/fetch-erpnext-pages.py --dry-run

list-pages:
	python3 scripts/fetch-erpnext-pages.py --list

# Job opportunities
sync-jobs:
	python3 scripts/fetch-erpnext-jobs.py

sync-jobs-dry-run:
	python3 scripts/fetch-erpnext-jobs.py --dry-run

list-jobs:
	python3 scripts/fetch-erpnext-jobs.py --list
