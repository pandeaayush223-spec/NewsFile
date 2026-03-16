from bs4 import BeautifulSoup

def clean_html(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    
    for tag_name in ['script', 'nav', 'style', 'footer', 'header']:
        for tag in soup.find_all(tag_name):
            tag.decompose()
    
    body = soup.find("article") or soup.find("main") or soup.body
    
    if not body:
        return ""
    
    paragraphs = body.find_all("p")

    text = "\n".join(p.get_text() for p in paragraphs)
    
    return text

        
