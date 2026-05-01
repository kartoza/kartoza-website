#!/bin/bash
set -e

mkdir -p /tmp/nginx/conf.d \
         /tmp/nginx/client_body \
         /tmp/nginx/proxy \
         /tmp/nginx/fastcgi \
         /tmp/nginx/uwsgi \
         /tmp/nginx/scgi

# Use same env var setup as production entrypoint
ERPNEXT_API_KEY="${ERPNEXT_API_KEY:-dummy_key}"
ERPNEXT_API_SECRET="${ERPNEXT_API_SECRET:-dummy_secret}"
GATEWAY_ERPNEXT_API_URL="${GATEWAY_ERPNEXT_API_URL:-https://api.do.kartoza.com/erpnext/kartoza-website/api}"

export erpnext_api_auth_base64=$(echo -n "${ERPNEXT_API_KEY}:${ERPNEXT_API_SECRET}" | base64 -w 0)
export gateway_erpnext_api_url="${GATEWAY_ERPNEXT_API_URL}"

# Process production nginx template (same as production entrypoint)
envsubst '${erpnext_api_auth_base64} ${gateway_erpnext_api_url}' \
    < /etc/nginx/templates/default.conf.template \
    > /tmp/nginx/conf.d/default.conf

# Copy redirect rules from production
cp /etc/nginx/templates/redirects.conf /tmp/nginx/redirects.conf

# Override location / with Hugo dev server proxy
awk '
/^    # Main location block$/ { skip=1; depth=0; next }
skip && /{/ { depth++ }
skip && /}/ {
    depth--
    if (depth == 0) {
        skip=0
        while ((getline line < "/etc/nginx/sites-enabled-dev/default.dev.conf") > 0)
            print line
        next
    }
}
!skip { print }
' /tmp/nginx/conf.d/default.conf > /tmp/default_patched.conf
mv /tmp/default_patched.conf /tmp/nginx/conf.d/default.conf

echo "Starting Hugo dev server..."
cd /src
hugo server --bind 127.0.0.1 --port 8000 \
    --config config.toml,config/config.dev.toml \
    --baseURL "http://localhost:${DEV_PORT:-8080}" \
    --appendPort=false \
    --liveReloadPort="${DEV_PORT:-8080}" &

echo "Starting nginx..."
exec nginx -g "daemon off;"