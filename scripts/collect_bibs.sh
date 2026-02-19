#!/usr/bin/env bash
set -euo pipefail

CENTRAL="bibliography/references.bib"

mkdir -p bibliography
touch "$CENTRAL"

echo "Collecting session bib files…"

TMP=$(mktemp)

# Gather all paper.bib files
find sessions -name "paper.bib" | while read -r BIB; do
  echo "Processing $BIB"

  # Extract citekeys from this file
  grep -E '^@' "$BIB" | sed -E 's/^@[^{]+\{([^,]+),/\1/' | while read -r KEY; do

    if grep -q "{$KEY," "$CENTRAL"; then
      echo "  → already have $KEY"
    else
      echo "  → adding $KEY"
      awk -v key="$KEY" '
        BEGIN{found=0}
        $0 ~ "{"key"," {found=1}
        found {print}
        found && /^}/ {exit}
      ' "$BIB" >> "$TMP"
      echo "" >> "$TMP"
    fi

  done
done

cat "$TMP" >> "$CENTRAL"
rm "$TMP"

echo "Done."
