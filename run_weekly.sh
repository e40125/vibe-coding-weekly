#!/bin/bash
# Run the weekly brief generator
# Schedule this with cron for automatic weekly runs:
# crontab -e
# 0 18 * * 0 /path/to/run_weekly.sh  (runs every Sunday at 6pm)

cd "$(dirname "$0")"
python3 weekly_brief.py
