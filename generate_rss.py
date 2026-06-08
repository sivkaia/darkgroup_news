import feedparser
from feedgen.feed import FeedGenerator
from email.utils import parsedate_to_datetime

SOURCE_RSS = 'https://news.google.com/rss/search?q=("Dark%20Arkitekter"%20OR%20"Dark%20Design%20Group"%20OR%20"Lark%20Landskap"%20OR%20"Zinc%20interiør"%20OR%20"HK%20Arkitekter"%20OR%20"Heggelund%20%26%20Koxvold%20Arkitekter")&hl=no&gl=NO&ceid=NO:no'

feed = feedparser.parse(SOURCE_RSS)

entries = []

for item in feed.entries:
    try:
        date = parsedate_to_datetime(item.published)
        entries.append((date, item))
    except:
        pass

entries = sorted(
    entries,
    key=lambda x: x[0].timestamp(),
    reverse=True
)

print("=== SORTERT LISTE ===")
for date, item in entries[:10]:
    print(date.isoformat(), item.title)

fg = FeedGenerator()
fg.title("Arkitektkontorer - Sortert etter dato")
fg.description("Google News sortert kronologisk")
fg.link(href="https://github.com")

for date, item in reversed(entries):
    fe = fg.add_entry()
    fe.title(item.title)
    fe.link(href=item.link)
    fe.pubDate(date)

    if hasattr(item, "summary"):
        fe.description(item.summary)

fg.rss_file("feed.xml")
