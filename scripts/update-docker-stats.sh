#!/usr/bin/env bash
#
# Update Docker image statistics from Docker Hub API
# This script fetches current pull counts and star counts for Kartoza Docker images
# and updates the frontmatter in the corresponding markdown files.
#
# Usage: ./scripts/update-docker-stats.sh
#
# Designed to run in GitHub Actions to keep stats current.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONTENT_DIR="${SCRIPT_DIR}/../content/docker"

# Color output for local runs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Format large numbers for display (e.g., 21831160 -> "21M+")
format_pulls() {
    local count=$1
    if [ "$count" -ge 1000000 ]; then
        echo "$((count / 1000000))M+"
    elif [ "$count" -ge 1000 ]; then
        echo "$((count / 1000))K+"
    else
        echo "$count"
    fi
}

# Update a single docker image file
update_image() {
    local md_file=$1
    local image_name=$2
    local file_path="${CONTENT_DIR}/${md_file}"

    if [ ! -f "$file_path" ]; then
        log_warn "File not found: $file_path"
        return 1
    fi

    log_info "Fetching stats for kartoza/${image_name}..."

    local response
    response=$(curl -s --max-time 10 "https://hub.docker.com/v2/repositories/kartoza/${image_name}/" 2>/dev/null) || {
        log_warn "Failed to fetch stats for kartoza/${image_name}"
        return 1
    }

    local pull_count star_count
    pull_count=$(echo "$response" | jq -r '.pull_count // 0')
    star_count=$(echo "$response" | jq -r '.star_count // 0')

    if [ "$pull_count" = "0" ] || [ "$pull_count" = "null" ]; then
        log_warn "Invalid pull count for kartoza/${image_name}"
        return 1
    fi

    local pulls_formatted
    pulls_formatted=$(format_pulls "$pull_count")

    # Use sed to update the pulls and stars in frontmatter
    sed -i "s/^pulls: \".*\"/pulls: \"${pulls_formatted}\"/" "$file_path"
    sed -i "s/^stars: .*/stars: ${star_count}/" "$file_path"

    log_info "Updated ${md_file}: pulls=${pulls_formatted}, stars=${star_count}"

    # Return the pull count for totaling
    echo "$pull_count"
}

main() {
    log_info "Starting Docker stats update..."

    # Check dependencies
    if ! command -v jq &> /dev/null; then
        log_error "jq is required but not installed. Install with: apt-get install jq"
        exit 1
    fi

    if ! command -v curl &> /dev/null; then
        log_error "curl is required but not installed."
        exit 1
    fi

    # Check content directory exists
    if [ ! -d "$CONTENT_DIR" ]; then
        log_error "Content directory not found: $CONTENT_DIR"
        exit 1
    fi

    local updated=0
    local failed=0
    local total_pulls=0
    local total_stars=0

    # Process each image
    local images=(
        "postgis.md:postgis"
        "geoserver.md:geoserver"
        "docker-osm.md:docker-osm"
        "mapproxy.md:mapproxy"
        "pg-backup.md:pg-backup"
        "qgis-server.md:qgis-server"
        "qgis-desktop.md:qgis-desktop"
    )

    for entry in "${images[@]}"; do
        local md_file="${entry%%:*}"
        local image_name="${entry##*:}"

        local pull_count
        if pull_count=$(update_image "$md_file" "$image_name"); then
            ((updated++)) || true
            total_pulls=$((total_pulls + pull_count))
        else
            ((failed++)) || true
        fi

        # Be nice to Docker Hub API - rate limiting
        sleep 2
    done

    echo ""
    log_info "========================================="
    log_info "Docker Stats Update Complete"
    log_info "========================================="
    log_info "Updated: ${updated} files"
    log_info "Failed: ${failed} files"
    log_info "Total pulls across all images: $(format_pulls $total_pulls)"

    if [ "$failed" -gt 0 ] && [ "$updated" -eq 0 ]; then
        exit 1
    fi
}

main "$@"
