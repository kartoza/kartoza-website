#!/usr/bin/env bash
#
# Welcome screen rendered when entering `nix develop` for the Kartoza Hugo site.
#
# Renders the Kartoza logo (via chafa with the kitty graphics protocol when
# available, otherwise a Unicode banner), then prints a categorised, colourful
# overview of the commands and integrations available in the dev shell.
#
# Designed to be sourced or executed from the flake.nix shellHook. Reads no
# arguments. Writes to stdout only.

set -u

# ---------------------------------------------------------------------------
# Colours / styles
# ---------------------------------------------------------------------------
if [ -t 1 ]; then
    C_RESET=$'\033[0m'
    C_BOLD=$'\033[1m'
    C_DIM=$'\033[2m'
    C_GREEN=$'\033[38;5;78m'        # Kartoza-ish green
    C_DARK_GREEN=$'\033[38;5;28m'
    C_ORANGE=$'\033[38;5;214m'
    C_BLUE=$'\033[38;5;75m'
    C_PURPLE=$'\033[38;5;141m'
    C_GREY=$'\033[38;5;245m'
    C_PINK=$'\033[38;5;205m'
else
    C_RESET="" C_BOLD="" C_DIM="" C_GREEN="" C_DARK_GREEN=""
    C_ORANGE="" C_BLUE="" C_PURPLE="" C_GREY="" C_PINK=""
fi

# ---------------------------------------------------------------------------
# Logo rendering
# ---------------------------------------------------------------------------
render_logo() {
    local logo="static/img/kartoza-logo.png"
    if [ ! -f "$logo" ]; then
        render_ascii_banner
        return
    fi

    if command -v chafa >/dev/null 2>&1 && [ "${TERM:-}" = "xterm-kitty" ]; then
        # Kitty graphics protocol — true image, scaled to 40 cols x 12 rows.
        chafa --format=kitty --size=40x12 --align=center "$logo" 2>/dev/null \
            || render_ascii_banner
    else
        render_ascii_banner
    fi
}

render_ascii_banner() {
    cat <<'BANNER'
   ╔═══════════════════════════════════════════════════════════╗
   ║                                                           ║
   ║      ██╗  ██╗ █████╗ ██████╗ ████████╗ ██████╗ ███████╗   ║
   ║      ██║ ██╔╝██╔══██╗██╔══██╗╚══██╔══╝██╔═══██╗╚══███╔╝   ║
   ║      █████╔╝ ███████║██████╔╝   ██║   ██║   ██║  ███╔╝    ║
   ║      ██╔═██╗ ██╔══██║██╔══██╗   ██║   ██║   ██║ ███╔╝     ║
   ║      ██║  ██╗██║  ██║██║  ██║   ██║   ╚██████╔╝███████╗   ║
   ║      ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚══════╝   ║
   ║                                                           ║
   ╚═══════════════════════════════════════════════════════════╝
BANNER
}

# ---------------------------------------------------------------------------
# Section helpers
# ---------------------------------------------------------------------------
section() {
    local icon="$1" title="$2" colour="$3"
    printf '\n%s%s%s %s%s%s\n' \
        "$colour" "$icon" "$C_RESET" \
        "$C_BOLD$colour" "$title" "$C_RESET"
    printf '%s%s%s\n' "$C_DIM" \
        "─────────────────────────────────────────────────────────────" \
        "$C_RESET"
}

cmd() {
    # cmd <command> <description>
    printf '  %s%-36s%s %s%s%s\n' \
        "$C_GREEN" "$1" "$C_RESET" \
        "$C_GREY" "$2" "$C_RESET"
}

note() {
    printf '  %s%s%s\n' "$C_DIM" "$1" "$C_RESET"
}

# ---------------------------------------------------------------------------
# Main render
# ---------------------------------------------------------------------------
echo ""
render_logo
echo ""
printf '%s%s%s\n' "$C_BOLD$C_GREEN" \
    "       Kartoza Hugo Website  —  Development Environment" \
    "$C_RESET"
printf '%s%s%s\n' "$C_DIM" \
    "             Made with 💗 by Kartoza — https://kartoza.com" \
    "$C_RESET"

section "🌍" "Hugo" "$C_GREEN"
cmd "hugo server"            "Start the live-reloading dev server"
cmd "hugo"                   "Build the static site into ./public"
cmd "make serve"             "Hugo server with git version env injected"
cmd "make build"             "Production build with git version env"
cmd "make clean"             "Remove ./public build artefacts"

section "🪛" "VSCode integration" "$C_BLUE"
cmd "./vscode.sh"            "Launch VSCode with the project profile"
note "Uses a dedicated profile ('QGISWebSite') and a project-local"
note "extensions directory (.vscode-extensions/), so your global VSCode"
note "setup stays untouched. Pre-pins extensions for Hugo, Playwright,"
note "Python, Prettier, GitLens, spell-checking and more."

section "🎭" "Playwright (E2E tests)" "$C_PURPLE"
cmd "cd playwright/ci-test && npm test"  "Run the full e2e suite"
note "Browsers come from the flake — PLAYWRIGHT_BROWSERS_PATH is preset."

section "📰" "ERPNext content sync" "$C_ORANGE"
cmd "make sync-all"          "Sync every content type from ERPNext"
cmd "make sync-blogs"        "Sync blog articles"
cmd "make sync-team"         "Sync team member pages"
cmd "make sync-portfolio"    "Sync portfolio items"
cmd "make sync-training"     "Sync training courses"
cmd "make sync-pages"        "Sync standalone pages (policies etc.)"
cmd "make sync-jobs"         "Sync job opportunities"
note "Add '-dry-run' (e.g. make sync-blogs-dry-run) to preview without writing."
note "Add 'list-' (e.g. make list-blogs) to see what's available on ERPNext."

section "🐳" "Docker" "$C_BLUE"
cmd "make docker-serve"      "Hugo dev server in Docker (:1313)"
cmd "make docker-up"         "Production-style site in Docker (:8888)"
cmd "make docker-down"       "Stop and remove containers"
cmd "make docker-logs"       "Tail container logs"

section "🚀" "Nix apps (flake)" "$C_DARK_GREEN"
cmd "nix run .#website"          "Serve built site via Python's http.server"
cmd "nix run .#sync-blogs"       "Run blog sync via the flake's pinned Python"
cmd "nix run .#list-blogs"       "List ERPNext blogs via the flake"
cmd "nix build .#website"        "Build the site reproducibly via Nix"

section "✅" "Quality" "$C_PINK"
cmd "markdownlint '**/*.md'" "Lint Markdown content"
cmd "prettier --check ."     "Check formatting"
cmd "cspell '**/*.md'"       "Spell-check Markdown"

section "💗" "Support Kartoza" "$C_PINK"
note "Kartoza:  https://kartoza.com"
note "Donate:   https://github.com/sponsors/kartoza"
note "GitHub:   https://github.com/kartoza/Kartoza-Hugo"

printf '\n%s%s%s\n\n' "$C_DIM" \
    "Tip: run 'make help' for the full Makefile target list." \
    "$C_RESET"
