def keywords_to_sources(keywords: list[str]):
    out = []
    for k in keywords[:5]:
        q = k.replace(" ", "+")
        out.append({
            "keyword": k,
            "unsplash_search": f"https://unsplash.com/s/photos/{q}",
            "pexels_search": f"https://www.pexels.com/search/{q}/",
            "placeholder": f"https://placehold.co/1200x630?text={q}"
        })
    return out