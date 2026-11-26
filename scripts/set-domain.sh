#!/bin/sh
# Replace the {{SITE_URL}} placeholder with the live domain, e.g.
#   sh scripts/set-domain.sh https://www.theeleven.farm
set -e
[ -n "$1" ] || { echo "usage: set-domain.sh https://www.example.com"; exit 1; }
cd "$(dirname "$0")/../website"
grep -rl '{{SITE_URL}}' --include='*.html' --include='*.xml' --include='*.txt' . | while read -r f; do
  sed -i.bak "s#{{SITE_URL}}#$1#g" "$f" && rm "$f.bak"
done
echo "Domain set to $1"
