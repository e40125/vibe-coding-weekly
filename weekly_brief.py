#!/usr/bin/env python3
"""
Weekly AI News Scraper for Taiwan Vibe Coding Audience
Fetches news from key outlets and summarizes via Claude CLI
"""

import feedparser
import subprocess
import json
import sys
from datetime import datetime, timedelta

# === CONFIGURE YOUR SOURCES HERE ===
RSS_FEEDS = {
    # Taiwan Tech Media
    "TechNews 科技新報": "https://technews.tw/feed/",
    "數位時代": "https://www.bnext.com.tw/rss",
    "iThome": "https://www.ithome.com.tw/rss",

    # International AI
    "OpenAI Blog": "https://openai.com/blog/rss.xml",
    "Anthropic": "https://www.anthropic.com/rss.xml",
    "The Verge AI": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
}

# How many days back to look
DAYS_BACK = 7

# === CLAUDE PROMPT ===
SUMMARY_PROMPT = """你是一個專門為台灣 Vibe Coding 愛好者撰寫週報的編輯。
Vibe Coding = 用 AI 工具（Claude, ChatGPT, Cursor 等）來寫程式，不需要深厚的技術背景。

以下是本週的 AI 新聞，請用繁體中文整理成週報格式：

【Vibe Coding 週報】{date}

🔥 本週重點 (最多 2 則)
- 只列出對 Vibe Coder 真正重要的更新

🛠 實用更新
- Claude/ChatGPT/Cursor 等工具的更新
- 對寫程式有幫助的新功能

📚 值得一試
- 本週可以試試的新工具或技巧

🙅 可以忽略
- 本週發布但對 Vibe Coder 不重要的東西（簡單列出即可）

規則：
1. 保持簡短，整份週報閱讀時間 < 2 分鐘
2. 用口語化的繁體中文
3. 專注於實用性，不是新聞報導
4. 如果某個來源沒有相關新聞，就跳過

---
本週新聞資料：

{news_content}
"""


def fetch_feeds():
    """Fetch all RSS feeds and filter by date"""
    cutoff_date = datetime.now() - timedelta(days=DAYS_BACK)
    all_articles = []

    for source_name, feed_url in RSS_FEEDS.items():
        print(f"Fetching: {source_name}...")
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:10]:  # Max 10 per source
                # Parse date
                published = None
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    published = datetime(*entry.published_parsed[:6])
                elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                    published = datetime(*entry.updated_parsed[:6])

                # Filter by date
                if published and published < cutoff_date:
                    continue

                article = {
                    "source": source_name,
                    "title": entry.get('title', 'No title'),
                    "link": entry.get('link', ''),
                    "summary": entry.get('summary', '')[:500],  # Truncate
                    "date": published.strftime("%Y-%m-%d") if published else "Unknown"
                }
                all_articles.append(article)
        except Exception as e:
            print(f"  Error fetching {source_name}: {e}")

    return all_articles


def format_for_claude(articles):
    """Format articles into text for Claude"""
    if not articles:
        return "本週沒有找到相關新聞。"

    output = []
    for article in articles:
        output.append(f"【{article['source']}】{article['date']}")
        output.append(f"標題: {article['title']}")
        output.append(f"連結: {article['link']}")
        if article['summary']:
            # Clean HTML tags roughly
            summary = article['summary'].replace('<p>', '').replace('</p>', '')
            output.append(f"摘要: {summary[:300]}...")
        output.append("---")

    return "\n".join(output)


def call_claude(prompt):
    """Call Claude CLI with the prompt"""
    print("\nCalling Claude CLI...")
    try:
        result = subprocess.run(
            ["claude", "-p", prompt],
            capture_output=True,
            text=True,
            timeout=120
        )
        return result.stdout
    except FileNotFoundError:
        print("Error: Claude CLI not found. Make sure 'claude' is in your PATH.")
        print("Install: npm install -g @anthropic-ai/claude-code")
        return None
    except subprocess.TimeoutExpired:
        print("Error: Claude CLI timed out")
        return None


def main():
    print("=" * 50)
    print("Weekly AI Brief Generator")
    print(f"Fetching news from the past {DAYS_BACK} days")
    print("=" * 50)

    # Fetch news
    articles = fetch_feeds()
    print(f"\nFound {len(articles)} articles")

    if not articles:
        print("No articles found. Check your RSS feeds.")
        return

    # Format content
    news_content = format_for_claude(articles)

    # Build prompt
    today = datetime.now().strftime("%Y.%m.%d")
    full_prompt = SUMMARY_PROMPT.format(date=today, news_content=news_content)

    # Save raw data for debugging
    with open("raw_news.txt", "w", encoding="utf-8") as f:
        f.write(news_content)
    print("Raw news saved to: raw_news.txt")

    # Call Claude
    result = call_claude(full_prompt)

    if result:
        # Save output
        output_file = f"weekly_brief_{today.replace('.', '_')}.md"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"\n✅ Brief saved to: {output_file}")
        print("\n" + "=" * 50)
        print(result)

        # Send to LINE if --send flag is passed
        if "--send" in sys.argv:
            print("\n" + "=" * 50)
            print("Sending to LINE...")
            try:
                from line_bot import send_broadcast
                if send_broadcast(result):
                    print("✅ Sent to LINE subscribers!")
                else:
                    print("❌ LINE send failed")
            except ImportError:
                print("line_bot.py not found")
            except Exception as e:
                print(f"LINE error: {e}")
    else:
        print("\nFailed to generate brief. Check Claude CLI.")
        print("You can manually run:")
        print("  cat raw_news.txt | claude -p 'Summarize this...'")


if __name__ == "__main__":
    main()
