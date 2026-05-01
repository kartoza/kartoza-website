# Minimal Nginx runtime with Hugo
FROM nginx:1.28.2-alpine-slim

# Hugo version
ARG HUGO_VERSION=0.156.0

# Install Hugo, upgrade packages, and install essentials
RUN apk upgrade --no-cache --available && \
    apk add --no-cache ca-certificates bash wget libc6-compat libstdc++ gettext && \
    wget -qO- https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz | tar xz -C /usr/local/bin/ && \
    apk del wget && \
    rm -rf /var/cache/apk/* /tmp/*

# Copy source files for runtime Hugo build
COPY . /src

COPY deployment/nginx/sites-enabled/nginx.conf /etc/nginx/nginx.conf
COPY deployment/nginx/sites-enabled/default.conf /etc/nginx/templates/default.conf.template
COPY deployment/nginx/sites-enabled/redirects.conf /etc/nginx/templates/redirects.conf

# Create entrypoint scripts
COPY deployment/docker/entrypoint.sh /entrypoint.sh
COPY deployment/docker/entrypoint.dev.sh /entrypoint.dev.sh
RUN chmod +x /entrypoint.sh /entrypoint.sh

# Security hardening
RUN addgroup -g 1001 -S www && \
    adduser -u 1001 -S www -G www && \
    mkdir -p /usr/share/nginx/html /var/cache/nginx /tmp \
             /var/lib/nginx/logs /var/lib/nginx/tmp && \
    chown -R www:www /usr/share/nginx/html /var/cache/nginx /src /tmp \
                     /var/lib/nginx /var/log/nginx && \
    touch /var/run/nginx.pid && \
    chown www:www /var/run/nginx.pid

USER www
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget -q --spider http://localhost:8080/health || exit 1

ENTRYPOINT ["/entrypoint.sh"]
