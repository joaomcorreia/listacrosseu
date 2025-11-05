import json
from .providers import get_provider

SYSTEM = (
    "You write concise SEO for a European business directory (ListAcross EU). "
    "Reply with strict JSON. Keys: title, description, tags(array), jsonld(object), images(array of {keyword,alt,idea}). "
    "Title<=60 chars, desc 120-160 chars."
)


def make_prompt(title, excerpt, body, url):
    return f"URL:{url}\nTitle:{title}\nExcerpt:{excerpt}\nBody:{(body or '')[:800]}"


def suggest_for(title="", excerpt="", body="", url=""):
    raw = get_provider().suggest(SYSTEM, make_prompt(title or "", excerpt or "", body or "", url or ""))
    try:
        data = json.loads(raw)
    except:
        data = {
            "title": raw[:60],
            "description": raw[:155],
            "tags": [],
            "jsonld": {},
            "images": []
        }
    
    # Ensure all required keys exist with defaults
    for k, defv in [("title", ""), ("description", ""), ("tags", []), ("jsonld", {}), ("images", [])]:
        data.setdefault(k, defv)
    
    return data