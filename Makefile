# Kartoza Hugo Website Makefile
# ==============================

.PHONY: help serve build clean sync-blogs sync-blogs-dry-run list-blogs

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

# ERPNext Blog Sync targets
sync-blogs:
	python3 scripts/fetch-erpnext-blogs.py

sync-blogs-dry-run:
	python3 scripts/fetch-erpnext-blogs.py --dry-run

list-blogs:
	python3 scripts/fetch-erpnext-blogs.py --list
