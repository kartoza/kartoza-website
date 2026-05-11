FROM kartoza-website:base

USER root
COPY deployment/docker-dev/entrypoint.sh /entrypoint.dev.sh
RUN chmod +x /entrypoint.dev.sh && \
    sed -i '/echo "Starting nginx\.\.\."/,/exec nginx -g "daemon off;"/d' /entrypoint.sh

USER www
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget -q --spider http://localhost:8080/health || exit 1

ENTRYPOINT ["/bin/bash", "-c", "/entrypoint.sh && /entrypoint.dev.sh"]