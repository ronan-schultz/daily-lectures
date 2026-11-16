"""Build feed.xml (podcast RSS) from episodes.json.

episodes.json is a list of objects:
  {"number": 1, "slug": "001-gps-relativity", "title": "...", "date": "2026-11-16", "series": "morning",
   "summary": "one or two sentences", "questions": ["...", "..."]}
The MP3 must exist at episodes/<slug>.mp3. Episodes whose MP3 is missing are skipped.
"""
import json, os, subprocess
from datetime import datetime, timezone
from email.utils import format_datetime
from xml.sax.saxutils import escape

BASE = "https://ronan-schultz.github.io/daily-lectures"
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
eps = json.load(open(os.path.join(root, "episodes.json")))

def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", path], capture_output=True, text=True).stdout
    s = int(float(out.strip()))
    return f"{s // 3600:02d}:{s % 3600 // 60:02d}:{s % 60:02d}"

items = []
for e in sorted(eps, key=lambda e: e["number"], reverse=True):
    mp3 = os.path.join(root, "episodes", e["slug"] + ".mp3")
    if not os.path.exists(mp3):
        continue
    # Morning series publishes at 02:00 Mountain (09:00 UTC), afternoon at 07:00 Mountain (14:00 UTC).
    series = e.get("series", "morning")
    pub = datetime.strptime(e["date"], "%Y-%m-%d").replace(hour=14 if series == "afternoon" else 9, tzinfo=timezone.utc)
    label = "PM" if series == "afternoon" else "AM"
    notes = e["summary"] + "\n\nQuiz (reply in that episode's Daily Lecture chat):\n" + \
        "\n".join(f"{i + 1}. {q}" for i, q in enumerate(e["questions"]))
    items.append(f"""    <item>
      <title>{escape(f"{label} {e['number']:03d}. {e['title']}")}</title>
      <description>{escape(notes)}</description>
      <itunes:summary>{escape(notes)}</itunes:summary>
      <enclosure url="{BASE}/episodes/{e['slug']}.mp3" length="{os.path.getsize(mp3)}" type="audio/mpeg"/>
      <guid isPermaLink="false">daily-lectures-{e['slug']}</guid>
      <pubDate>{format_datetime(pub)}</pubDate>
      <itunes:duration>{duration(mp3)}</itunes:duration>
      <itunes:episode>{e['number']}</itunes:episode>
    </item>""")

feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
  <channel>
    <title>Daily Lecture</title>
    <link>{BASE}/</link>
    <language>en-us</language>
    <description>Two lectures a day for Ronan: STEM in the morning, skills, institutions and ideas in the afternoon.</description>
    <itunes:author>Claude</itunes:author>
    <itunes:image href="{BASE}/cover.png"/>
    <image><url>{BASE}/cover.png</url><title>Daily Lecture</title><link>{BASE}/</link></image>
    <itunes:explicit>false</itunes:explicit>
    <itunes:block>Yes</itunes:block>
{chr(10).join(items)}
  </channel>
</rss>
"""
open(os.path.join(root, "feed.xml"), "w").write(feed)
print(f"feed.xml: {len(items)} episodes")
