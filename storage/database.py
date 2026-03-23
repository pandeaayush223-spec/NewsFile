from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY
from config import MAX_ARTICLES_PER_TOPIC

from logger import get_logger

logger = get_logger(__name__)


supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def insert_article(article: dict):
    try:
        supabase.table('articles').upsert(article).execute()
    except Exception as e:
        logger.error(f'article failed to insert: {e}')


def article_exists(url: str) -> bool:
    try:
        response = supabase.table("articles").select("id").eq("url", url).execute()
        return bool(response.data)
    except Exception as e:
        logger.error(f"Error checking article existence for {url!r}: {e}")
        return False
    

def get_articles_by_topic(topic: str, days: int = None, subtopic: str = None) -> list:
    # Select all articles where topic matches
    # Order by published_date descending so newest comes first
    # Return the .data list
    try:
        query = supabase.table('articles')\
        .select("id, title, url, source, topic, subtopic, summary, published_date, word_count")\
        .eq("topic", topic)\
        .order("published_date", desc=True)

        if subtopic:
            query = query.eq("subtopic", subtopic)

        if days:
            cutoff = (datetime.utcnow() - timedelta(days=days)).isoformat()
            query = query.gte("published_date", cutoff)

        return query.execute().data
    except Exception as e:
        logger.error(f"Unable to get articles: {e}")
        return []

def get_all_stats() -> list:
    # For now just return all articles and we'll aggregate in the API layer
    # Select all articles, return .data
    try:
        response = supabase.table("articles").select('id, title, url, source, topic, summary, published_date, scraped_at, word_count').execute()
        return response.data
    except Exception as e:
        logger.error(f'Unable to get stats: {e}')
        return []

def get_article_by_id(article_id: str) -> dict:
    try:
        response = supabase.table("articles").select("*").eq("id", article_id).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        logger.error(f"Error fetching article: {e}")
        return None
    
def get_topics() -> list:
    try:
        response = supabase.table("articles").select("topic, subtopic").execute()
        # Build nested structure: {parent: {subtopic: count, _total: count}}
        topic_data: dict = {}
        for row in response.data:
            parent = row["topic"]
            subtopic = row.get("subtopic")
            if parent not in topic_data:
                topic_data[parent] = {"count": 0, "subtopics": {}}
            topic_data[parent]["count"] += 1
            if subtopic:
                topic_data[parent]["subtopics"][subtopic] = topic_data[parent]["subtopics"].get(subtopic, 0) + 1

        result = []
        for parent, data in topic_data.items():
            result.append({
                "topic": parent,
                "count": data["count"],
                "subtopics": [{"name": s, "count": c} for s, c in data["subtopics"].items()],
            })
        return result
    except Exception as e:
        logger.error(f"Error fetching topics: {e}")
        return []

def search_articles(query: str) -> list:
    try:
        response = supabase.table("articles").select("*").ilike("title", f"%{query}%").execute()
        return response.data
    except Exception as e:
        logger.error(f"Error searching articles: {e}")
        return []

def prune_topic(topic: str) -> None:
    try:
        response = supabase.table("articles").select("id").eq("topic", topic).execute()
        count = len(response.data)

        if count <= MAX_ARTICLES_PER_TOPIC:
            return

        excess = count - MAX_ARTICLES_PER_TOPIC

        oldest = supabase.table("articles").select("id").eq("topic", topic).order("published_date", desc=False).limit(excess).execute()
        ids_to_delete = [row["id"] for row in oldest.data]

        supabase.table("articles").delete().in_("id", ids_to_delete).execute()
        logger.info(f"Pruned {excess} articles from {topic}")
    except Exception as e:
        logger.error(f"Error pruning topic {topic!r}: {e}")