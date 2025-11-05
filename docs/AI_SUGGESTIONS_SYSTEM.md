# AI Suggestions System Documentation

## Overview
The AI Suggestions system provides intelligent SEO recommendations for CMS pages and blog posts using OpenAI GPT-4o-mini, Anthropic Claude, or local heuristic fallbacks.

## Features

### 🤖 AI Providers
- **OpenAI Provider**: Uses GPT-4o-mini for intelligent SEO suggestions
- **Anthropic Provider**: Uses Claude-3.5-sonnet for content optimization
- **Local Provider**: Heuristic fallback when no API keys are configured

### 🎯 SEO Intelligence
- **Smart Titles**: Generate compelling meta titles (≤60 characters)
- **Rich Descriptions**: Create engaging meta descriptions (120-160 characters)
- **Keyword Tags**: Extract relevant tags for content categorization
- **JSON-LD Structured Data**: Generate schema.org markup
- **Image Suggestions**: Recommend keywords with source links

### 🔧 Integration Points
- **Django Admin Actions**: Bulk AI suggestions for selected items
- **REST API**: Programmatic access for frontend applications
- **Automatic Fallbacks**: Graceful degradation when APIs are unavailable

## Configuration

### Environment Variables (.env)
```bash
# For OpenAI GPT-4o-mini suggestions
OPENAI_API_KEY=sk-your-openai-api-key-here
AI_PROVIDER=openai

# Alternative: For Anthropic Claude suggestions  
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
AI_PROVIDER=anthropic

# Local fallback (no API keys needed)
AI_PROVIDER=local
```

### Django Settings
```python
# Automatically configured in settings.py
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
AI_PROVIDER = os.getenv("AI_PROVIDER", "openai" if OPENAI_API_KEY else ("anthropic" if ANTHROPIC_API_KEY else "local"))

INSTALLED_APPS += ["assist"]
```

## Usage

### Django Admin Interface

#### For CMS Pages:
1. Go to **Admin** → **CMS** → **Pages**
2. Select one or more pages
3. Choose **Actions** → **AI: Suggest SEO (title/description/JSON-LD/images)**
4. Click **Go** to apply suggestions

#### For Blog Posts:
1. Go to **Admin** → **Blog** → **Posts**  
2. Select one or more posts
3. Choose **Actions** → **AI: Suggest SEO (title/description/JSON-LD/images)**
4. Click **Go** to apply suggestions

#### What Gets Updated:
- ✅ **meta_title**: Only if currently empty
- ✅ **meta_description**: Only if currently empty  
- ✅ **meta_json._ai**: Always updated with full AI response
- ✅ **meta_json._ai.image_sources**: Generated image source links

### REST API

#### Endpoint
```
POST /api/ai/suggest/
```

#### Request Body
```json
{
  "title": "About Our European Business Directory",
  "excerpt": "ListAcrossEU helps you discover businesses across Europe", 
  "body": "Our comprehensive directory features thousands of businesses...",
  "url": "/about",
  "kind": "page",  // optional: "page" or "post"
  "id": 1          // optional: auto-apply to existing object
}
```

#### Response
```json
{
  "ok": true,
  "data": {
    "title": "European Business Directory - ListAcrossEU", 
    "description": "Discover trusted businesses across all EU countries. Find, compare, and connect with local services in your area or anywhere in Europe.",
    "tags": ["european business", "directory", "eu services", "local businesses"],
    "jsonld": {
      "@context": "https://schema.org",
      "@type": "WebPage", 
      "headline": "European Business Directory - ListAcrossEU",
      "description": "Discover trusted businesses across all EU countries..."
    },
    "images": [
      {
        "keyword": "european business directory", 
        "alt": "European business network visualization",
        "idea": "Modern map of Europe with business connection lines"
      }
    ]
  }
}
```

### JavaScript Frontend Integration
```javascript
// Generate AI suggestions for content
async function getAISuggestions(content) {
  const response = await fetch('/api/ai/suggest/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      title: content.title,
      excerpt: content.excerpt, 
      body: content.body,
      url: content.url
    })
  });
  
  const result = await response.json();
  return result.data;
}

// Auto-apply to existing page/post
async function applySuggestionsToPage(pageId) {
  const response = await fetch('/api/ai/suggest/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      kind: 'page',
      id: pageId,
      title: 'About Us',
      body: 'Our company description...'
    })
  });
  
  return response.json();
}
```

## AI Response Structure

### Generated Data Fields
- **title**: SEO-optimized title (≤60 chars)
- **description**: Compelling meta description (120-160 chars)
- **tags**: Array of relevant keywords
- **jsonld**: Schema.org structured data object
- **images**: Array of image suggestions with keywords

### Image Sources Generation
Each image keyword automatically generates:
```json
{
  "keyword": "european business map",
  "unsplash_search": "https://unsplash.com/s/photos/european+business+map",
  "pexels_search": "https://www.pexels.com/search/european+business+map/", 
  "placeholder": "https://placehold.co/1200x630?text=european+business+map"
}
```

## Provider Details

### OpenAI Provider
- **Model**: gpt-4o-mini
- **Temperature**: 0.6 (balanced creativity/consistency)
- **Timeout**: 30 seconds
- **Cost**: ~$0.0015 per 1K tokens (very affordable)

### Anthropic Provider  
- **Model**: claude-3-5-sonnet-20240620
- **Max Tokens**: 350
- **Timeout**: 30 seconds
- **Cost**: ~$0.003 per 1K tokens

### Local Provider
- **Features**: No API calls, instant responses
- **Limitations**: Generic suggestions, no content analysis
- **Use Case**: Development, API quota exhaustion fallback

## Data Storage

### meta_json Field Structure
```json
{
  "_ai": {
    "title": "AI-generated title",
    "description": "AI-generated description", 
    "tags": ["tag1", "tag2"],
    "jsonld": { "@type": "WebPage", ... },
    "images": [
      { "keyword": "...", "alt": "...", "idea": "..." }
    ],
    "image_sources": [
      {
        "keyword": "business directory",
        "unsplash_search": "https://unsplash.com/s/photos/business+directory",
        "pexels_search": "https://www.pexels.com/search/business+directory/",
        "placeholder": "https://placehold.co/1200x630?text=business+directory"
      }
    ]
  }
}
```

## Error Handling

### API Failures
- **Network Issues**: Automatic fallback to LocalProvider
- **Invalid JSON**: Parse error recovery with text-based suggestions  
- **Rate Limits**: Graceful degradation with informative messages
- **Timeout**: 30-second timeout prevents hanging requests

### Admin Interface
- **Success Messages**: "AI suggestions applied to N item(s)."
- **Error Messages**: Detailed error descriptions in Django messages
- **Partial Failures**: Continue processing other items if one fails

### API Responses
```json
// Success
{ "ok": true, "data": {...} }

// Error  
{ "ok": false, "error": "API rate limit exceeded", "fallback": true }
```

## Performance Considerations

### Batch Processing
- Admin actions process multiple items sequentially
- Each item gets individual AI analysis for accuracy
- Progress feedback through Django messages

### Caching Strategy
- No built-in caching (responses are content-specific)
- Consider implementing Redis caching for repeated content
- Local provider responses are deterministic (cache-friendly)

### Rate Limiting
- OpenAI: 500 RPM default (adjustable)
- Anthropic: 100 RPM default (adjustable)
- Local: No limits (instant)

## Security

### API Key Protection
- Environment variables only (never committed to code)
- Settings.py safely loads from environment
- Optional configuration (system works without keys)

### Permission Controls
- Admin actions: Requires staff permissions
- API endpoint: Currently AllowAny (⚠️ tighten for production)
- Content validation: Input sanitization recommended

### Production Recommendations
```python
# Tighten API permissions
class AISuggest(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
```

## Troubleshooting

### Common Issues

#### "No changes detected" in admin
- Check that meta_title/meta_description are empty
- AI only updates empty fields to prevent overwriting

#### API timeout errors  
- Increase timeout in providers.py
- Check network connectivity to AI services
- Verify API keys are valid

#### Local provider always used
- Verify environment variables are set
- Check AI_PROVIDER setting
- Ensure .env file is loaded

### Debug Commands
```bash
# Check current provider
python manage.py shell -c "from assist.providers import get_provider; print(type(get_provider()))"

# Test API connectivity
python manage.py shell -c "from assist.seo import suggest_for; print(suggest_for('Test', 'Test content'))"

# Check settings
python manage.py shell -c "from django.conf import settings; print(f'Provider: {settings.AI_PROVIDER}')"
```

## Development

### Adding New Providers
1. Create provider class in `assist/providers.py`
2. Implement `suggest(system, prompt)` method
3. Add to `get_provider()` function
4. Update environment variable handling

### Customizing Prompts
Edit the SYSTEM prompt in `assist/seo.py`:
```python
SYSTEM = (
    "You write concise SEO for a European business directory (ListAcross EU). "
    "Reply with strict JSON. Keys: title, description, tags(array), jsonld(object), images(array of {keyword,alt,idea}). "
    "Title<=60 chars, desc 120-160 chars."
)
```

### Testing
```python
# Unit test example
def test_ai_suggestions():
    from assist.seo import suggest_for
    result = suggest_for("Test Page", "Test excerpt", "Test body")
    assert "title" in result
    assert len(result["title"]) <= 60
```

The AI Suggestions system is now fully operational and ready to enhance your content with intelligent SEO recommendations! 🚀