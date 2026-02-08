#!/usr/bin/env python3
"""
Converts the latest weekly brief (markdown) into index.html
"""

import glob
import re
from datetime import datetime
from pathlib import Path

# HTML template
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vibe Coding 週報 | 台灣 AI 建造者週報</title>
    <meta name="description" content="每週精選 AI 工具更新，專為用 AI 寫程式的台灣人準備">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>Vibe Coding 週報</h1>
            <p class="subtitle">每週精選 AI 工具更新，專為用 AI 寫程式的你準備</p>
            <p class="date">最後更新：{date}</p>
        </header>

        <main id="content">
{content}
        </main>

        <footer>
            <p>自動產生 by Claude CLI</p>
        </footer>
    </div>
</body>
</html>
'''


def markdown_to_html(md_text: str) -> str:
    """
    Simple markdown to HTML converter
    Handles: headers, bold, lists, links, paragraphs
    """
    lines = md_text.split('\n')
    html_lines = []
    in_list = False

    for line in lines:
        stripped = line.strip()

        # Skip the title line if it starts with #
        if stripped.startswith('# 【'):
            continue

        # Headers
        if stripped.startswith('## '):
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            # Remove emoji from header, we add via CSS
            header_text = stripped[3:].strip()
            # Remove leading emoji if present
            header_text = re.sub(r'^[🔥🛠📚🙅]\s*', '', header_text)
            html_lines.append(f'<h2>{header_text}</h2>')

        # Horizontal rule
        elif stripped == '---':
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append('<hr>')

        # List items
        elif stripped.startswith('- ') or stripped.startswith('* '):
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            item_text = stripped[2:]
            item_text = convert_inline(item_text)
            html_lines.append(f'<li>{item_text}</li>')

        # Empty line
        elif not stripped:
            if in_list:
                html_lines.append('</ul>')
                in_list = False

        # Regular paragraph
        elif stripped:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            para_text = convert_inline(stripped)
            html_lines.append(f'<p>{para_text}</p>')

    if in_list:
        html_lines.append('</ul>')

    return '\n            '.join(html_lines)


def convert_inline(text: str) -> str:
    """Convert inline markdown: bold, links"""
    # Bold: **text** → <strong>text</strong>
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)

    # Links: [text](url) → <a href="url">text</a>
    text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', text)

    # Inline code: `code` → <code>code</code>
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)

    return text


def get_latest_brief() -> tuple[str, str]:
    """Find the most recent brief file and return (content, date)"""
    briefs = sorted(glob.glob('weekly_brief_*.md'))

    if not briefs:
        return None, None

    latest = briefs[-1]
    print(f"Using: {latest}")

    # Extract date from filename: weekly_brief_2026_02_08.md
    match = re.search(r'weekly_brief_(\d{4})_(\d{2})_(\d{2})', latest)
    if match:
        date_str = f"{match.group(1)}.{match.group(2)}.{match.group(3)}"
    else:
        date_str = datetime.now().strftime("%Y.%m.%d")

    with open(latest, 'r', encoding='utf-8') as f:
        content = f.read()

    return content, date_str


def generate_site():
    """Main function: convert latest brief to index.html"""
    print("=" * 50)
    print("Generating website from latest brief")
    print("=" * 50)

    # Get latest brief
    md_content, date_str = get_latest_brief()

    if not md_content:
        print("No brief files found. Run weekly_brief.py first.")
        return False

    # Convert to HTML
    html_content = markdown_to_html(md_content)

    # Build full page
    full_html = HTML_TEMPLATE.format(
        date=date_str,
        content=html_content
    )

    # Write index.html
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(full_html)

    print(f"✅ Generated index.html (updated: {date_str})")
    print("\nTo preview locally:")
    print("  open index.html")
    print("  # or")
    print("  python3 -m http.server 8000")

    return True


if __name__ == "__main__":
    generate_site()
