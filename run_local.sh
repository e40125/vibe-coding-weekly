#!/bin/bash
# Generate brief + build site locally (no git push)

cd "$(dirname "$0")"
source venv/bin/activate

echo "Generating brief..."
python3 weekly_brief.py

echo ""
echo "Building website..."
python3 generate_site.py

echo ""
echo "Opening in browser..."
open index.html
