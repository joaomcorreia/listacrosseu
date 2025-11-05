from django.contrib import admin
from django.utils.safestring import mark_safe

SEO_PREVIEW_HTML = """
<div style="margin-bottom: 20px;">
    <div id="serp-preview-container" style="border: 1px solid #ddd; border-radius: 8px; padding: 16px; background: #fff; font-family: Arial, sans-serif;">
        <h4 style="margin: 0 0 12px 0; color: #333; font-size: 14px; font-weight: 600;">🔍 Search Engine Preview</h4>
        
        <!-- Google Preview -->
        <div id="google-preview" style="margin-bottom: 16px; padding: 12px; border: 1px solid #e0e0e0; border-radius: 6px; background: #fafafa;">
            <div style="font-size: 12px; color: #5f6368; margin-bottom: 8px; font-weight: 500;">Google Search Result:</div>
            <div id="serp-title" style="color: #1a0dab; font-size: 18px; line-height: 1.3; cursor: pointer; margin-bottom: 2px; font-weight: normal;">Your Page Title Will Appear Here</div>
            <div id="serp-url" style="color: #006621; font-size: 14px; margin-bottom: 4px;">https://listacrosseu.eu/example-page</div>
            <div id="serp-desc" style="color: #4d5156; font-size: 13px; line-height: 1.4;">Your meta description will appear here. Make it compelling to encourage clicks from search results.</div>
        </div>

        <!-- Bing Preview -->
        <div id="bing-preview" style="margin-bottom: 16px; padding: 12px; border: 1px solid #e0e0e0; border-radius: 6px; background: #f8f9fa;">
            <div style="font-size: 12px; color: #666; margin-bottom: 8px; font-weight: 500;">Bing Search Result:</div>
            <div id="bing-title" style="color: #0066cc; font-size: 18px; line-height: 1.3; cursor: pointer; margin-bottom: 2px; font-weight: normal;">Your Page Title Will Appear Here</div>
            <div id="bing-url" style="color: #008000; font-size: 14px; margin-bottom: 4px;">https://listacrosseu.eu/example-page</div>
            <div id="bing-desc" style="color: #666; font-size: 13px; line-height: 1.4;">Your meta description will appear here. Make it compelling to encourage clicks from search results.</div>
        </div>

        <!-- Character Counters -->
        <div style="display: flex; gap: 20px; font-size: 12px; color: #666; border-top: 1px solid #eee; padding-top: 12px;">
            <span>📝 Title: <span id="title-count" style="font-weight: 600; color: #333;">0</span><span style="color: #999;">/70</span></span>
            <span>📄 Description: <span id="desc-count" style="font-weight: 600; color: #333;">0</span><span style="color: #999;">/160</span></span>
            <span>🌐 OG Title: <span id="og-title-count" style="font-weight: 600; color: #333;">0</span><span style="color: #999;">/120</span></span>
            <span>📱 OG Desc: <span id="og-desc-count" style="font-weight: 600; color: #333;">0</span><span style="color: #999;">/200</span></span>
        </div>

        <!-- Status Indicators -->
        <div id="seo-status" style="margin-top: 12px; font-size: 12px;">
            <span id="title-status" style="margin-right: 12px;"></span>
            <span id="desc-status"></span>
        </div>
    </div>
</div>

<script>
function initSEOPreview() {
    const titleField = document.querySelector('#id_meta_title');
    const descField = document.querySelector('#id_meta_description');
    const ogTitleField = document.querySelector('#id_og_title');
    const ogDescField = document.querySelector('#id_og_description');
    const canonicalField = document.querySelector('#id_canonical_url');
    
    if (!titleField || !descField) return; // Fields not loaded yet
    
    const elements = {
        serpTitle: document.querySelector('#serp-title'),
        serpDesc: document.querySelector('#serp-desc'),
        serpUrl: document.querySelector('#serp-url'),
        bingTitle: document.querySelector('#bing-title'),
        bingDesc: document.querySelector('#bing-desc'),
        bingUrl: document.querySelector('#bing-url'),
        titleCount: document.querySelector('#title-count'),
        descCount: document.querySelector('#desc-count'),
        ogTitleCount: document.querySelector('#og-title-count'),
        ogDescCount: document.querySelector('#og-desc-count'),
        titleStatus: document.querySelector('#title-status'),
        descStatus: document.querySelector('#desc-status')
    };
    
    function updatePreview() {
        const title = titleField.value || 'Your Page Title Will Appear Here';
        const desc = descField.value || 'Your meta description will appear here. Make it compelling to encourage clicks from search results.';
        const canonical = canonicalField ? canonicalField.value : '';
        const ogTitle = ogTitleField ? ogTitleField.value : '';
        const ogDesc = ogDescField ? ogDescField.value : '';
        
        // Update SERP previews
        elements.serpTitle.textContent = title;
        elements.serpDesc.textContent = desc;
        elements.bingTitle.textContent = title;
        elements.bingDesc.textContent = desc;
        
        // Update URL if canonical is provided
        if (canonical && elements.serpUrl) {
            elements.serpUrl.textContent = canonical;
            elements.bingUrl.textContent = canonical;
        }
        
        // Update character counts
        elements.titleCount.textContent = titleField.value.length;
        elements.descCount.textContent = descField.value.length;
        if (elements.ogTitleCount) elements.ogTitleCount.textContent = ogTitle.length;
        if (elements.ogDescCount) elements.ogDescCount.textContent = ogDesc.length;
        
        // Update status indicators
        const titleLen = titleField.value.length;
        const descLen = descField.value.length;
        
        // Title status
        if (titleLen === 0) {
            elements.titleStatus.innerHTML = '⚠️ <span style="color: #d93025;">Missing title</span>';
        } else if (titleLen < 30) {
            elements.titleStatus.innerHTML = '📏 <span style="color: #ea4335;">Title too short</span>';
        } else if (titleLen > 70) {
            elements.titleStatus.innerHTML = '📏 <span style="color: #ea4335;">Title too long</span>';
        } else {
            elements.titleStatus.innerHTML = '✅ <span style="color: #34a853;">Title length good</span>';
        }
        
        // Description status
        if (descLen === 0) {
            elements.descStatus.innerHTML = '⚠️ <span style="color: #d93025;">Missing description</span>';
        } else if (descLen < 120) {
            elements.descStatus.innerHTML = '📏 <span style="color: #fbbc04;">Description could be longer</span>';
        } else if (descLen > 160) {
            elements.descStatus.innerHTML = '📏 <span style="color: #ea4335;">Description too long</span>';
        } else {
            elements.descStatus.innerHTML = '✅ <span style="color: #34a853;">Description length good</span>';
        }
        
        // Update character count colors
        elements.titleCount.style.color = titleLen > 70 ? '#ea4335' : titleLen < 30 ? '#fbbc04' : '#34a853';
        elements.descCount.style.color = descLen > 160 ? '#ea4335' : descLen < 120 ? '#fbbc04' : '#34a853';
    }
    
    // Bind event listeners
    titleField.addEventListener('input', updatePreview);
    descField.addEventListener('input', updatePreview);
    if (ogTitleField) ogTitleField.addEventListener('input', updatePreview);
    if (ogDescField) ogDescField.addEventListener('input', updatePreview);
    if (canonicalField) canonicalField.addEventListener('input', updatePreview);
    
    // Initial update
    updatePreview();
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initSEOPreview);
} else {
    initSEOPreview();
}

// Re-initialize when Django admin loads content via AJAX
document.addEventListener('DOMContentLoaded', function() {
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.addedNodes.length > 0) {
                setTimeout(initSEOPreview, 100); // Small delay to ensure fields are ready
            }
        });
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
});
</script>

<style>
/* Hover effects for SERP previews */
#serp-title:hover, #bing-title:hover {
    text-decoration: underline;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    #serp-preview-container > div {
        flex-direction: column !important;
        gap: 10px !important;
    }
}

/* Enhanced visual indicators */
.seo-field-group {
    margin-bottom: 15px;
}

.seo-field-group label {
    font-weight: 600 !important;
    color: #333 !important;
}

/* Character count styling */
#title-count, #desc-count, #og-title-count, #og-desc-count {
    font-family: 'Courier New', monospace;
    background: #f0f0f0;
    padding: 2px 4px;
    border-radius: 3px;
}
</style>
"""

class SEOFirstAdmin(admin.ModelAdmin):
    """
    Base admin class that shows SEO fields first with live SERP preview.
    
    Usage:
        class YourModelAdmin(SEOFirstAdmin):
            fieldsets = (
                SEOFirstAdmin.seo_fieldset,  # SEO at top
                ("Content", {"fields": ("title", "content", ...)}),
            )
    """
    
    seo_fieldset = ("🔍 SEO Settings & Search Preview", {
        "fields": (
            "meta_title",
            "meta_description", 
            "canonical_url",
            "robots",
            "og_title",
            "og_description",
            "og_image",
        ),
        "description": mark_safe(SEO_PREVIEW_HTML),
        "classes": ("wide",),
    })
    
    def get_fieldsets(self, request, obj=None):
        """
        Ensure SEO fieldset appears first if not already defined.
        Subclasses should override fieldsets instead of this method.
        """
        fieldsets = super().get_fieldsets(request, obj)
        if not fieldsets:
            # If no fieldsets defined, create a basic one with SEO first
            seo_fields = [f.name for f in self.model._meta.fields if f.name.startswith(('meta_', 'og_', 'canonical', 'robots'))]
            other_fields = [f.name for f in self.model._meta.fields if not f.name.startswith(('meta_', 'og_', 'canonical', 'robots')) and f.name != 'id']
            
            fieldsets = [
                self.seo_fieldset,
                ("Content", {"fields": other_fields}) if other_fields else None
            ]
            fieldsets = [fs for fs in fieldsets if fs is not None]
        
        return fieldsets
    
    class Media:
        css = {
            'all': ('admin/css/seo-preview.css',)
        }
        js = ('admin/js/seo-preview.js',)