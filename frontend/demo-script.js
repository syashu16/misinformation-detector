// Demo functionality for hackathon presentation

const DEMO_EXAMPLES = {
    covid_myth: {
        text: "URGENT: Govt doctors don't want you to know! Drinking hot water with turmeric and cow urine 3 times daily COMPLETELY prevents COVID-19! Big pharma hiding this truth! Share with 10 friends immediately for protection! 🙏",
        expected_risk: 85,
        category: "Health Misinformation"
    },
    whatsapp_forward: {
        text: "Good morning! 🌅 Reliance Jio is giving FREE 1TB data to first 1000 people who forward this message to 20 contacts. Offer valid till tonight only! Don't miss this golden opportunity! Forward now! 📱💯",
        expected_risk: 90,
        category: "WhatsApp Scam"
    },
    political_deepfake: {
        text: "LEAKED VIDEO: Opposition leader caught taking Rs 500 crore bribe! Media hiding this scandal! Watch before it gets deleted! Share everywhere! This will change election results! 🔥🔥",
        expected_risk: 95,
        category: "Political Misinformation"
    },
    financial_scam: {
        text: "🎉 CONGRATULATIONS! You have won Rs 25 LAKH in Modi Government's Digital India Lottery! Claim your prize by clicking this link and providing Aadhaar details. Limited time offer! 💰",
        expected_risk: 100,
        category: "Financial Fraud"
    },
    reliable_content: {
        text: "According to a peer-reviewed study published in The Lancet by researchers at AIIMS Delhi, the new COVID-19 variant shows 15% increased transmissibility. The study, conducted over 6 months with 10,000 participants, suggests continued mask usage in crowded areas. Full paper available at doi.org/example",
        expected_risk: 10,
        category: "Credible Information"
    }
};

// Demo testing function
function testDemo(exampleType) {
    if (exampleType === 'custom') {
        // Switch to text analysis tab for custom input
        switchTab('text');
        return;
    }
    
    const example = DEMO_EXAMPLES[exampleType];
    if (!example) return;
    
    // Switch to text analysis tab
    switchTab('text');
    
    // Fill the textarea with demo content
    const textInput = document.getElementById('text-input');
    if (textInput) {
        textInput.value = example.text;
        updateCharCount();
        
        // Add visual indicator that this is a demo
        textInput.style.border = '2px solid #667eea';
        textInput.style.backgroundColor = '#f8f9ff';
        
        // Automatically analyze after a short delay
        setTimeout(() => {
            const textForm = document.getElementById('text-form');
            if (textForm) {
                // Trigger analysis
                handleTextAnalysis({ preventDefault: () => {} });
            }
        }, 500);
    }
    
    // Show notification about demo
    showDemoNotification(example.category, example.expected_risk);
}

function showDemoNotification(category, expectedRisk) {
    const notification = document.createElement('div');
    notification.className = 'demo-notification';
    notification.innerHTML = `
        <i class="fas fa-flask"></i>
        <span>Demo: ${category} (Expected Risk: ${expectedRisk}%)</span>
        <button onclick="this.parentElement.remove()" class="close-demo-notification">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

// Add demo button to navigation
function addDemoButton() {
    const navTabs = document.querySelector('.nav-tabs');
    if (navTabs) {
        const demoBtn = document.createElement('button');
        demoBtn.className = 'tab-btn demo-btn';
        demoBtn.innerHTML = '<i class="fas fa-rocket"></i> Live Demo';
        demoBtn.onclick = () => toggleDemoSection();
        navTabs.appendChild(demoBtn);
    }
}

function toggleDemoSection() {
    const demoSection = document.getElementById('demo-section');
    const mainContent = document.querySelector('.main-content');
    
    if (demoSection && mainContent) {
        if (demoSection.style.display === 'none') {
            demoSection.style.display = 'block';
            mainContent.style.display = 'none';
            
            // Animate metrics
            animateMetrics();
            
            // Update tab active state
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            document.querySelector('.demo-btn').classList.add('active');
        } else {
            demoSection.style.display = 'none';
            mainContent.style.display = 'block';
        }
    }
}

function animateMetrics() {
    // Animate the accuracy metric
    animateNumber('accuracy-metric', 0, 94, 2000);
    setTimeout(() => animateNumber('patterns-metric', 0, 500, 1500), 500);
    setTimeout(() => animateNumber('languages-metric', 0, 3, 1000), 1000);
}

function animateNumber(elementId, start, end, duration) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    const startTime = performance.now();
    const suffix = element.textContent.includes('%') ? '%' : 
                  element.textContent.includes('+') ? '+' : 
                  element.textContent.includes('<') ? 's' : '';
    
    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        const current = Math.floor(start + (end - start) * progress);
        element.textContent = current + suffix;
        
        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }
    
    requestAnimationFrame(update);
}

// Enhanced results display with Indian context
function displayResultsWithIndianContext(data) {
    // Call the original display function
    displayResults(data);
    
    // Add Indian context if available
    if (data.indian_context) {
        const resultsCard = document.querySelector('.results-card');
        if (resultsCard) {
            const indianContextDiv = document.createElement('div');
            indianContextDiv.className = 'indian-context-results';
            indianContextDiv.innerHTML = `
                <h4><i class="fas fa-flag"></i> Indian Context Analysis</h4>
                <div class="indian-risk-score">
                    Regional Risk Score: ${data.indian_context.india_specific_risk}/100
                </div>
                <div class="regional-patterns">
                    ${data.indian_context.regional_patterns.map(pattern => 
                        `<div class="regional-pattern-item">${pattern}</div>`
                    ).join('')}
                </div>
            `;
            
            resultsCard.appendChild(indianContextDiv);
        }
    }
}

// Initialize demo features when page loads
document.addEventListener('DOMContentLoaded', function() {
    // Add demo button after other initialization
    setTimeout(() => {
        addDemoButton();
    }, 100);
});

// Demo notification styles
const demoStyles = `
.demo-notification {
    position: fixed;
    top: 80px;
    right: 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 15px 20px;
    border-radius: 10px;
    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    display: flex;
    align-items: center;
    gap: 10px;
    z-index: 10000;
    max-width: 350px;
    animation: slideInRight 0.3s ease-out;
}

.demo-notification i:first-child {
    font-size: 1.2rem;
    color: #ffd700;
}

.close-demo-notification {
    background: none;
    border: none;
    color: white;
    cursor: pointer;
    padding: 5px;
    margin-left: auto;
    opacity: 0.8;
}

.close-demo-notification:hover {
    opacity: 1;
}

.demo-btn {
    background: linear-gradient(135deg, #28a745 0%, #20c997 100%) !important;
    color: white !important;
}

.demo-btn:hover {
    background: linear-gradient(135deg, #218838 0%, #1abc9c 100%) !important;
}

.indian-context-results {
    margin-top: 20px;
    padding: 20px;
    background: linear-gradient(135deg, #fff8e1 0%, #f3e5f5 100%);
    border-radius: 10px;
    border-left: 4px solid #ff9933;
}

.indian-risk-score {
    font-size: 1.1rem;
    font-weight: bold;
    color: #d84315;
    margin: 10px 0;
}

.regional-pattern-item {
    background: rgba(255, 152, 0, 0.1);
    padding: 8px 12px;
    margin: 5px 0;
    border-radius: 5px;
    border-left: 3px solid #ff9800;
    font-size: 0.9rem;
}
`;

// Add demo styles to document
const demoStyleSheet = document.createElement('style');
demoStyleSheet.textContent = demoStyles;
document.head.appendChild(demoStyleSheet);
