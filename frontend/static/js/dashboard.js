/**
 * Dashboard JavaScript
 * SIH PS1 - Cybersecurity Threat Detector
 */

// Text Analysis
document.getElementById('textForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const text = document.getElementById('textInput').value.trim();
    if (!text) return alert('Please enter text to analyze');
    
    await analyzeContent('/api/analyze-text', { text }, 'textResults', 'textBtn');
});

// URL Analysis
document.getElementById('urlForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const url = document.getElementById('urlInput').value.trim();
    if (!url) return alert('Please enter URL to analyze');
    
    await analyzeContent('/api/analyze-url', { url }, 'urlResults', 'urlBtn');
});

async function analyzeContent(endpoint, data, resultsId, btnId) {
    const resultsDiv = document.getElementById(resultsId);
    const btn = document.getElementById(btnId);
    
    btn.disabled = true;
    btn.textContent = '🔄 Analyzing...';
    resultsDiv.style.display = 'none';

    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        displayResults(result, resultsDiv);
        
    } catch (error) {
        alert('Analysis failed: ' + error.message);
    } finally {
        btn.disabled = false;
        btn.textContent = btn.id === 'textBtn' ? '🔍 Analyze Text' : '🔍 Analyze URL';
    }
}

function displayResults(result, container) {
    const riskScore = Math.round(result.risk_score * 100);
    const headerClass = result.is_threat ? 'danger' : (riskScore > 30 ? 'warning' : 'safe');
    const headerText = result.is_threat ? '⚠️ THREAT DETECTED' : (riskScore > 30 ? '⚡ SUSPICIOUS' : '✅ SAFE');
    
    container.innerHTML = `
        <div class="result-header ${headerClass}">${headerText}</div>
        <div class="metrics">
            <div class="metric">
                <div class="metric-value">${riskScore}%</div>
                <div>Risk Score</div>
            </div>
            <div class="metric">
                <div class="metric-value">${result.risk_level}</div>
                <div>Risk Level</div>
            </div>
            <div class="metric">
                <div class="metric-value">${Math.round(result.confidence * 100)}%</div>
                <div>Confidence</div>
            </div>
            <div class="metric">
                <div class="metric-value">${result.analysis_time}</div>
                <div>Analyzed</div>
            </div>
        </div>
        <div>
            <strong>Detected Issues:</strong>
            <div class="keywords">
                ${(result.detected_keywords || result.detected_issues || []).map(item => 
                    `<span class="keyword">${item}</span>`
                ).join('')}
            </div>
        </div>
    `;
    
    container.style.display = 'block';
}
