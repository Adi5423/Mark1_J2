import feedparser
import random

def get_news():
    news_feeds = {
        'Technology': [
            "https://feeds.feedburner.com/TechCrunch/",
            "https://www.wired.com/feed/rss",
            "https://feeds.feedburner.com/TheNextWeb"
        ],
        'Business': [
            "https://feeds.feedburner.com/entrepreneur/latest",
            "http://feeds.bbci.co.uk/news/business/rss.xml",
            "https://www.forbes.com/business/feed/"
        ]
    }

    news_items = []

    for category, feeds in news_feeds.items():
        random.shuffle(feeds)
        for feed_url in feeds:
            try:
                feed = feedparser.parse(feed_url)
                entry = random.choice(feed.entries)
                news_items.append(f"{category}: {entry.title}")
                break
            except:
                continue

    return news_items

if __name__ == "__main__":
    news = get_news()
    for item in news:
        print(item)