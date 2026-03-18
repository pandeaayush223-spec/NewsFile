from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY
from config import MAX_ARTICLES_PER_TOPIC


supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def insert_article(article: dict):
    # Use supabase.table("articles").insert(article).execute()
    # Wrap it in a try/except — what might go wrong when inserting?
    try:
        supabase.table('articles').insert(article).execute()
    except Exception as e:
        print(f'article failed to insert: {e}')
    

def article_exists(url: str) -> bool:
    # Use supabase.table("articles").select("id").eq("url", url).execute()
    # The response has a .data attribute — it's a list
    # If the list is empty, the article doesn't exist
    # What should you return in each case?
    response = supabase.table("articles").select("id").eq("url", url).execute()
    
    return bool(response.data)
    

def get_articles_by_topic(topic: str, days: int = None) -> list:
    # Select all articles where topic matches
    # Order by published_date descending so newest comes first
    # Return the .data list
    try :
        query = supabase.table('articles')\
        .select("id, title, url, source, topic, summary, published_date, word_count")\
        .eq("topic", topic)\
        .order("published_date", desc=True)
        
        if days:
            cutoff = (datetime.utcnow() - timedelta(days=days)).isoformat()
            query = query.gte("published_date", cutoff)
        
        return query.execute().data
    except Exception as e:
        print(f"Unable to get articles: {e}")
        return []

def get_all_stats() -> list:
    # For now just return all articles and we'll aggregate in the API layer
    # Select all articles, return .data
    try:
        response = supabase.table("articles").select('id, title, url, source, topic, summary, published_date, scraped_at, word_count').execute()
        return response.data
    except Exception as e:
        print(f'Unable to get stats: {e}')
        return []

def get_article_by_id(article_id: str) -> dict:
    try:
        response = supabase.table("articles").select("*").eq("id", article_id).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error fetching article: {e}")
        return None
    
def get_topics() -> list:
    try:
        response = supabase.table("articles").select("topic").execute()
        topics = {}
        for row in response.data:
            topic = row["topic"]
            topics[topic] = topics.get(topic, 0) + 1
        return [{"topic": t, "count": c} for t, c in topics.items()]
    except Exception as e:
        print(f"Error fetching topics: {e}")
        return []

def search_articles(query: str) -> list:
    try:
        response = supabase.table("articles").select("*").ilike("title", f"%{query}%").execute()
        return response.data
    except Exception as e:
        print(f"Error searching articles: {e}")
        return []

def prune_topic(topic: str) -> None:
    # Query 1 — just count
    response = supabase.table("articles").select("id").eq("topic", topic).execute()
    count = len(response.data)
    
    if count <= MAX_ARTICLES_PER_TOPIC:
        return
    
    excess = count - MAX_ARTICLES_PER_TOPIC
    
    # Query 2 — find oldest articles to delete
    oldest = supabase.table("articles").select("id").eq("topic", topic).order("published_date", desc=False).limit(excess).execute()
    
    # Extract just the IDs from oldest.data
    ids_to_delete = [row["id"] for row in oldest.data]
    
    # Delete those articles
    supabase.table("articles").delete().in_("id", ids_to_delete).execute()
    
    # Log how many were pruned
    print(f"Pruned {excess} articles from {topic}")