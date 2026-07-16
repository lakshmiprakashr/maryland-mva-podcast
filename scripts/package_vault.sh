#!/bin/bash
# Package Obsidian vault for distribution

set -e

echo "============================================"
echo "MARYLAND MVA PODCAST - PACKAGE VAULT"
echo "============================================"

# Run vault packaging
python3 scripts/package_vault.py

# Create ZIP
echo ""
echo "Creating distribution ZIP..."
cd "$(dirname "$0")/.."
zip -r obsidian-vault.zip obsidian-vault/ -x "obsidian-vault/.obsidian/workspace*"

echo ""
echo "============================================"
echo "PACKAGING COMPLETE"
echo "============================================"
echo ""
echo "Output files:"
echo "  obsidian-vault/     - Ready to open in Obsidian"
echo "  obsidian-vault.zip  - Distribution archive"
echo ""
echo "To use:"
echo "  1. Unzip obsidian-vault.zip"
echo "  2. Open Obsidian"
echo "  3. Open folder as vault"
echo "  4. Select the obsidian-vault folder"
