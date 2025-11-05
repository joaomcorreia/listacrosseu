import os
import httpx
import json


class OpenAIProvider:
    def __init__(self, key: str):
        self.key = key
    
    def suggest(self, system, prompt):
        r = httpx.post("https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {self.key}"},
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.6
            },
            timeout=30)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"].strip()


class AnthropicProvider:
    def __init__(self, key: str):
        self.key = key
    
    def suggest(self, system, prompt):
        r = httpx.post("https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": self.key,
                "anthropic-version": "2023-06-01"
            },
            json={
                "model": "claude-3-5-sonnet-20240620",
                "max_tokens": 350,
                "system": system,
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=30)
        r.raise_for_status()
        return r.json()["content"][0]["text"].strip()


class LocalProvider:
    def suggest(self, system, prompt):
        title = "Recommended Title"
        desc = f"Discover {title} across the EU. Find, compare, and contact trusted businesses."
        jsonld = {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "headline": title,
            "description": desc
        }
        return json.dumps({
            "title": title,
            "description": desc,
            "tags": ["eu", "directory", "business"],
            "jsonld": jsonld,
            "images": [{
                "keyword": "europe business map gradient",
                "alt": "EU map graphic",
                "idea": "Abstract map with stars"
            }]
        })


def get_provider():
    if os.getenv("AI_PROVIDER") == "openai" and os.getenv("OPENAI_API_KEY"):
        return OpenAIProvider(os.getenv("OPENAI_API_KEY"))
    if os.getenv("AI_PROVIDER") == "anthropic" and os.getenv("ANTHROPIC_API_KEY"):
        return AnthropicProvider(os.getenv("ANTHROPIC_API_KEY"))
    return LocalProvider()