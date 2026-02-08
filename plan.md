# Plan: Daily AI Brief Website

## Goal
A simple website that displays the latest Vibe Coding weekly brief, auto-updated daily.

---

## What I Need From You

1. **GitHub account** - Do you have one? (for free hosting)
2. **Site name** - What should it be called? (e.g., "Vibe Coding 週報", "台灣 AI 週報")
3. **Domain** - Use free `yourusername.github.io/repo-name` or custom domain?

---

## Steps

### Step 1: Create Website Files ✅ DONE
- [x] `index.html` - Main page template
- [x] `style.css` - Clean, mobile-friendly styling
- [x] `generate_site.py` - Script to convert brief → HTML

### Step 2: Test Locally ✅ DONE
- [x] Generate brief
- [x] Convert to HTML
- [x] Preview in browser

### Step 3: Setup GitHub Pages ⏳ WAITING ON YOU
- [ ] Create GitHub repo
- [ ] Push files
- [ ] Enable GitHub Pages
- [ ] Get live URL

### Step 4: Automate Daily Updates ✅ SCRIPTS READY
- [x] `deploy.sh` - Script to generate + push
- [ ] Cron job or GitHub Actions for daily runs

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                    Daily Cron                        │
│                        │                             │
│                        ▼                             │
│              weekly_brief.py                         │
│           (fetch RSS → Claude CLI)                   │
│                        │                             │
│                        ▼                             │
│             generate_site.py                         │
│           (brief.md → index.html)                    │
│                        │                             │
│                        ▼                             │
│                deploy.sh                             │
│              (git push to GitHub)                    │
│                        │                             │
│                        ▼                             │
│              GitHub Pages                            │
│            (serves index.html)                       │
│                        │                             │
│                        ▼                             │
│               🌐 Users visit                         │
│          yourusername.github.io                      │
└─────────────────────────────────────────────────────┘
```

---

## File Structure (Final)

```
Vibe Code Demo 2/
├── index.html           # The website
├── style.css            # Styling
├── weekly_brief.py      # Fetches news, generates brief
├── generate_site.py     # Converts brief to HTML
├── deploy.sh            # Pushes to GitHub
├── venv/                # Python environment
└── briefs/              # Archive of past briefs
```

---

## Timeline

| Step | What | Who |
|------|------|-----|
| 1 | Create HTML/CSS/generate script | Me (now) |
| 2 | Test locally | Me (now) |
| 3 | Create GitHub repo | You (2 min) |
| 4 | Push & enable Pages | Me + You |
| 5 | Setup daily automation | Me |

---

## Let's Start

I'll begin with Steps 1-2 now. While I work, please answer:

1. Do you have a GitHub account?
2. What name do you want for the site?
