import os, json, re, html
from typing import Dict, Any, List, Optional
import datetime

PROVIDER = os.getenv("AI_PROVIDER", "OPENAI").upper()  # OPENAI or ANTHROPIC or MOCK
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY","")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY","")
MODEL_OUTLINE = os.getenv("AI_MODEL_OUTLINE","gpt-4.1-mini")
MODEL_DRAFT   = os.getenv("AI_MODEL_DRAFT","gpt-4.1")
MODEL_SEO     = os.getenv("AI_MODEL_SEO","gpt-4.1-mini")
MODEL_TRANSL  = os.getenv("AI_MODEL_TRANSL","gpt-4.1-mini")

TEMPERATURE = float(os.getenv("AI_TEMPERATURE","0.2"))
MAX_TOKENS  = int(os.getenv("AI_MAX_TOKENS","4000"))

# --- Provider shims (lazy import to avoid hard dependency when MOCK)
def _openai_client():
    try:
        from openai import OpenAI
        return OpenAI(api_key=OPENAI_API_KEY)
    except Exception as e:
        raise RuntimeError(f"OpenAI import/init failed: {e}")

def _anthropic_client():
    try:
        import anthropic
        return anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    except Exception as e:
        raise RuntimeError(f"Anthropic import/init failed: {e}")

# --- Shared system rules for reliability
SYSTEM_RULES = """You are Listy, the editorial AI for ListAcross EU.
Goals: produce accurate, sourced, helpful articles for EU readers.
Rules:
- No fabrication. If unsure, say you need a source.
- Prefer official/high-authority sources (EU, gov portals, standards bodies, reputable orgs).
- Always structure content clearly (H1, H2/H3, short paragraphs, bullet lists, ToC anchors).
- Output must be valid JSON conforming exactly to the requested schema.
- EU spelling for English (en-GB).
- Avoid legal/medical/financial advice; present neutral, sourced info.
"""

def _call_openai(model: str, messages: List[Dict[str, str]], response_format: Optional[Dict]=None) -> str:
    client = _openai_client()
    # Use Responses API with JSON mode if available; fallback to chat.completions with strict JSON instruction
    try:
        r = client.responses.create(
            model=model,
            input=messages,
            temperature=TEMPERATURE,
            max_output_tokens=MAX_TOKENS,
            response_format={"type":"json_object"}
        )
        # New Responses API returns output as r.output_text
        return r.output_text
    except Exception:
        # Fallback to Chat
        chat = client.chat.completions.create(
            model=model,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            response_format={"type":"json_object"},
            messages=messages
        )
        return chat.choices[0].message.content

def _call_anthropic(model: str, messages: List[Dict[str, str]]) -> str:
    client = _anthropic_client()
    # Convert OpenAI-style messages -> single prompt
    sys = SYSTEM_RULES
    user_blocks = []
    for m in messages:
        if m.get("role") == "system":
            sys = m["content"]
        elif m.get("role") in ("user","assistant"):
            user_blocks.append(m["content"])
    prompt = "\n\n".join(user_blocks)
    r = client.messages.create(
        model=model,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
        system=sys,
        messages=[{"role":"user","content":prompt}]
    )
    # Concatenate text blocks
    parts = []
    for c in r.content:
        if getattr(c, "type", None) == "text":
            parts.append(c.text)
        elif isinstance(c, dict) and c.get("type") == "text":
            parts.append(c.get("text",""))
    return "\n".join(parts)

def _mock_response(payload: Dict[str,Any], kind: str) -> Dict[str,Any]:
    # Deterministic mock for local dev
    if kind == "outline":
        return {
            "title": f"{payload.get('topic','Untitled')} — 2025 Guide",
            "sections":[
                {"h2":"Overview","bullets":["Why it matters","Who it's for"]},
                {"h2":"Steps","bullets":["Step 1","Step 2","Step 3"]},
                {"h2":"Costs & timelines","bullets":["Fees","Typical delays"]},
                {"h2":"FAQs","bullets":["Q1","Q2"]}
            ],
            "candidate_faqs":["What does it cost?","How long does it take?"],
            "sources":[]
        }
    if kind == "draft":
        outline = payload.get("outline",{})
        body = f"<h1>{outline.get('title','Untitled')}</h1>"
        for s in outline.get("sections",[]):
            body += f"<h2 id='{re.sub(r'[^a-z0-9]+','-',s['h2'].lower()).strip('-')}'>{html.escape(s['h2'])}</h2>"
            body += f"<p>{'; '.join(s.get('bullets',[]))}</p>"
        return {
            "body_html": body + "<h2 id='references'>References</h2><ol></ol>",
            "headings": [s["h2"] for s in outline.get("sections",[])],
            "toc": [{"id": re.sub(r'[^a-z0-9]+','-',s['h2'].lower()).strip('-'), "text": s["h2"]} for s in outline.get("sections",[])],
            "citations": [],
            "internal_links": [
              {"href":"/how-it-works","anchor":"How it works"},
              {"href":"/countries","anchor":"Countries"}
            ]
        }
    if kind == "seo":
        title = payload.get("title","AI-generated post")
        slug = re.sub(r'[^a-z0-9\-]+','-', payload.get("proposed_slug", title.lower().replace(" ","-")))[:200]
        return {"meta_title": title[:60], "meta_desc":"Helpful, human-reviewed article.", "slug": slug, "alt_texts":[], "tags": payload.get("keywords",[])[:6]}
    if kind == "translate":
        return payload.get("input_json",{})
    return {}

def _ensure_json(text: str) -> Dict[str,Any]:
    text = text.strip()
    # try to extract JSON object if assistant wrapped with code fences
    m = re.search(r"\{.*\}\s*$", text, re.S)
    if m:
        text = m.group(0)
    return json.loads(text)

# --- Public functions
def generate_outline(topic: str, language: str, country_code: str, keywords: List[str], tone: str) -> Dict[str,Any]:
    user = {
        "role":"user",
        "content": f"""
Create a blog post OUTLINE.

Topic: {topic}
Language: {language}
Country focus: {country_code}
Primary keywords: {', '.join(keywords)}
Tone: {tone}
Target reader: EU small business owners

Output JSON:
{{
  "title": "...",
  "sections": [{{"h2":"", "bullets":["..."]}}, ...],
  "candidate_faqs": ["Q1?","Q2?"],
  "sources": [{{"title":"", "url":"", "note":""}}]
}}
Quality bar: Use trustworthy sources. If none found, return "sources": [] and do not fabricate.
"""
    }
    msgs = [{"role":"system","content":SYSTEM_RULES}, user]
    if PROVIDER == "OPENAI":
        out = _call_openai(MODEL_OUTLINE, msgs)
        return _ensure_json(out)
    if PROVIDER == "ANTHROPIC":
        out = _call_anthropic("claude-3-5-sonnet-latest", msgs)
        return _ensure_json(out)
    return _mock_response({"topic":topic}, "outline")

def generate_draft(outline_json: Dict[str,Any]) -> Dict[str,Any]:
    user = {
        "role":"user",
        "content": f"""
Using this outline JSON, write the full HTML article.
- Cite facts with numbered references [1], [2] and include a <h2 id="references">References</h2><ol> list of links at the end.
- Add ids to H2/H3 for ToC.
- Suggest 2–3 internal links (href + anchor text) from: /how-it-works, /countries, /categories.
- Output JSON:
{{
  "body_html":"<h1>...</h1> ...",
  "headings":["H2","H2","H3"],
  "toc":[{{"id":"...","text":"..."}}],
  "citations":[{{"title":"", "url":"", "note":""}}],
  "internal_links":[{{"href":"","anchor":""}}]
}}

Outline JSON:
{json.dumps(outline_json, ensure_ascii=False)}
"""
    }
    msgs = [{"role":"system","content":SYSTEM_RULES}, user]
    if PROVIDER == "OPENAI":
        out = _call_openai(MODEL_DRAFT, msgs)
        return _ensure_json(out)
    if PROVIDER == "ANTHROPIC":
        out = _call_anthropic("claude-3-5-sonnet-latest", msgs)
        return _ensure_json(out)
    return _mock_response({"outline":outline_json}, "draft")

def generate_seo(title: str, keywords: List[str], proposed_slug: str, language: str) -> Dict[str,Any]:
    user = {
        "role":"user",
        "content": f"""
Produce SEO metadata.

Input:
- Language: {language}
- Title: {title}
- Top keywords: {', '.join(keywords)}

Output JSON:
{{
  "meta_title":"<=60 chars, includes main keyword, natural",
  "meta_desc":"<=155 chars, compelling and truthful",
  "slug":"kebab-case",
  "alt_texts":[{{"selector":"first-image","alt":"..."}}],
  "tags":[]
}}
"""
    }
    msgs = [{"role":"system","content":SYSTEM_RULES}, user]
    if PROVIDER == "OPENAI":
        out = _call_openai(MODEL_SEO, msgs)
        return _ensure_json(out)
    if PROVIDER == "ANTHROPIC":
        out = _call_anthropic("claude-3-5-sonnet-latest", msgs)
        return _ensure_json(out)
    return _mock_response({"title":title, "keywords":keywords, "proposed_slug":proposed_slug}, "seo")

def translate_article(input_json: Dict[str,Any], target_language: str) -> Dict[str,Any]:
    user = {
        "role":"user",
        "content": f"""
Translate this article JSON to {target_language} keeping structure/anchors.
Do not modify links; translate visible text only; localise units/currency for EU readers.

Input JSON:
{json.dumps(input_json, ensure_ascii=False)}
"""
    }
    msgs = [{"role":"system","content":SYSTEM_RULES}, user]
    if PROVIDER == "OPENAI":
        out = _call_openai(MODEL_TRANSL, msgs)
        return _ensure_json(out)
    if PROVIDER == "ANTHROPIC":
        out = _call_anthropic("claude-3-5-sonnet-latest", msgs)
        return _ensure_json(out)
    return _mock_response({"input_json":input_json}, "translate")


class AIProviderFactory:
    """Factory class to provide a clean interface for AI operations"""
    
    @staticmethod
    def get_provider():
        """Get an AI provider instance"""
        return AIProvider()


class AIProvider:
    """Provider interface for AI operations"""
    
    def generate_outline(self, topic: str, target_audience: str = "general business audience") -> Dict[str, Any]:
        """Generate blog post outline"""
        # Map to the module-level function with appropriate defaults
        return generate_outline(
            topic=topic,
            language="en",  # Default to English
            country_code="EU",  # Default to EU
            keywords=[],  # Default empty keywords
            tone="professional"  # Default tone
        )
    
    def generate_draft(self, outline: str, word_count: int = 800) -> Dict[str, Any]:
        """Generate blog post draft from outline string"""
        # Convert outline string to JSON structure
        try:
            # If outline is already JSON, parse it
            if outline.strip().startswith('{'):
                outline_json = json.loads(outline)
            else:
                # Create a simple JSON structure from text outline
                outline_json = {
                    "title": "Generated Article",
                    "sections": [{"heading": "Introduction", "content": outline}],
                    "word_count": word_count
                }
        except json.JSONDecodeError:
            # Fallback: create JSON structure from text
            outline_json = {
                "title": "Generated Article",
                "sections": [{"heading": "Introduction", "content": outline}],
                "word_count": word_count
            }
        
        return generate_draft(outline_json)
    
    def generate_seo(self, content: str, target_keywords: List[str] = None) -> Dict[str, Any]:
        """Generate SEO metadata for content"""
        if target_keywords is None:
            target_keywords = []
        
        # Extract or generate a title from content
        lines = content.strip().split('\n')
        title = lines[0][:60] if lines else "Generated Article"
        
        # Generate a slug from title
        slug = re.sub(r'[^a-zA-Z0-9\s-]', '', title.lower())
        slug = re.sub(r'[\s-]+', '-', slug).strip('-')
        
        return generate_seo(
            title=title,
            keywords=target_keywords,
            proposed_slug=slug,
            language="en"  # Default to English
        )
    
    def translate_article(self, content: str, target_language: str) -> Dict[str, Any]:
        """Translate article content"""
        # Create input JSON structure for translation
        input_json = {
            "title": "Article",
            "content": content,
            "target_language": target_language
        }
        
        return translate_article(input_json, target_language)