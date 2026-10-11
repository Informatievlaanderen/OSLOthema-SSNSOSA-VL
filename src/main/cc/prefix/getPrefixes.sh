#!/bin/bash
# Downloads the prefix.cc registry next to this script (used by ld-vocab via --prefix-registry).
# Plain http: the https certificate of prefix.cc has expired (December 2025).
set -euo pipefail
dir="$(cd "$(dirname "$0")" && pwd)"
tmp="$(mktemp)"
trap 'rm -f "$tmp"' EXIT
curl -fsS -o "$tmp" http://prefix.cc/popular/all.file.ttl
# Keep the previous file if the download is not a list of @prefix declarations.
if ! head -1 "$tmp" | grep -q '^@prefix'; then
  echo "Download is not Turtle; $dir/prefix.cc.ttl left unchanged" >&2
  exit 1
fi
chmod 644 "$tmp"
mv "$tmp" "$dir/prefix.cc.ttl"
echo "$(grep -c '^@prefix' "$dir/prefix.cc.ttl") prefixes written to $dir/prefix.cc.ttl"
