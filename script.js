// Initialize event listeners
function initializeEventListeners() {
    const form = document.getElementById('soilForm');
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        processSoilData();
    });
}

async function processSoilData() {
    const soilData = getSoilData();
    
    try {
        // Show loading state
        showLoading();
        
        // Call Python prediction API
        const response = await fetch('http://localhost:5000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                    ph: soilData.ph,
                    soilType: soilData.soilType,
                    moisture: soilData.moisture
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            displayResults(result.recommendations, result.soil_analysis, result.model_info);
            scrollToResults();
        } else {
            showError('Failed to get predictions: ' + result.error);
        }
    } catch (error) {
        showError('Error connecting to prediction server: ' + error.message);
    } finally {
        hideLoading();
    }
}

function getSoilData() {
    return {
        ph: parseFloat(document.getElementById('ph').value) || 6.5,
        soilType: document.getElementById('soilType').value || 'Loamy',
        moisture: document.getElementById('moisture').value || 'Moist'
    };
}

function showLoading() {
    const button = document.querySelector('button[type="submit"]');
    button.disabled = true;
    button.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Analyzing...';
}

function hideLoading() {
    const button = document.querySelector('button[type="submit"]');
    button.disabled = false;
    // button.innerHTML = '<i class="fas fa-search mr-2"></i>Get Crop Recommendations';
    button.innerHTML = '<i class="fas fa-search"></i> Get Crop Suggestions';

}

function displayResults(recommendations, soilAnalysis, modelInfo) {
    const resultsSection = document.getElementById('results');
    const soilAnalysisDiv = document.getElementById('soil-analysis');
    const cropRecommendationsDiv = document.getElementById('crop-suggestions');

    soilAnalysisDiv.innerHTML = `
        <h3 class="analysis-title">
            <i class="fas fa-microscope"></i>
            Your Soil Analysis
        </h3>
        <div class="analysis-grid">
            <div class="analysis-card">
                <h4>Input Properties</h4>
                <div class="property-list">
                    <div class="property-item">
                        <span class="property-label">pH:</span>
                        <span class="property-value">${soilAnalysis.ph}</span>
                    </div>
                    <div class="property-item">
                        <span class="property-label">Soil Type:</span>
                        <span class="property-value">${soilAnalysis.soil_type}</span>
                    </div>
                    <div class="property-item">
                        <span class="property-label">Moisture:</span>
                        <span class="property-value">${soilAnalysis.moisture !== undefined && soilAnalysis.moisture !== null ? soilAnalysis.moisture : 'N/A'}</span>
                    </div>
                </div>
            </div>
            <div class="analysis-card">
                <h4>Predicted Nutrients</h4>
                <div class="nutrient-list">
                    <div class="nutrient-item">
                        <div class="nutrient-header">
                            <span>Nitrogen</span>
                            <span>${soilAnalysis.nitrogen} kg/ha</span>
                        </div>
                        <div class="nutrient-bar">
                            <div class="nutrient-fill nitrogen-fill" style="width: ${Math.min(100, (soilAnalysis.nitrogen/200)*100)}%"></div>
                        </div>
                    </div>
                    <div class="nutrient-item">
                        <div class="nutrient-header">
                            <span>Phosphorus</span>
                            <span>${soilAnalysis.phosphorus} kg/ha</span>
                        </div>
                        <div class="nutrient-bar">
                            <div class="nutrient-fill phosphorus-fill" style="width: ${Math.min(100, (soilAnalysis.phosphorus/100)*100)}%"></div>
                        </div>
                    </div>
                    <div class="nutrient-item">
                        <div class="nutrient-header">
                            <span>Potassium</span>
                            <span>${soilAnalysis.potassium} kg/ha</span>
                        </div>
                        <div class="nutrient-bar">
                            <div class="nutrient-fill potassium-fill" style="width: ${Math.min(100, (soilAnalysis.potassium/200)*100)}%"></div>
                        </div>
                    </div>
                </div>
                ${soilAnalysis.recommended_fertilizer ? `
                    <div class="ml-info">
                        <h4>
                            <i class="fas fa-flask"></i>
                            Recommended Fertilizer
                        </h4>
                        <p>${soilAnalysis.recommended_fertilizer}</p>
                    </div>
                ` : ''}
            </div>
        </div>
        <div class="ml-info">
            <h4>
                <i class="fas fa-brain"></i>
                Prediction Algorithm
            </h4>
            <p>
                <strong>Model:</strong> ${modelInfo.type}<br>
                <strong>Accuracy:</strong> ${modelInfo.accuracy}<br>
                <strong>Training Data:</strong> ${modelInfo.training_data}
            </p>
        </div>
    `;

    // Display crop recommendations
    if (recommendations.length === 0) {
        cropRecommendationsDiv.innerHTML = `
            <div class="no-results">
                <i class="fas fa-exclamation-triangle"></i>
                <h3>No suitable crops found</h3>
                <p>Try adjusting your soil parameters.</p>
            </div>
        `;
    } else {
        cropRecommendationsDiv.innerHTML = recommendations.map((crop, index) => {
            const confidenceClass = crop.confidence >= 80 ? 'confidence-high' : 
                                   crop.confidence >= 60 ? 'confidence-medium' : 'confidence-low';
            
            return `
                <div class="crop-card ${index === 0 ? 'best-match' : ''}">
                    ${index === 0 ? '<div class="best-match-badge">Best Match</div>' : ''}
                    <div class="crop-header">
                        <span class="crop-icon">${crop.icon}</span>
                        <div class="crop-info">
                            <h3>${crop.name}</h3>
                            <p>${crop.description}</p>
                        </div>
                    </div>
                    
                    <div class="confidence-score">
                        <div class="confidence-label">
                            <span>Confidence Score</span>
                            <span class="confidence-value">${crop.confidence}%</span>
                        </div>
                        <div class="confidence-bar">
                            <div class="confidence-fill ${confidenceClass}" style="width: ${crop.confidence}%"></div>
                        </div>
                    </div>

                    <div class="crop-details">
                        <div class="detail-row">
                            <span class="detail-label">Season:</span>
                            <span class="detail-value">${crop.growing_season}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Expected Yield:</span>
                            <span class="detail-value">${crop.yield_info}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Market Value:</span>
                            <span class="detail-value">${crop.market_value}</span>
                        </div>
                    </div>

                    <div class="ml-info">
                        <h4>
                            <i class="fas fa-robot"></i>
                            Prediction Details
                        </h4>
                        <p>
                            ${crop.reason || (`Algorithm predicts ${crop.confidence}% suitability based on pH and soil type compatibility.`)}
                        </p>
                    </div>
                </div>
            `;
        }).join('');
    }

resultsSection.style.display = 'block';
resultsSection.classList.add('fade-in');

}

function scrollToResults() {
    const resultsSection = document.getElementById('results');
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'fixed top-4 right-4 bg-red-500 text-white px-6 py-3 rounded-lg shadow-lg z-50 fade-in';
    errorDiv.innerHTML = `
        <div class="flex items-center">
            <i class="fas fa-exclamation-circle mr-2"></i>
            <span>${message}</span>
        </div>
    `;
    
    document.body.appendChild(errorDiv);
    
    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}

// Initialize when DOM loaded
document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
});
