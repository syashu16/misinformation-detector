// DOM Elements
const tabButtons = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');
const resultsTabButtons = document.querySelectorAll('.results-tab-btn');
const resultsTabContents = document.querySelectorAll('.results-tab-content');

const textForm = document.getElementById('text-form');
const urlForm = document.getElementById('url-form');
const imageForm = document.getElementById('image-form');

const textInput = document.getElementById('text-input');
const urlInput = document.getElementById('url-input');
const imageInput = document.getElementById('image-input');
const fileUploadArea = document.getElementById('file-upload-area');
const imagePreview = document.getElementById('image-preview');
const previewImg = document.getElementById('preview-img');
const removeImageBtn = document.getElementById('remove-image');

const loadingOverlay = document.getElementById('loading-overlay');
const resultsSection = document.getElementById('results-section');
const closeResultsBtn = document.getElementById('close-results');
const textCharCount = document.getElementById('text-char-count');

// API Configuration
const API_BASE_URL = 'http://127.0.0.1:5000';

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    console.log('Page loaded, initializing application...');
    
    // Ensure loading overlay is hidden on page load
    if (loadingOverlay) {
        loadingOverlay.style.display = 'none';
    }
    
    initializeEventListeners();
    updateCharCount();
    
    console.log('Application initialized successfully');
});

// Event Listeners
function initializeEventListeners() {
    // Check if all required elements exist
    if (!textForm || !urlForm || !imageForm || !loadingOverlay) {
        console.error('Required DOM elements not found');
        return;
    }
    
    // Tab switching
    tabButtons.forEach(button => {
        button.addEventListener('click', () => switchTab(button.dataset.tab));
    });

    // Results tab switching
    resultsTabButtons.forEach(button => {
        button.addEventListener('click', () => switchResultsTab(button.dataset.resultsTab));
    });

    // Form submissions
    textForm.addEventListener('submit', handleTextAnalysis);
    urlForm.addEventListener('submit', handleUrlAnalysis);
    imageForm.addEventListener('submit', handleImageAnalysis);

    // Character counter for text input
    textInput.addEventListener('input', updateCharCount);

    // File upload handling
    imageInput.addEventListener('change', handleFileSelect);
    fileUploadArea.addEventListener('dragover', handleDragOver);
    fileUploadArea.addEventListener('drop', handleFileDrop);
    removeImageBtn.addEventListener('click', removeSelectedImage);

    // Close results
    closeResultsBtn.addEventListener('click', closeResults);

    // Prevent form submission on Enter in text area
    textInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && e.ctrlKey) {
            e.preventDefault();
            textForm.dispatchEvent(new Event('submit'));
        }
    });
}

// Tab Management
function switchTab(tabName) {
    // Update tab buttons
    tabButtons.forEach(btn => btn.classList.remove('active'));
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');

    // Update tab content
    tabContents.forEach(content => content.classList.remove('active'));
    document.getElementById(`${tabName}-tab`).classList.add('active');

    // Hide results when switching tabs
    hideResults();
}

function switchResultsTab(tabName) {
    // Update results tab buttons
    resultsTabButtons.forEach(btn => btn.classList.remove('active'));
    document.querySelector(`[data-results-tab="${tabName}"]`).classList.add('active');

    // Update results tab content
    resultsTabContents.forEach(content => content.classList.remove('active'));
    document.getElementById(`${tabName}-results`).classList.add('active');
}

// Character Counter
function updateCharCount() {
    const count = textInput.value.length;
    textCharCount.textContent = count;
    
    if (count > 5000) {
        textCharCount.style.color = '#dc3545';
    } else if (count > 4000) {
        textCharCount.style.color = '#ffc107';
    } else {
        textCharCount.style.color = '#6c757d';
    }
}

// File Upload Handling
function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        displayImagePreview(file);
    }
}

function handleDragOver(event) {
    event.preventDefault();
    fileUploadArea.classList.add('drag-over');
}

function handleFileDrop(event) {
    event.preventDefault();
    fileUploadArea.classList.remove('drag-over');
    
    const files = event.dataTransfer.files;
    if (files.length > 0) {
        const file = files[0];
        if (file.type.startsWith('image/')) {
            imageInput.files = files;
            displayImagePreview(file);
        } else {
            showError('Please select a valid image file.');
        }
    }
}

function displayImagePreview(file) {
    const reader = new FileReader();
    reader.onload = function(e) {
        previewImg.src = e.target.result;
        imagePreview.style.display = 'block';
        fileUploadArea.style.display = 'none';
    };
    reader.readAsDataURL(file);
}

function removeSelectedImage() {
    imageInput.value = '';
    imagePreview.style.display = 'none';
    fileUploadArea.style.display = 'block';
    previewImg.src = '';
}

// Analysis Handlers
async function handleTextAnalysis(event) {
    event.preventDefault();
    
    const text = textInput.value.trim();
    if (!text) {
        showError('Please enter some text to analyze.');
        return;
    }

    if (text.length > 5000) {
        showError('Text is too long. Please limit to 5000 characters.');
        return;
    }

    showLoading();
    
    try {
        console.log('Making request to:', `${API_BASE_URL}/api/analyze/text`);
        console.log('Request body:', JSON.stringify({ text: text }));
        
        const response = await fetch(`${API_BASE_URL}/api/analyze/text`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text })
        });

        console.log('Response status:', response.status);
        console.log('Response ok:', response.ok);
        
        const result = await response.json();
        console.log('Response data:', result);
        
        if (response.ok) {
            displayResults(result);
        } else {
            showError(result.error || 'An error occurred during analysis.');
        }
    } catch (error) {
        console.error('Error details:', error);
        console.error('Error message:', error.message);
        console.error('Error stack:', error.stack);
        showError(`Failed to connect to the analysis service. Error: ${error.message}. Please try again.`);
    } finally {
        hideLoading();
    }
}

async function handleUrlAnalysis(event) {
    event.preventDefault();
    
    const url = urlInput.value.trim();
    if (!url) {
        showError('Please enter a URL to analyze.');
        return;
    }

    // Basic URL validation
    try {
        new URL(url);
    } catch {
        showError('Please enter a valid URL (e.g., https://example.com).');
        return;
    }

    showLoading();
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/analyze/url`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url })
        });

        const result = await response.json();
        
        if (response.ok) {
            displayResults(result);
        } else {
            showError(result.error || 'An error occurred during analysis.');
        }
    } catch (error) {
        console.error('Error:', error);
        showError('Failed to connect to the analysis service. Please try again.');
    } finally {
        hideLoading();
    }
}

async function handleImageAnalysis(event) {
    event.preventDefault();
    
    const file = imageInput.files[0];
    if (!file) {
        showError('Please select an image to analyze.');
        return;
    }

    // Validate file size (16MB limit)
    if (file.size > 16 * 1024 * 1024) {
        showError('Image file is too large. Please select an image smaller than 16MB.');
        return;
    }

    // Validate file type
    if (!file.type.startsWith('image/')) {
        showError('Please select a valid image file.');
        return;
    }

    showLoading();
    
    try {
        const formData = new FormData();
        formData.append('image', file);

        const response = await fetch(`${API_BASE_URL}/api/analyze/image`, {
            method: 'POST',
            body: formData
        });

        const result = await response.json();
        
        if (response.ok) {
            displayResults(result);
        } else {
            showError(result.error || 'An error occurred during analysis.');
        }
    } catch (error) {
        console.error('Error:', error);
        showError('Failed to connect to the analysis service. Please try again.');
    } finally {
        hideLoading();
    }
}

// Results Display
function displayResults(data) {
    // Populate risk score
    const scoreElement = document.getElementById('score-number');
    const scoreCircle = document.getElementById('score-circle');
    const riskLevel = document.getElementById('risk-level');
    const riskExplanation = document.getElementById('risk-explanation');

    scoreElement.textContent = data.risk_score;
    
    // Update score circle color based on risk level
    updateScoreCircleColor(scoreCircle, data.risk_score);
    
    // Update risk level text
    const { level, description } = getRiskLevelInfo(data.risk_score);
    riskLevel.textContent = level;
    riskExplanation.textContent = description;

    // Populate red flags
    const redFlagsList = document.getElementById('red-flags-list');
    redFlagsList.innerHTML = '';
    
    if (data.red_flags && data.red_flags.length > 0) {
        data.red_flags.forEach(flag => {
            const li = document.createElement('li');
            li.textContent = flag;
            redFlagsList.appendChild(li);
        });
    } else {
        const li = document.createElement('li');
        li.textContent = 'No significant red flags detected.';
        li.style.color = '#28a745';
        redFlagsList.appendChild(li);
    }

    // Populate verification steps
    const verificationList = document.getElementById('verification-list');
    verificationList.innerHTML = '';
    
    if (data.verification_suggestions && data.verification_suggestions.length > 0) {
        data.verification_suggestions.forEach(step => {
            const li = document.createElement('li');
            li.textContent = step.step || step;
            verificationList.appendChild(li);
        });
    }

    // Populate technical details
    populateTechnicalDetails(data);

    // Populate educational tips
    populateEducationalTips(data);

    // Show results
    showResults();
}

function updateScoreCircleColor(scoreCircle, score) {
    let color;
    if (score >= 70) {
        color = '#dc3545'; // Red
    } else if (score >= 40) {
        color = '#ffc107'; // Yellow
    } else if (score >= 20) {
        color = '#fd7e14'; // Orange
    } else {
        color = '#28a745'; // Green
    }
    
    scoreCircle.style.background = `conic-gradient(from 0deg, ${color} 0%, ${color} ${score}%, #e9ecef ${score}%, #e9ecef 100%)`;
}

function getRiskLevelInfo(score) {
    if (score >= 70) {
        return {
            level: 'HIGH RISK',
            description: 'This content shows multiple indicators of potential misinformation. Exercise extreme caution and verify thoroughly before sharing.'
        };
    } else if (score >= 40) {
        return {
            level: 'MODERATE RISK',
            description: 'This content has some concerning elements. Consider verifying key claims before sharing.'
        };
    } else if (score >= 20) {
        return {
            level: 'LOW RISK',
            description: 'Minor concerns detected, but content appears generally credible. Standard verification recommended if sharing widely.'
        };
    } else {
        return {
            level: 'MINIMAL RISK',
            description: 'Content appears to have good credibility indicators. However, always practice critical thinking and verify important claims.'
        };
    }
}

function populateTechnicalDetails(data) {
    const technicalDetails = document.getElementById('technical-details');
    technicalDetails.innerHTML = '';

    // Use advanced visualization if available
    if (typeof displayAdvancedResults === 'function' && data.analysis && data.analysis.advanced) {
        displayAdvancedResults(data);
        return;
    }

    // Fallback to basic technical details
    if (data.type === 'text') {
        populateTextDetails(technicalDetails, data);
    } else if (data.type === 'url') {
        populateUrlDetails(technicalDetails, data);
    } else if (data.type === 'image') {
        populateImageDetails(technicalDetails, data);
    }

    // Add AI analysis if available
    if (data.analysis && data.analysis.ai) {
        populateAIAnalysis(technicalDetails, data.analysis.ai);
    }
    
    // Add fact-checking results if available
    if (data.analysis && data.analysis.fact_checking) {
        populateFactCheckResults(technicalDetails, data.analysis.fact_checking);
    }
    
    // Add processing summary if available
    if (data.processing_summary) {
        populateProcessingSummary(technicalDetails, data.processing_summary);
    }
}

function populateTextDetails(container, data) {
    const section = createDetailSection('Text Analysis Details', [
        { label: 'Word Count', value: data.analysis?.basic?.word_count || 'N/A' },
        { label: 'Sentiment', value: data.analysis?.basic?.sentiment?.interpretation || 'N/A' },
        { label: 'Emotional Score', value: data.analysis?.basic?.details?.emotional_manipulation || 0 },
        { label: 'Clickbait Score', value: data.analysis?.basic?.details?.clickbait_patterns || 0 },
        { label: 'Source Reliability Score', value: data.analysis?.basic?.details?.source_reliability || 0 }
    ]);
    container.appendChild(section);
}

function populateUrlDetails(container, data) {
    const section = createDetailSection('URL Analysis Details', [
        { label: 'Domain', value: data.domain || 'N/A' },
        { label: 'Protocol', value: data.scheme || 'N/A' },
        { label: 'Page Title', value: data.title || 'N/A' },
        { label: 'External Links', value: data.external_links?.length || 0 },
        { label: 'Social Signals', value: Object.values(data.social_signals || {}).filter(Boolean).length }
    ]);
    container.appendChild(section);
}

function populateImageDetails(container, data) {
    const section = createDetailSection('Image Analysis Details', [
        { label: 'Filename', value: data.filename || 'N/A' },
        { label: 'File Hash', value: data.file_hash?.substring(0, 16) + '...' || 'N/A' },
        { label: 'Format', value: data.image_info?.format || 'N/A' },
        { label: 'Dimensions', value: data.image_info ? `${data.image_info.width}x${data.image_info.height}` : 'N/A' },
        { label: 'Technical Score', value: data.analysis?.technical?.risk_score || 0 }
    ]);
    container.appendChild(section);

    // Add reverse search suggestion
    if (data.reverse_search_info?.suggestion) {
        const reverseSearchDiv = document.createElement('div');
        reverseSearchDiv.className = 'detail-section';
        reverseSearchDiv.innerHTML = `
            <h4><i class="fas fa-search"></i> Reverse Image Search</h4>
            <p>${data.reverse_search_info.suggestion}</p>
        `;
        container.appendChild(reverseSearchDiv);
    }
}

function populateAIAnalysis(container, aiData) {
    const section = document.createElement('div');
    section.className = 'detail-section ai-analysis';
    section.innerHTML = `
        <h4><i class="fas fa-robot"></i> AI Analysis</h4>
        <div class="ai-details">
            <p><strong>AI Risk Score:</strong> ${aiData.risk_score || 0}/100</p>
            <p><strong>Confidence:</strong> ${aiData.ai_confidence || 'Unknown'}</p>
            ${aiData.explanation ? `<p><strong>Explanation:</strong> ${aiData.explanation}</p>` : ''}
        </div>
    `;
    container.appendChild(section);
}

function populateFactCheckResults(container, factCheckData) {
    const section = document.createElement('div');
    section.className = 'detail-section fact-check-analysis';
    section.innerHTML = `
        <h4><i class="fas fa-search"></i> Fact-Check Analysis</h4>
        <div class="fact-check-details">
            <p><strong>Overall Credibility:</strong> ${factCheckData.overall_credibility || 'N/A'}%</p>
            <p><strong>Claims Checked:</strong> ${factCheckData.total_claims || 0}</p>
            ${factCheckData.detailed_checks && factCheckData.detailed_checks.length > 0 ? 
                `<div class="claims-list">
                    <h5>Detailed Fact Checks:</h5>
                    ${factCheckData.detailed_checks.slice(0, 3).map(check => `
                        <div class="claim-item">
                            <p><strong>Claim:</strong> ${check.claim}</p>
                            <p><strong>Verified:</strong> ${check.verified ? 'Yes' : 'No'}</p>
                            <p><strong>Confidence:</strong> ${check.confidence || 'N/A'}%</p>
                        </div>
                    `).join('')}
                </div>` : ''
            }
        </div>
    `;
    container.appendChild(section);
}

function populateProcessingSummary(container, summaryData) {
    const section = document.createElement('div');
    section.className = 'detail-section processing-summary';
    section.innerHTML = `
        <h4><i class="fas fa-cogs"></i> Processing Summary</h4>
        <div class="processing-details">
            <p><strong>Analysis Layers:</strong> ${summaryData.analysis_layers || 0}</p>
            <p><strong>Processing Time:</strong> ${summaryData.total_processing_time ? (summaryData.total_processing_time * 1000).toFixed(0) + 'ms' : 'N/A'}</p>
            <p><strong>Fact Checks Performed:</strong> ${summaryData.fact_checks_performed || 0}</p>
        </div>
    `;
    container.appendChild(section);
}

function populateEducationalTips(data) {
    const educationalTips = document.getElementById('educational-tips');
    educationalTips.innerHTML = '';

    // Add content-specific tips
    if (data.educational_tips && data.educational_tips.length > 0) {
        const tipsSection = document.createElement('div');
        tipsSection.className = 'detail-section';
        tipsSection.innerHTML = `
            <h4><i class="fas fa-lightbulb"></i> Content-Specific Tips</h4>
            <ul class="tips-list">
                ${data.educational_tips.map(tip => `<li>${tip}</li>`).join('')}
            </ul>
        `;
        educationalTips.appendChild(tipsSection);
    }

    // Add verification steps
    if (data.verification_suggestions && data.verification_suggestions.length > 0) {
        const verificationSection = document.createElement('div');
        verificationSection.className = 'detail-section';
        verificationSection.innerHTML = `
            <h4><i class="fas fa-tasks"></i> Verification Steps</h4>
            <ol class="verification-steps">
                ${data.verification_suggestions.map(step => `<li>${step.step || step}</li>`).join('')}
            </ol>
        `;
        educationalTips.appendChild(verificationSection);
    }

    // Add general resources
    const resourcesSection = document.createElement('div');
    resourcesSection.className = 'detail-section';
    resourcesSection.innerHTML = `
        <h4><i class="fas fa-external-link-alt"></i> Additional Resources</h4>
        <div class="resources-grid">
            <a href="https://www.snopes.com" target="_blank" class="resource-card">
                <i class="fas fa-check-circle"></i>
                <span>Snopes Fact Checking</span>
            </a>
            <a href="https://www.factcheck.org" target="_blank" class="resource-card">
                <i class="fas fa-shield-alt"></i>
                <span>FactCheck.org</span>
            </a>
            <a href="https://images.google.com" target="_blank" class="resource-card">
                <i class="fas fa-search"></i>
                <span>Google Image Search</span>
            </a>
            <a href="https://tineye.com" target="_blank" class="resource-card">
                <i class="fas fa-eye"></i>
                <span>TinEye Reverse Search</span>
            </a>
        </div>
    `;
    educationalTips.appendChild(resourcesSection);
}

function createDetailSection(title, items) {
    const section = document.createElement('div');
    section.className = 'detail-section';
    
    const titleElement = document.createElement('h4');
    titleElement.innerHTML = `<i class="fas fa-info-circle"></i> ${title}`;
    section.appendChild(titleElement);

    const list = document.createElement('div');
    list.className = 'detail-list';
    
    items.forEach(item => {
        const row = document.createElement('div');
        row.className = 'detail-row';
        row.innerHTML = `
            <span class="detail-label">${item.label}:</span>
            <span class="detail-value">${item.value}</span>
        `;
        list.appendChild(row);
    });
    
    section.appendChild(list);
    return section;
}

// UI State Management
function showLoading() {
    loadingOverlay.style.display = 'flex';
    
    // Disable all forms
    const forms = [textForm, urlForm, imageForm];
    forms.forEach(form => {
        const submitBtn = form.querySelector('.analyze-btn');
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
        }
    });
}

function hideLoading() {
    loadingOverlay.style.display = 'none';
    
    // Re-enable all forms
    const forms = [
        { form: textForm, text: '<i class="fas fa-search"></i> Analyze Text' },
        { form: urlForm, text: '<i class="fas fa-search"></i> Analyze URL' },
        { form: imageForm, text: '<i class="fas fa-search"></i> Analyze Image' }
    ];
    
    forms.forEach(({ form, text }) => {
        const submitBtn = form.querySelector('.analyze-btn');
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = text;
        }
    });
}

function showResults() {
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function hideResults() {
    resultsSection.style.display = 'none';
}

function closeResults() {
    hideResults();
}

function showError(message) {
    // Create error notification
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-notification';
    errorDiv.innerHTML = `
        <i class="fas fa-exclamation-circle"></i>
        <span>${message}</span>
        <button onclick="this.parentElement.remove()" class="close-error">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    // Add to page
    document.body.appendChild(errorDiv);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (errorDiv.parentElement) {
            errorDiv.remove();
        }
    }, 5000);
}

// Utility Functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Add error notification styles dynamically
const errorStyles = `
.error-notification {
    position: fixed;
    top: 20px;
    right: 20px;
    background: #dc3545;
    color: white;
    padding: 15px 20px;
    border-radius: 10px;
    box-shadow: 0 5px 15px rgba(220, 53, 69, 0.3);
    display: flex;
    align-items: center;
    gap: 10px;
    z-index: 10000;
    max-width: 400px;
    animation: slideInRight 0.3s ease-out;
}

.error-notification i {
    font-size: 1.2rem;
}

.close-error {
    background: none;
    border: none;
    color: white;
    cursor: pointer;
    padding: 5px;
    margin-left: auto;
}

@keyframes slideInRight {
    from {
        transform: translateX(100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}

.detail-section {
    margin-bottom: 25px;
    padding: 20px;
    background: #f8f9fa;
    border-radius: 10px;
    border-left: 4px solid #667eea;
}

.detail-section h4 {
    color: #333;
    margin-bottom: 15px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.detail-section h4 i {
    color: #667eea;
}

.detail-list {
    display: grid;
    gap: 10px;
}

.detail-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0;
    border-bottom: 1px solid #e9ecef;
}

.detail-row:last-child {
    border-bottom: none;
}

.detail-label {
    font-weight: 500;
    color: #495057;
}

.detail-value {
    color: #6c757d;
    text-align: right;
}

.ai-analysis {
    border-left-color: #28a745;
}

.ai-details p {
    margin-bottom: 10px;
    color: #555;
}

.tips-list {
    list-style: none;
    margin: 0;
    padding: 0;
}

.tips-list li {
    padding: 8px 0;
    border-bottom: 1px solid #e9ecef;
    color: #555;
    display: flex;
    align-items: flex-start;
    gap: 10px;
}

.tips-list li::before {
    content: "💡";
    flex-shrink: 0;
}

.tips-list li:last-child {
    border-bottom: none;
}

.resources-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
    margin-top: 15px;
}

.resource-card {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 12px;
    background: white;
    border: 1px solid #e9ecef;
    border-radius: 8px;
    text-decoration: none;
    color: #667eea;
    transition: all 0.3s ease;
}

.resource-card:hover {
    background: #f8f9ff;
    border-color: #667eea;
    transform: translateY(-2px);
}

.resource-card i {
    font-size: 1.2rem;
}
`;

// Add styles to document
const styleSheet = document.createElement('style');
styleSheet.textContent = errorStyles;
document.head.appendChild(styleSheet);
