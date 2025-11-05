# Plans & Visibility System Documentation

## Overview
The Plans & Visibility system provides comprehensive content monetization, featuring, and SEO control based on subscription tiers. It enables plan-based content visibility, weighted ordering, AI boosting, and sitemap management.

## Features

### 📋 **Plan Management**
- **Three-Tier System**: Free, Product Page, Premium plans
- **Flexible Entitlements**: JSON-defined feature permissions
- **Priority Weighting**: Numerical sorting weights for content ordering
- **Highlight Features**: Marketing-friendly feature lists
- **Admin Management**: Full CRUD interface for plan configuration

### 🎯 **Visibility Profiles**
- **Plan Association**: Each profile linked to a specific plan
- **Featured Content**: Boost visibility with featured flags and weights
- **SEO Control**: Sitemap inclusion and noindex overrides
- **Badge System**: Custom badges for enhanced presentation
- **Content Linking**: Attach to CMS pages and blog posts

### 🚀 **Content Enhancement**
- **Plan-Aware Ordering**: Weighted sorting based on plan priority
- **AI Boosting**: Enhanced AI suggestions for higher-tier plans
- **SEO Optimization**: Plan-based indexing and sitemap control
- **Frontend Integration**: API endpoints for plan-aware features

## Plan Structure

### Free Plan
```json
{
  "key": "free",
  "name": "Free",
  "description": "Basic presence.",
  "priority_weight": 0,
  "highlights": ["Basic meta", "Listed in category", "Upgrade-ready"],
  "entitlements": {
    "jsonld": false,
    "custom_og": false,
    "canonical_control": true,
    "ai_boost": 0,
    "max_media": 3,
    "sitemap": true,
    "allow_featured": false
  }
}
```

### Product Page Plan
```json
{
  "key": "product",
  "name": "Product Page",
  "description": "Richer profile, priority placement.",
  "priority_weight": 10,
  "highlights": ["Priority lists", "Custom OG", "More media"],
  "entitlements": {
    "jsonld": true,
    "custom_og": true,
    "canonical_control": true,
    "ai_boost": 1,
    "max_media": 12,
    "sitemap": true,
    "allow_featured": true
  }
}
```

### Premium Plan
```json
{
  "key": "premium",
  "name": "Premium",
  "description": "EU-wide visibility, featured boosts.",
  "priority_weight": 25,
  "highlights": ["EU-wide targeting", "Full JSON-LD", "Featured & badges"],
  "entitlements": {
    "jsonld": true,
    "custom_og": true,
    "canonical_control": true,
    "ai_boost": 2,
    "max_media": 30,
    "sitemap": true,
    "allow_featured": true
  }
}
```

## Database Models

### Plan Model
```python
class Plan(models.Model):
    key = models.CharField(max_length=32, unique=True, choices=PLAN_KEYS)
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    entitlements = models.JSONField(default=dict)
    highlights = models.JSONField(default=list)
    priority_weight = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
```

### VisibilityProfile Model
```python
class VisibilityProfile(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    include_in_sitemap = models.BooleanField(default=True)
    force_noindex = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    featured_weight = models.IntegerField(default=0)
    badges = models.JSONField(default=list)
```

### Content Integration
Both `Page` and `Post` models include:
```python
visibility = models.ForeignKey(VisibilityProfile, on_delete=models.PROTECT, null=True, blank=True)

# CMS Pages
def is_indexable(self):
    if self.visibility and self.visibility.force_noindex:
        return False
    return not self.noindex

def effective_jsonld_allowed(self):
    plan = self.visibility.plan if self.visibility else None
    return bool(plan and plan.entitlements.get("jsonld", False))

# Blog Posts  
def list_weight(self):
    base = 0
    if self.visibility and self.visibility.plan:
        base += self.visibility.plan.priority_weight
    if self.visibility and self.visibility.featured:
        base += self.visibility.featured_weight
    return base
```

## Plan-Aware Features

### 🔄 **Weighted Content Ordering**
Blog posts are automatically sorted by combined weight:
- **Plan Priority**: Base weight from plan (0, 10, 25)
- **Featured Boost**: Additional weight from featured status
- **Recency Fallback**: Published date for tie-breaking

```python
# In blog/views.py PostList
posts = list(qs.select_related("category", "author", "visibility__plan"))
posts.sort(key=lambda p: (p.list_weight(), p.published_at or p.created_at), reverse=True)
```

### 🤖 **AI Boosting by Plan**
Higher-tier plans receive enhanced AI suggestions:
- **Free Plan** (ai_boost: 0): Standard AI suggestions
- **Product Plan** (ai_boost: 1): Enhanced tags + JSON-LD if entitled
- **Premium Plan** (ai_boost: 2): Maximum AI enhancement

```python
# AI boost implementation
plan = getattr(getattr(obj, "visibility", None), "plan", None)
boost = int(plan.entitlements.get("ai_boost", 0)) if plan else 0
if boost > 0:
    data.setdefault("tags", [])
    data["tags"] = list({*data["tags"], "eu", "visibility", "listacross"})
    if isinstance(data.get("jsonld"), dict) and plan.entitlements.get("jsonld", False):
        data["jsonld"].setdefault("about", "EU-wide business discovery")
```

### 🗺️ **Visibility-Aware Sitemaps**
Sitemaps respect plan visibility settings:
- **include_in_sitemap**: Controls sitemap inclusion
- **force_noindex**: Overrides content noindex settings
- **Plan entitlements**: Respects plan-level sitemap permissions

```python
def _ok(self, obj):
    if obj.visibility and not obj.visibility.include_in_sitemap:
        return False
    return not obj.noindex
```

## Admin Interface

### Plan Administration
- **List View**: Shows name, key, priority weight, and active status
- **Filter Options**: Filter by active status
- **Search Fields**: Search by name, key, and description
- **Fieldsets**: Organized into Basics and Entitlements sections

### VisibilityProfile Administration
- **List View**: Shows plan, featured status, weights, and SEO settings
- **Filter Options**: Filter by plan, featured, sitemap inclusion, noindex
- **Comprehensive Controls**: All visibility settings in one interface

### Content Administration Updates
Both CMS Pages and Blog Posts now include:
- **Plan Key Column**: Shows associated plan in list view
- **Visibility Fieldset**: Dedicated section for visibility management
- **Enhanced Filtering**: Filter content by associated plan
- **Plan Display**: Clear indication of content's plan tier

## API Endpoints

### Plans API
```
GET /api/plans/
```

**Response:**
```json
{
  "count": 3,
  "results": [
    {
      "id": 1,
      "key": "free",
      "name": "Free",
      "description": "Basic presence.",
      "highlights": ["Basic meta", "Listed in category", "Upgrade-ready"],
      "entitlements": {
        "jsonld": false,
        "custom_og": false,
        "canonical_control": true,
        "ai_boost": 0,
        "max_media": 3,
        "sitemap": true,
        "allow_featured": false
      },
      "priority_weight": 0,
      "is_active": true
    }
  ]
}
```

### Enhanced Content APIs
All existing CMS and blog APIs now return plan-aware data:
- **Weighted Ordering**: Blog posts sorted by plan priority
- **Plan Information**: Visibility profile data in responses
- **Feature Filtering**: Content filtered by plan entitlements

## Management Commands

### Seed Plans Command
```bash
python manage.py seed_plans
```

Creates or updates the three default plans with proper entitlements and highlights.

**Output:**
```
Created plan free
Created plan product  
Created plan premium
```

## SEO & Sitemap Integration

### Enhanced Sitemaps
- **PageSitemap**: CMS pages with visibility filtering
- **PostSitemap**: Blog posts with plan-aware inclusion
- **Business Integration**: Combines with existing business sitemaps
- **Automatic Filtering**: Respects noindex and visibility settings

**Sitemap URL Structure:**
- Pages: `/{language}/{slug}/`
- Posts: `/{language}/blog/{slug}/`
- Priority: Pages (0.6), Posts (0.5)
- Change Frequency: Weekly for both

### SEO Control Hierarchy
1. **Content Level**: Individual noindex/nofollow settings
2. **Visibility Level**: force_noindex override
3. **Plan Level**: Entitlement-based features
4. **Global Level**: System-wide SEO settings

## Usage Examples

### Creating Visibility Profiles
```python
from plans.models import Plan, VisibilityProfile

# Get plans
premium_plan = Plan.objects.get(key='premium')

# Create high-visibility profile
profile = VisibilityProfile.objects.create(
    plan=premium_plan,
    featured=True,
    featured_weight=25,
    include_in_sitemap=True,
    force_noindex=False,
    badges=["Premium", "Featured", "EU-wide"]
)
```

### Assigning to Content
```python
from cms.models import Page
from blog.models import Post

# Assign to CMS page
page = Page.objects.get(slug='about-us')
page.visibility = profile
page.save()

# Assign to blog post
post = Post.objects.get(slug='welcome-blog')
post.visibility = profile
post.save()
```

### Checking Plan Features
```python
# Check if content can use JSON-LD
if page.effective_jsonld_allowed():
    # Generate structured data
    
# Get content weight for ordering
weight = post.list_weight()  # Returns combined plan + featured weight

# Check indexability
if page.is_indexable():
    # Include in search results
```

### Frontend Plan Detection
```javascript
// Get available plans for upsell
const plans = await fetch('/api/plans/').then(r => r.json());

// Check plan entitlements
plans.results.forEach(plan => {
  console.log(`${plan.name}: ${plan.entitlements.ai_boost} AI boost`);
});

// Display plan highlights
const highlights = plans.results.find(p => p.key === 'premium').highlights;
```

## Performance Considerations

### Database Optimization
- **Select Related**: All queries use select_related for visibility/plan
- **Indexed Fields**: Plan key and visibility relationships indexed
- **Efficient Sorting**: In-memory sorting after database filtering

### Caching Strategies
- **Plan Data**: Cache plan entitlements for frequent access
- **Visibility Profiles**: Cache profile data with content
- **Weighted Lists**: Consider caching sorted content lists

### Query Optimization
```python
# Efficient plan-aware queries
posts = Post.objects.select_related('visibility__plan', 'category', 'author')
             .filter(is_published=True, language='en')
```

## Security & Permissions

### Plan Protection
- **PROTECT on Delete**: Prevents accidental plan deletion
- **Admin Permissions**: Only staff can manage plans
- **Entitlement Validation**: Server-side validation of plan features

### Content Security
- **Plan Verification**: Server-side plan entitlement checking
- **Visibility Enforcement**: Automatic application of visibility rules
- **SEO Protection**: Prevents indexing of restricted content

## Migration & Deployment

### Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py seed_plans
```

### Existing Content
- **Graceful Defaults**: Content without visibility uses safe defaults
- **Bulk Assignment**: Use admin or shell to assign visibility profiles
- **Backward Compatibility**: System works with mixed visibility states

### Production Considerations
- **Plan Strategy**: Define clear plan differentiation
- **Pricing Integration**: Connect with payment systems
- **Analytics**: Track plan effectiveness and upgrades
- **Support Tools**: Admin tools for plan management

## Future Enhancements

### Planned Features
- **Dynamic Pricing**: API-driven plan pricing
- **Usage Analytics**: Plan performance tracking  
- **A/B Testing**: Plan feature experimentation
- **Bulk Operations**: Mass visibility profile updates

### Integration Opportunities
- **Payment Systems**: Stripe/PayPal integration
- **Marketing Tools**: Plan-based email campaigns
- **Analytics**: Plan conversion tracking
- **CRM Integration**: Customer plan history

The Plans & Visibility system provides a robust foundation for content monetization while maintaining SEO best practices and user experience optimization! 🚀💰