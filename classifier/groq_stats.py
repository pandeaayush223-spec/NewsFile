from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

def extract_stats(title, article_text):
    try:
        system = """You are a data extraction assistant. Extract all numerical statistics from the article.
Return ONLY this exact JSON structure with no markdown, no explanation:
{
  "summary": "one sentence summary of key findings",
  "stats": [{"label": "stat name", "value": 42, "unit": "%"}],
  "chart_data": [{"name": "category", "value": 42}],
  "key_facts": ["fact 1", "fact 2", "fact 3"]
}"""
        user = f"Title: {title}\n\nArticle: {article_text[:3000]}"
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Groq error: {e}")
        return None