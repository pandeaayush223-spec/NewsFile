import feedparser
from config import RSS_FEEDS

def parse_feed(source_name: str, feed_url: str) -> list:
    # feedparser.parse(feed_url) returns a feed object
    # feed.entries is the list of articles in that feed
    # For each entry pull out:
    #   - title      → entry.title
    #   - url        → entry.link
    #   - summary    → entry.get("summary", "")
    #   - published  → entry.get("published", "")
    #   - source     → source_name
    # Return a list of dicts, one per entry
    try:
        feed = feedparser.parse(feed_url)
        
        if not feed.entries:
            print(f"No entries found in {source_name} feed: {feed_url}")
            return []
    except Exception as e:
        print(f'Error fetching feed {source_name}: {str(e)}')
        return []
        
    feed_list = []

    for entry in feed.entries:
        feed_list.append({'title': entry.title,
        'url': entry.link, 
        'summary': entry.get("summary", ""),
        'published': entry.get("published", ""),
        'source': source_name
            
        })
    return feed_list
        
    
    
    

def fetch_all_feeds() -> list:
    # Loop over RSS_FEEDS.items()
    # Call parse_feed() for each one
    # Combine all results into one big list and return it
    results = []
    
    for source_name, feed_url in RSS_FEEDS.items():
        articles = parse_feed(source_name, feed_url)
        results.extend(articles)
    return results
        