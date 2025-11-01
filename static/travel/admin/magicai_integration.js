/**
 * MagicAI Integration for Travel Admin
 * Provides AJAX content generation capabilities
 */

document.addEventListener('DOMContentLoaded', function () {
    // Add MagicAI generation button to article admin
    if (window.location.pathname.includes('/travel/article/')) {
        addMagicAIButton();
    }
});

function addMagicAIButton() {
    // Find the content textarea
    const contentField = document.getElementById('id_content');
    if (!contentField) return;

    // Create MagicAI generation panel
    const magicAIPanel = document.createElement('div');
    magicAIPanel.className = 'magicai-panel';
    magicAIPanel.innerHTML = `
        <div class="magicai-header">
            <h3>🤖 MagicAI Content Generation</h3>
        </div>
        <div class="magicai-controls">
            <div class="magicai-options">
                <label for="magicai-prompt-type">Content Type:</label>
                <select id="magicai-prompt-type">
                    <option value="city_guide">City Guide</option>
                    <option value="attraction">Attraction Guide</option>
                    <option value="restaurant">Restaurant Review</option>
                    <option value="itinerary">Travel Itinerary</option>
                </select>
            </div>
            <div class="magicai-actions">
                <button type="button" id="magicai-generate-btn" class="button">
                    ✨ Generate Content
                </button>
                <button type="button" id="magicai-enhance-btn" class="button">
                    🔧 Enhance Existing
                </button>
            </div>
            <div class="magicai-status" id="magicai-status"></div>
        </div>
    `;

    // Insert panel before the content field
    const contentFieldGroup = contentField.closest('.form-row, .field-content');
    if (contentFieldGroup) {
        contentFieldGroup.parentNode.insertBefore(magicAIPanel, contentFieldGroup);
    }

    // Add event listeners
    document.getElementById('magicai-generate-btn').addEventListener('click', generateContent);
    document.getElementById('magicai-enhance-btn').addEventListener('click', enhanceContent);
}

function generateContent() {
    const statusDiv = document.getElementById('magicai-status');
    const generateBtn = document.getElementById('magicai-generate-btn');
    const promptType = document.getElementById('magicai-prompt-type').value;

    // Get article ID from URL
    const urlParts = window.location.pathname.split('/');
    const articleId = urlParts[urlParts.indexOf('article') + 1];

    if (!articleId || articleId === 'add') {
        showStatus('Please save the article first before generating content.', 'warning');
        return;
    }

    // Show loading state
    generateBtn.disabled = true;
    generateBtn.textContent = '⏳ Generating...';
    showStatus('Generating content with MagicAI...', 'info');

    // Prepare form data
    const formData = new FormData();
    formData.append('article_id', articleId);
    formData.append('prompt_type', promptType);
    formData.append('csrfmiddlewaretoken', getCSRFToken());

    // Make AJAX request
    fetch('/admin/travel/article/magicai-generate/', {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update form fields with generated content
                if (data.title && !document.getElementById('id_title').value) {
                    document.getElementById('id_title').value = data.title;
                }

                if (data.content) {
                    document.getElementById('id_content').value = data.content;
                }

                if (data.excerpt && !document.getElementById('id_excerpt').value) {
                    document.getElementById('id_excerpt').value = data.excerpt;
                }

                if (data.meta_description && !document.getElementById('id_meta_description').value) {
                    document.getElementById('id_meta_description').value = data.meta_description;
                }

                showStatus('✅ Content generated successfully!', 'success');
            } else {
                showStatus(`❌ Generation failed: ${data.error}`, 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showStatus('❌ Network error occurred', 'error');
        })
        .finally(() => {
            generateBtn.disabled = false;
            generateBtn.textContent = '✨ Generate Content';
        });
}

function enhanceContent() {
    const contentField = document.getElementById('id_content');
    const currentContent = contentField.value.trim();

    if (!currentContent) {
        showStatus('No existing content to enhance. Use "Generate Content" instead.', 'warning');
        return;
    }

    showStatus('Enhancement feature coming soon! 🚧', 'info');
}

function showStatus(message, type = 'info') {
    const statusDiv = document.getElementById('magicai-status');
    statusDiv.textContent = message;
    statusDiv.className = `magicai-status status-${type}`;

    // Auto-clear after 5 seconds for success messages
    if (type === 'success') {
        setTimeout(() => {
            statusDiv.textContent = '';
            statusDiv.className = 'magicai-status';
        }, 5000);
    }
}

function getCSRFToken() {
    // Get CSRF token from cookie
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];

    return cookieValue || document.querySelector('[name=csrfmiddlewaretoken]')?.value;
}

// Auto-suggest based on article title and location
document.addEventListener('DOMContentLoaded', function () {
    const titleField = document.getElementById('id_title');
    const promptTypeSelect = document.getElementById('magicai-prompt-type');

    if (titleField && promptTypeSelect) {
        titleField.addEventListener('input', function () {
            const title = this.value.toLowerCase();

            if (title.includes('restaurant') || title.includes('dining')) {
                promptTypeSelect.value = 'restaurant';
            } else if (title.includes('itinerary') || title.includes('day')) {
                promptTypeSelect.value = 'itinerary';
            } else if (title.includes('museum') || title.includes('cathedral') || title.includes('attraction')) {
                promptTypeSelect.value = 'attraction';
            } else {
                promptTypeSelect.value = 'city_guide';
            }
        });
    }
});