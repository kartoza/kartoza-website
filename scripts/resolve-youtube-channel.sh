#!/usr/bin/env bash
#
# Resolve a YouTube @handle to its channel ID (UC...) and uploads playlist
# ID (UU...). Used to keep content/youtube/_index.md's `uploadsPlaylist`
# field up-to-date if the Kartoza channel ID ever changes.
#
# Usage:
#   scripts/resolve-youtube-channel.sh                 # defaults to @KartozaGeo
#   scripts/resolve-youtube-channel.sh @SomeOtherHandle

set -eu

HANDLE="${1:-@KartozaGeo}"
URL="https://www.youtube.com/${HANDLE}"

HTML=$(curl -fsSL \
    -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36" \
    -H "Accept-Language: en-US,en;q=0.9" \
    "${URL}")

# YouTube has used several JSON keys for the channel ID over the years;
# try them in order of likelihood.
CHANNEL_ID=$(
    {
        echo "${HTML}" | grep -oE '"channelId":"UC[A-Za-z0-9_-]{22}"'
        echo "${HTML}" | grep -oE '"externalId":"UC[A-Za-z0-9_-]{22}"'
        echo "${HTML}" | grep -oE '/channel/UC[A-Za-z0-9_-]{22}'
    } \
    | head -1 \
    | grep -oE 'UC[A-Za-z0-9_-]{22}'
)

if [ -z "${CHANNEL_ID}" ]; then
    echo "ERROR: could not extract a channel ID from ${URL}" >&2
    exit 1
fi

UPLOADS_PLAYLIST="UU${CHANNEL_ID:2}"

cat <<EOF
Handle:           ${HANDLE}
Channel ID:       ${CHANNEL_ID}
Uploads playlist: ${UPLOADS_PLAYLIST}
Embed URL:        https://www.youtube.com/embed/videoseries?list=${UPLOADS_PLAYLIST}
EOF
