from dotenv import load_dotenv
import os

ENV = os.getenv("ENV", "development")

if ENV == "production":
    load_dotenv(".env.production")
else:
    load_dotenv(".env.development")
    

TOPICS = ['Technology', 'Economics', 'Politics', 'Health', 'Climate', 'Other'] 

TOPIC_KEYWORDS = {"Technology": ["AI", "software", "Apple", "Google", "startup", "chip", "cyber", "tech", "data", "algorithm"],
    "Economics":    ["stock", "Fed", "rate", "inflation", "bank", "market", "GDP", "economy", "invest", "dollar"],
    "Politics":   ["congress", "senate", "election", "president", "vote", "policy", "democrat", "republican", "bill", "law"],
    "Health":     ["vaccine", "cancer", "FDA", "drug", "hospital", "disease", "mental health", "study", "clinical"],
    "Climate":    ["climate", "emissions", "carbon", "renewable", "flood", "wildfire", "EPA", "fossil", "solar"],
    "Other": []
}

RSS_FEEDS = {
    "Reuters": "https://news.google.com/rss/search?q=when:24h+allinurl:reuters.com&ceid=US:en&hl=en-US&gl=US",
    "AP News": "https://news.google.com/rss/search?q=when:24h+site:apnews.com&ceid=US:en&hl=en-US&gl=US",    
    "BBC": "http://feeds.bbci.co.uk/news/rss.xml",
    "TechCrunch": "https://techcrunch.com/feed/",
    "Guardian": "https://www.theguardian.com/world/rss",
    "NPR": "https://feeds.npr.org/1001/rss.xml",
}

MAX_ARTICLES_PER_TOPIC = 500

ARTICLES_DIR = "articles"

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

REFRESH_INTERVAL_MINS = 60