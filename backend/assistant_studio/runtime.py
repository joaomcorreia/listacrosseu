import os, re, json
from typing import List, Dict, Any
from django.utils import timezone
from .models import AssistantConfig, Intent, KnowledgeDoc
from .serializers import get_live_config

WORD_RE = re.compile(r"[a-z0-9]+", re.I)

def detect_lang(requested: str, cfg: AssistantConfig) -> str:
    if requested and requested.lower() in (cfg.supported_langs or []):
        return requested.lower()
    return (cfg.default_lang or "en").lower()

def tokenize(text: str) -> List[str]:
    return WORD_RE.findall(text.lower())

def score_intent(intents: List[Intent], text: str) -> Dict[str, Any]:
    tokens = tokenize(text)
    joined = " ".join(tokens)
    best = None
    best_score = -1
    for it in intents:
        if not it.enabled:
            continue
        score = 0
        for kw in (it.keywords or []):
            kw_l = kw.lower()
            if kw_l in tokens or kw_l in joined:
                score += 2
        for ex in (it.examples or []):
            ex_l = ex.lower()
            if ex_l in joined:
                score += 1
        score += int(it.priority or 0)
        if score > best_score:
            best_score = score
            best = it
    return {"intent": best, "score": best_score}

def select_kb(lang: str, limit: int = 4) -> List[KnowledgeDoc]:
    qs = KnowledgeDoc.objects.filter(enabled=True).order_by("-priority","slug")
    # prefer exact language, then 'multi', then others
    exact = list(qs.filter(lang=lang)[:limit])
    if len(exact) < limit:
        exact += list(qs.filter(lang="multi")[: (limit - len(exact))])
    if len(exact) < limit:
        extra = list(qs.exclude(lang__in=[lang,"multi"])[: (limit - len(exact))])
        exact += extra
    return exact[:limit]

def render_template_answer(cfg: AssistantConfig, it: Intent, lang: str, kb_docs: List[KnowledgeDoc], question: str) -> str:
    title = it.title if it else "Help"
    tips = []
    for d in kb_docs:
        if d.type in ("kb_json","pricing_json"):
            try:
                data = json.loads(d.content or "{}")
                bullets = data.get("bullets", {}).get(lang) or data.get("bullets", {}).get("en")
                if isinstance(bullets, list):
                    tips.extend(bullets[:3])
            except Exception:
                pass
        else:
            if d.content:
                lines = [ln.strip() for ln in d.content.splitlines() if ln.strip()]
                tips.extend(lines[:2])
    tips = tips[:5]
    bullet_text = "\n- ".join(tips) if tips else "- I will guide you through the next steps."
    return (
        f"{title} — here's the gist based on what I know:\n"
        f"- Question: {question}\n"
        f"{('- ' + bullet_text) if tips else ''}\n"
        f"If you want, we can proceed with the suggested action."
    ).strip()

def choose_cta_text(cfg: AssistantConfig, cta_code: str, lang: str) -> str:
    table = cfg.cta_text or {}
    by_lang = table.get(lang) or table.get("en") or {}
    return by_lang.get(cta_code, cta_code)

def tool_payload_template(intent: Intent, lang: str) -> Dict[str, Any]:
    if not intent: 
        return {}
    code = intent.primary_cta
    if code == "create_listing":
        return {"business_name": "", "country": "", "city": "", "email": "", "phone": ""}
    if code == "start_jcw_build":
        return {"tenant_id": "", "preferred_locales": [lang], "template_id": "jcw-rest-01"}
    if code == "start_print_order":
        return {"product": "business_card_standard", "quantity": 250}
    if code == "upgrade_plan":
        return {"upgrade_url": "/dashboard/billing/upgrade"}
    return {}

def llm_answer_openai(system_prompt, lang, q, intent, kb_docs):
    from openai import OpenAI
    client = OpenAI()

    # Build compact KB context (prefer inline content)
    chunks = []
    for d in kb_docs:
        if d.content:
            text = d.content.strip()
            if len(text) > 1500:
                text = text[:1500]
            chunks.append(f"[{d.slug}] {text}")
    context = "\n\n".join(chunks[:4])

    messages = [
        {"role": "system", "content": f"{system_prompt}\n\nAnswer in language: {lang}. Keep it concise and actionable. Never invent prices or policies; if unknown, say so and suggest the next step."},
        {"role": "user", "content": f"Context:\n{context}\n\nUser question:\n{q}\n\nReturn a short, helpful answer with one clear next step."}
    ]

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.4,
        max_tokens=350,
    )
    return resp.choices[0].message.content.strip()
