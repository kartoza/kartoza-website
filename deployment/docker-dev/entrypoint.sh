#!/bin/bash
# Override location / with Hugo dev server proxy
awk '
/^    # Main location block$/ { skip=1; depth=0; next }
skip && /[{]/ { depth++ }
skip && /[}]/ {
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

echo "Starting nginx..."
exec nginx -g "daemon off;"