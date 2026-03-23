from dotenv import load_dotenv
import os

ENV = os.getenv("ENV", "development")

if ENV == "production":
    load_dotenv(".env.production")
else:
    load_dotenv(".env.development")
    

# Nested topic hierarchy: parent topic → list of subtopics
# Adjust subtopic names to match what you see in your articles
TOPICS = {
    "Technology": ["AI", "Cybersecurity", "Hardware", "Software"],
    "Economics":  ["Markets", "Crypto", "Trade", "Fiscal Policy"],
    "Politics":   ["US Politics", "International", "Legislation", "Conflicts"],
    "Health":     ["Medicine", "Mental Health", "Public Health"],
    "Climate":    ["Energy", "Environment", "Science"],
    "Other":      [],
}

# Keywords keyed by SUBTOPIC (not parent topic)
# Add or adjust keywords here to improve classification accuracy
TOPIC_KEYWORDS = {
    # Technology subtopics
    "AI":["artificial intelligence", "machine learning", "large language model", "ChatGPT", "Gemini", "Claude", "neural network", "deep learning", "generative AI", "LLM", "OpenAI", "Anthropic"],
    "Cybersecurity":["cybersecurity", "hacker", "breach", "vulnerability", "ransomware", "malware", "phishing", "encryption", "zero-day"],
    "Hardware":  ["computer chip", "semiconductor", "hardware", "silicon chip", "robotics", "processor", "GPU", "Intel", "NVIDIA"],
    "Software":      ["software", "app development", "developer tools", "open source", "cloud computing", "SaaS"],

    # Economics subtopics
    "Markets":       ["stock market", "Fed rate", "interest rate", "inflation", "Wall Street", "GDP", "recession", "S&P", "earnings report"],
    "Crypto":       ["crypto", "bitcoin", "ethereum", "blockchain", "NFT", "web3"],
    "Trade":        ["trade deal", "tariff", "import tariff", "export ban", "supply chain"],
    "Fiscal Policy":["fiscal", "monetary", "budget", "spending", "deficit"],

    # Politics subtopics
    "US Politics":  ["congress", "senate", "election", "president", "vote", "democrat", "republican", "White House", "campaign"],
    "International": ["foreign policy", "diplomat", "treaty", "United Nations", "NATO", "bilateral", "summit"],
    "Legislation":  ["senate bill", "new law", "legislation", "regulation", "policy"],
    "Conflicts":    ["war", "military", "troops", "conflict", "sanctions", "ceasefire", "military attack"],

    # Health subtopics
    "Medicine":     ["vaccine", "cancer", "FDA", "drug approval", "hospital", "infectious disease", "clinical trial", "surgery", "CDC", "pharmaceutical", "diagnosis"],
    "Mental Health":["mental health", "therapy", "anxiety", "depression", "wellbeing", "psychiatry"],
    "Public Health":["pandemic", "outbreak", "public health", "epidemic", "WHO"],

    # Climate subtopics
    "Energy":       ["renewable", "solar", "wind energy", "fossil fuel", "oil price", "natural gas", "nuclear energy", "EPA"],
    "Environment":  ["climate change", "emissions", "carbon", "flood", "wildfire", "drought", "deforestation", "greenhouse", "net zero"],
    "Science":      ["scientific research", "scientific study", "scientist", "discovery", "experiment", "space mission", "NASA"],

    "Other":        [],
}

RSS_FEEDS = {
    "Reuters": "https://news.google.com/rss/search?q=when:24h+allinurl:reuters.com&ceid=US:en&hl=en-US&gl=US",
    "AP News": "https://news.google.com/rss/search?q=when:24h+site:apnews.com&ceid=US:en&hl=en-US&gl=US",    
    "BBC": "http://feeds.bbci.co.uk/news/rss.xml",
    "TechCrunch": "https://techcrunch.com/feed/",
    # "Guardian": "https://www.theguardian.com/world/rss",  # returning 0 entries
    # "NPR": "https://feeds.npr.org/1001/rss.xml",          # blocking requests
}

MAX_ARTICLES_PER_TOPIC = 500

ARTICLES_DIR = "articles"

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

REFRESH_INTERVAL_MINS = 60