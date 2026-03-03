#!/usr/bin/env python3
"""
Read Like Ray — Daily Build Script
Runs via GitHub Actions every night at midnight.
Calculates the current day, pulls the reading from readings.json,
and rebuilds index.html from the template.
"""

import json
import math
from datetime import date, datetime

# ── Config ──────────────────────────────────────────────────────────────────
PROJECT_START = date(2026, 4, 1)
TOTAL_DAYS = 1000

# ── Calculate today ──────────────────────────────────────────────────────────
today = date.today()
delta = (today - PROJECT_START).days
day_number = max(1, min(delta + 1, TOTAL_DAYS))  # clamp between 1 and 1000

# Which entry to use (cycle if we run out — shouldn't happen but safe)
with open('readings.json', 'r') as f:
    data = json.load(f)

days = data['days']
entry_index = (day_number - 1) % len(days)
entry = days[entry_index]

# ── Helper: format date nicely ───────────────────────────────────────────────
today_formatted = today.strftime('%B %-d, %Y')
week_number = math.ceil(day_number / 7)
progress_pct = round((day_number / TOTAL_DAYS) * 100, 2)

# ── Helper: link HTML ─────────────────────────────────────────────────────────
def link_html(url):
    if url:
        return f'<a class="card-link" href="{url}" target="_blank" rel="noopener">Read free online →</a>'
    return '<span class="no-link">Find at your library or search title + author</span>'

# ── Load template ─────────────────────────────────────────────────────────────
with open('template.html', 'r') as f:
    html = f.read()

# ── Replace all placeholders ──────────────────────────────────────────────────
replacements = {
    '{{DAY_NUMBER}}':    str(day_number),
    '{{TODAY_DATE}}':    today_formatted,
    '{{WEEK_NUMBER}}':   str(week_number),
    '{{PROGRESS_PCT}}':  str(progress_pct),
    '{{POEM_TITLE}}':    entry['poem']['title'],
    '{{POEM_AUTHOR}}':   entry['poem']['author'],
    '{{POEM_YEAR}}':     entry['poem']['year'],
    '{{POEM_DESC}}':     entry['poem']['desc'],
    '{{POEM_LINK_HTML}}': link_html(entry['poem'].get('link', '')),
    '{{STORY_TITLE}}':   entry['story']['title'],
    '{{STORY_AUTHOR}}':  entry['story']['author'],
    '{{STORY_YEAR}}':    entry['story']['year'],
    '{{STORY_DESC}}':    entry['story']['desc'],
    '{{STORY_LINK_HTML}}': link_html(entry['story'].get('link', '')),
    '{{ESSAY_TITLE}}':   entry['essay']['title'],
    '{{ESSAY_AUTHOR}}':  entry['essay']['author'],
    '{{ESSAY_YEAR}}':    entry['essay']['year'],
    '{{ESSAY_DESC}}':    entry['essay']['desc'],
    '{{ESSAY_LINK_HTML}}': link_html(entry['essay'].get('link', '')),
    '{{PROMPT}}':        entry['prompt'],
}

for placeholder, value in replacements.items():
    html = html.replace(placeholder, value)

# ── Write final index.html ────────────────────────────────────────────────────
with open('index.html', 'w') as f:
    f.write(html)

print(f"✓ Built Day {day_number} — {today_formatted}")
print(f"  Poem:  {entry['poem']['title']} — {entry['poem']['author']}")
print(f"  Story: {entry['story']['title']} — {entry['story']['author']}")
print(f"  Essay: {entry['essay']['title']} — {entry['essay']['author']}")
