#!/usr/bin/env bash
# Build the site and publish it for sandbox.kartoza.com (served by nginx from a static directory).
#
#   scripts/deploy-sandbox.sh [destination]      default destination: /var/www/sandbox-kartoza
#
# The site is built with --baseURL /, so every link Hugo generates (absURL, .Permalink, ...) is
# root-relative: it works on whatever host serves it, instead of pointing back at kartoza.com.
# config.toml keeps the production baseURL; only this build overrides it.
# --environment sandbox turns off analytics (Google Tag Manager only loads for 'production').
set -euo pipefail

cd "$(dirname "$0")/.."
DEST="${1:-/var/www/sandbox-kartoza}"

if command -v hugo >/dev/null 2>&1; then
    HUGO=(hugo)
else
    HUGO=(nix --extra-experimental-features nix-command --extra-experimental-features flakes shell nixpkgs#hugo -c hugo)
fi

if [ ! -d "$DEST" ]; then
    sudo mkdir -p "$DEST"
    sudo chown "$(id -un):$(id -gn)" "$DEST"
fi

HUGO_PARAMS_GITCOMMIT="$(git rev-parse --short HEAD)" \
HUGO_PARAMS_GITVERSION="$(git describe --tags --always)" \
"${HUGO[@]}" --environment sandbox --baseURL / --destination "$DEST" --cleanDestinationDir --gc

echo "Built into $DEST"
