#!/usr/bin/env bash
set -euo pipefail

grep -E '^@' bibliography/references.bib \
  | sed -E 's/^@[^{]+\{([^,]+),/\1/' \
  | sort | uniq -d | while read -r DUP; do
    echo "Duplicate key: $DUP"
  done
