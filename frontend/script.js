/**
 * TrustEye Frontend JavaScript
 * SIH PS1 - Cybersecurity Threat Detector
 */

// API Configuration
const API_BASE = 'http://localhost:5000/api';

// Example data
const examples = {
    'phishing': {
        text: 'URGENT SECURITY ALERT! Your account will be suspended in 24 hours due to suspicious activity. Click here immediately to verify your identity and avoid account closure.',
        url: 'http://secure-bank-verify.fake-domain.com/urgent-login'
    },
    'suspicious-url': {
        text: '',
        url: 'http://192.168.1.100/urgent-verify/login.php'
    },
    'safe': {
        text: 'Thank you for your recent purchase from Amazon. Your order has been shipped and will arrive within 2-3 business days. Track your package in your account.',
        url: 'https://amazon.com/your-orders'
    }
};

// DOM Elements
const scanForm = document.getElementById('scanForm');
const textInput = document.getElementById('textInput');
const urlInput = document.getElementById('urlInput');
const scanBtn = document.getElementById('scanBtn');
const results = document.getElementById('results');

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    setupEventListeners();
    checkAPIHealth();
});

function setupEventListeners() {
    // Form submission
    scanForm.addEventListener('submit', handleScan);
    
    // Input validation
    textInput.addEventListener('input', validateInputs);
    urlInput.addEventListener('input', validateInputs);
    
    // Smooth scrolling for navigation
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

function validateInputs() {
    const hasText = textInput.value.trim().length > 0;
    const hasUrl = urlInput.value.trim().length > 0;
    
    scanBtn.disabled = !hasText && !hasUrl;
}

async function handleScan(e) {
    e.preventDefault();
    
    const text = textInput.value.trim();
    const url = urlInput.value.trim();
    
    if (!text && !url) {
        showNotification('Please enter text or URL to analyze', 'warning');
        return;
    }
    
    // Show loading state
    setLoadingState(true);
    
    try {
        const startTime = Date.now();
        
        const response = await fetch(`${API_BASE}/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text, url })
        });
        
        const endTime = Date.now();
        const analysisTime = ((endTime - startTime) / 1000).toFixed(1);
        
        if (!response.ok) {
            throw new Error(`Analysis failed: ${response.status}`);
        }
        
        const result = await response.json();
        displayResults(result, analysisTime);
        
    } catch (error) {
        console.error('Scan error:', error);
        showNotification('Analysis failed. Please try again.', 'error');
    } finally {
        setLoadingState(false);
    }
}

function setLoadingState(loading) {
    const btnIcon = scanBtn.querySelector('.btn-icon');
    const btnText = scanBtn.querySelector('.btn-text');
    
    if (loading) {
        scanBtn.disabled = true;
        btnIcon.textContent = '⏳';
        btnText.textContent = 'Analyzing...';
        scanBtn.style.transform = 'none';
    } else {
        scanBtn.disabled = false;
        btnIcon.textContent = '🔍';
        btnText.textContent = 'Scan with TrustEye';
    }
}

function displayResults(result, analysisTime) {
    // Show results section
    results.classList.remove('hidden');
    
    // Update title and badge
    const resultsTitle = document.getElementById('resultsTitle');
    const riskBadge = document.getElementById('riskBadge');
    
    if (result.is_threat) {
        resultsTitle.textContent = '⚠️ Threat Detected';
        riskBadge.textContent = result.risk_level;
        riskBadge.className = `risk-badge ${result.risk_level.toLowerCase()}`;
    } else {
        resultsTitle.textContent = '✅ Appears Safe';
        riskBadge.textContent = result.risk_level;
        riskBadge.className = `risk-badge ${result.risk_level.toLowerCase()}`;
    }
    
    // Update risk score circle
    updateRiskScore(result.combined_score);
    
    // Update score details
    document.getElementById('riskLevel').textContent = result.risk_level;
    document.getElementById('confidence').textContent = `${Math.round(result.confidence * 100)}%`;
    document.getElementById('analysisTime').textContent = `${analysisTime}s`;
    
    // Update threat indicators
    updateThreatIndicators(result.threat_indicators);
    
    // Update explanation
    updateExplanation(result);
    
    // Scroll to results
    results.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function updateRiskScore(score) {
    const scoreValue = document.getElementById('scoreValue');
    const scoreCircle = document.querySelector('.score-circle');
    
    const percentage = Math.round(score * 100);
    scoreValue.textContent = `${percentage}%`;
    
    // Update circle gradient
    const degrees = (score * 360);
    let color = '#10b981'; // Green for low risk
    
    if (score >= 0.7) color = '#ef4444'; // Red for high risk
    else if (score >= 0.4) color = '#f59e0b'; // Yellow for medium risk
    
    scoreCircle.style.background = `conic-gradient(${color} ${degrees}deg, #e2e8f0 ${degrees}deg)`;
}

function updateThreatIndicators(indicators) {
    const indicatorsList = document.getElementById('indicatorsList');
    const threatIndicators = document.getElementById('threatIndicators');
    
    if (!indicators || indicators.length === 0) {
        threatIndicators.style.display = 'none';
        return;
    }
    
    threatIndicators.style.display = 'block';
    indicatorsList.innerHTML = indicators
        .slice(0, 5) // Show max 5 indicators
        .map(indicator => `<span class="indicator-tag">${indicator}</span>`)
        .join('');
}

function updateExplanation(result) {
    const explanationText = document.getElementById('explanationText');
    
    let explanation = '';
    
    if (result.is_threat) {
        explanation = `This content shows signs of phishing with a risk score of ${Math.round(result.combined_score * 100)}%. `;
        
        if (result.text_score > 0.5) {
            explanation += 'The text contains suspicious language patterns commonly used in phishing attacks. ';
        }
        
        if (result.url_score > 0.3) {
            explanation += 'The URL exhibits characteristics associated with malicious websites. ';
        }
        
        explanation += 'Exercise extreme caution and verify through official channels before taking any action.';
    } else {
        explanation = `This content appears to be legitimate with a low risk score of ${Math.round(result.combined_score * 100)}%. `;
        explanation += 'No significant phishing indicators were detected, but always remain vigilant when sharing personal information online.';
    }
    
    explanationText.textContent = explanation;
}

function loadExample(type) {
    const example = examples[type];
    if (example) {
        textInput.value = example.text;
        urlInput.value = example.url;
        validateInputs();
        
        // Scroll to form
        scanForm.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
}

function clearResults() {
    results.classList.add('hidden');
}

function scanAnother() {
    textInput.value = '';
    urlInput.value = '';
    clearResults();
    validateInputs();
    textInput.focus();
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    // Style notification
    Object.assign(notification.style, {
        position: 'fixed',
        top: '20px',
        right: '20px',
        padding: '1rem 1.5rem',
        borderRadius: '8px',
        color: 'white',
        fontWeight: '500',
        zIndex: '1000',
        transform: 'translateX(100%)',
        transition: 'transform 0.3s ease'
    });
    
    // Set background color based on type
    const colors = {
        info: '#2563eb',
        warning: '#f59e0b',
        error: '#ef4444',
        success: '#10b981'
    };
    notification.style.background = colors[type] || colors.info;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

async function checkAPIHealth() {
    try {
        const response = await fetch(`${API_BASE}/health`);
        if (response.ok) {
            console.log('✅ TrustEye API is healthy');
        } else {
            console.warn('⚠️ TrustEye API health check failed');
        }
    } catch (error) {
        console.warn('⚠️ TrustEye API is not accessible:', error.message);
        showNotification('API connection issue. Some features may not work.', 'warning');
    }
}

// Export functions for global access
window.loadExample = loadExample;
window.clearResults = clearResults;
window.scanAnother = scanAnother;
