#!/usr/bin/env bash
set -eu

PROFILE="${1:-abtest-jev-dev17}"
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
DEST="$HOME/.hermes/profiles/$PROFILE/plugins/hermes-jev"
STAMP=$(date +%Y%m%dT%H%M%S)

mkdir -p "$(dirname "$DEST")"
if [ -e "$DEST" ]; then
  BACKUP="${DEST}.pre-dev17-${STAMP}"
  mv "$DEST" "$BACKUP"
  echo "Existing plugin preserved at: $BACKUP"
fi
mkdir -p "$DEST"
cp -a "$ROOT"/. "$DEST"/
rm -rf "$DEST/.pytest_cache" "$DEST/__pycache__"

hermes -p "$PROFILE" plugins enable hermes-jev
printf 'Installed Hermes-Jev %s into %s\n' "$(python3 -c "import sys; sys.path.insert(0, '$DEST'); from hermes_jev.provenance import VERSION; print(VERSION)")" "$DEST"
