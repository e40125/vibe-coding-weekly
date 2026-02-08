#!/bin/bash
# Full pipeline: generate brief → build site → deploy to GitHub Pages
# Run this daily via cron

set -e  # Exit on error

cd "$(dirname "$0")"
echo "=================================="
echo "Vibe Coding Weekly Brief Pipeline"
echo "$(date)"
echo "=================================="

# Step 1: Activate venv
source venv/bin/activate

# Step 2: Generate new brief
echo ""
echo "Step 1: Generating brief..."
python3 weekly_brief.py

# Step 3: Build website
echo ""
echo "Step 2: Building website..."
python3 generate_site.py

# Step 4: Deploy to GitHub
echo ""
echo "Step 3: Deploying to GitHub..."
git add index.html style.css
git commit -m "Update brief: $(date +%Y-%m-%d)" || echo "No changes to commit"
git push origin main

echo ""
echo "=================================="
echo "✅ Done! Site updated."
echo "=================================="
