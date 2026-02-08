#!/usr/bin/env python3
"""
LINE Bot integration for Weekly Brief
Sends the generated brief to all LINE subscribers

Setup:
1. Create LINE Official Account: https://manager.line.biz/
2. Get Channel Access Token from LINE Developers Console
3. Set your CHANNEL_ACCESS_TOKEN below or in environment variable
"""

import os
import requests
import json

# === CONFIGURATION ===
# Option 1: Set directly here
CHANNEL_ACCESS_TOKEN = "YOUR_CHANNEL_ACCESS_TOKEN_HERE"

# Option 2: Use environment variable (more secure)
# CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")

LINE_BROADCAST_URL = "https://api.line.me/v2/bot/message/broadcast"


def send_broadcast(message: str) -> bool:
    """
    Send a message to ALL subscribers of your LINE Official Account
    Free tier: 500 messages/month
    """
    if CHANNEL_ACCESS_TOKEN == "YOUR_CHANNEL_ACCESS_TOKEN_HERE":
        print("Error: Set your LINE Channel Access Token first!")
        print("1. Go to https://manager.line.biz/")
        print("2. Create an Official Account")
        print("3. Enable Messaging API")
        print("4. Get Channel Access Token")
        return False

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}"
    }

    # LINE has 5000 char limit per message, split if needed
    messages = split_message(message, max_length=4500)

    for msg in messages:
        payload = {
            "messages": [
                {
                    "type": "text",
                    "text": msg
                }
            ]
        }

        response = requests.post(
            LINE_BROADCAST_URL,
            headers=headers,
            data=json.dumps(payload)
        )

        if response.status_code == 200:
            print(f"✅ Message sent successfully")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            return False

    return True


def split_message(text: str, max_length: int = 4500) -> list:
    """Split long messages at line breaks"""
    if len(text) <= max_length:
        return [text]

    messages = []
    current = ""

    for line in text.split("\n"):
        if len(current) + len(line) + 1 > max_length:
            messages.append(current.strip())
            current = line + "\n"
        else:
            current += line + "\n"

    if current.strip():
        messages.append(current.strip())

    return messages


def send_brief_file(filepath: str) -> bool:
    """Read a brief file and send it"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        return send_broadcast(content)
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return False


# === TEST ===
if __name__ == "__main__":
    # Test with the latest brief
    import glob

    briefs = sorted(glob.glob("weekly_brief_*.md"))
    if briefs:
        latest = briefs[-1]
        print(f"Sending: {latest}")
        send_brief_file(latest)
    else:
        print("No brief files found. Run weekly_brief.py first.")
