#!/bin/bash
set -e

# Default baseURL if not provided
BASE_URL="${BASE_URL:-/}"

echo "Building Hugo site with baseURL: $BASE_URL"

# Build Hugo site with runtime baseURL
cd /src

# Update baseURL in config.toml
sed -i "s|^baseURL = .*|baseURL = '$BASE_URL'|g" config.toml

hugo \
    --config config.toml,config/config.gh-pages.toml \
    --gc \
    --cleanDestinationDir

# Copy output to nginx
cp -r /src/public/* /usr/share/nginx/html/
chown -R www:www /usr/share/nginx/html

echo "Hugo build complete. Configuring nginx..."

# Create all required nginx directories in writable /tmp location
mkdir -p /tmp/nginx/conf.d \
         /tmp/nginx/client_body \
         /tmp/nginx/proxy \
         /tmp/nginx/fastcgi \
         /tmp/nginx/uwsgi \
         /tmp/nginx/scgi

# Prepare authentication - encode credentials as Base64 for Basic auth
ERPNEXT_API_KEY="${ERPNEXT_API_KEY:-dummy_key}"
ERPNEXT_API_SECRET="${ERPNEXT_API_SECRET:-dummy_secret}"
GATEWAY_ERPNEXT_API_URL="${GATEWAY_ERPNEXT_API_URL:-${ERPNEXT_API_URL:-https://api.do.kartoza.com/erpnext/kartoza-website/api}}"

export erpnext_api_auth_base64=$(echo -n "${ERPNEXT_API_KEY}:${ERPNEXT_API_SECRET}" | base64 -w 0)
export gateway_erpnext_api_url="${GATEWAY_ERPNEXT_API_URL}"
export gateway_erpnext_host=$(echo "${GATEWAY_ERPNEXT_API_URL}" | awk -F/ '{print $3}')

# Create temporary config with substituted variables in writable location
envsubst '${erpnext_api_auth_base64} ${gateway_erpnext_api_url} ${gateway_erpnext_host}' < /etc/nginx/templates/default.conf.template > /tmp/nginx/conf.d/default.conf

# Copy redirect rules (no envsubst needed - static config)
cp /etc/nginx/templates/redirects.conf /tmp/nginx/redirects.conf

echo "Starting nginx..."

# Start nginx
exec nginx -g "daemon off;"
