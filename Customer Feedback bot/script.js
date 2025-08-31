// DOM elements
const feedbackText = document.getElementById('feedback-text');
const analyzeBtn = document.getElementById('analyze-btn');
const clearBtn = document.getElementById('clear-btn');
const resultsSection = document.getElementById('results-section');
const loadingSection = document.getElementById('loading-section');
const errorSection = document.getElementById('error-section');
const exampleBtns = document.querySelectorAll('.example-btn');

// Result elements
const sentimentIcon = document.getElementById('sentiment-icon');
const sentimentLabel = document.getElementById('sentiment-label');
const sentimentDescription = document.getElementById('sentiment-description');
const confidencePercentage = document.getElementById('confidence-percentage');
const confidenceFill = document.getElementById('confidence-fill');
const analyzedText = document.getElementById('analyzed-text');
const errorMessage = document.getElementById('error-message');

// API endpoint - you'll need to update this to match your backend
const API_ENDPOINT = 'http://localhost:5000/analyze'; // Update this URL

// Event listeners
analyzeBtn.addEventListener('click', analyzeSentiment);
clearBtn.addEventListener('click', clearForm);
feedbackText.addEventListener('keydown', handleEnterKey);

// Example button listeners
exampleBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const text = btn.getAttribute('data-text');
        feedbackText.value = text;
        analyzeSentiment();
    });
});

// Handle Enter key in textarea
function handleEnterKey(e) {
    if (e.key === 'Enter' && e.ctrlKey) {
        analyzeSentiment();
    }
}

// Main analysis function
async function analyzeSentiment() {
    const text = feedbackText.value.trim();
    
    if (!text) {
        showError('Please enter some feedback text to analyze.');
        return;
    }
    
    // Show loading state
    showLoading();
    
    try {
        // Prepare the request payload
        const payload = {
            text: text
        };
        
        // Make API call
        const response = await fetch(API_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Display results
        displayResults(data);
        
    } catch (error) {
        console.error('Error analyzing sentiment:', error);
        showError('Failed to analyze sentiment. Please check your connection and try again.');
    }
}

// Display results
function displayResults(data) {
    // Hide loading and error sections
    hideLoading();
    hideError();
    
    // Update UI with results
    const prediction = data.prediction;
    const confidence = data.confidence;
    const text = data.text;
    
    // Update sentiment icon and label
    updateSentimentDisplay(prediction);
    
    // Update confidence
    const confidencePercent = Math.round(confidence * 100);
    confidencePercentage.textContent = `${confidencePercent}%`;
    confidenceFill.style.width = `${confidencePercent}%`;
    
    // Update analyzed text
    analyzedText.textContent = text;
    
    // Show results section
    resultsSection.style.display = 'block';
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Update sentiment display based on prediction
function updateSentimentDisplay(prediction) {
    const icon = sentimentIcon.querySelector('i');
    
    // Remove existing classes
    sentimentIcon.className = 'sentiment-icon';
    
    // Update based on prediction (adjust these based on your model's labels)
    if (prediction.toLowerCase().includes('positive') || prediction.toLowerCase().includes('pos')) {
        sentimentIcon.classList.add('positive');
        icon.className = 'fas fa-smile';
        sentimentLabel.textContent = 'Positive';
        sentimentDescription.textContent = 'The feedback expresses positive sentiment';
    } else if (prediction.toLowerCase().includes('negative') || prediction.toLowerCase().includes('neg')) {
        sentimentIcon.classList.add('negative');
        icon.className = 'fas fa-frown';
        sentimentLabel.textContent = 'Negative';
        sentimentDescription.textContent = 'The feedback expresses negative sentiment';
    } else {
        sentimentIcon.classList.add('neutral');
        icon.className = 'fas fa-meh';
        sentimentLabel.textContent = 'Neutral';
        sentimentDescription.textContent = 'The feedback expresses neutral sentiment';
    }
}

// Clear form
function clearForm() {
    feedbackText.value = '';
    hideResults();
    hideError();
    feedbackText.focus();
}

// Show loading state
function showLoading() {
    loadingSection.style.display = 'block';
    resultsSection.style.display = 'none';
    errorSection.style.display = 'none';
    analyzeBtn.disabled = true;
    analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
}

// Hide loading state
function hideLoading() {
    loadingSection.style.display = 'none';
    analyzeBtn.disabled = false;
    analyzeBtn.innerHTML = '<i class="fas fa-search"></i> Analyze Sentiment';
}

// Show error
function showError(message) {
    hideLoading();
    hideResults();
    errorMessage.textContent = message;
    errorSection.style.display = 'block';
}

// Hide error
function hideError() {
    errorSection.style.display = 'none';
}

// Hide results
function hideResults() {
    resultsSection.style.display = 'none';
}

// Mock API function for testing (remove this when you have a real backend)
async function mockAnalyzeSentiment(text) {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // Mock response based on text content
    const positiveWords = ['good', 'great', 'excellent', 'amazing', 'love', 'perfect', 'wonderful', 'fantastic'];
    const negativeWords = ['bad', 'terrible', 'awful', 'hate', 'disappointed', 'worst', 'horrible', 'useless'];
    
    const lowerText = text.toLowerCase();
    let prediction = 'neutral';
    let confidence = 0.6;
    
    const positiveCount = positiveWords.filter(word => lowerText.includes(word)).length;
    const negativeCount = negativeWords.filter(word => lowerText.includes(word)).length;
    
    if (positiveCount > negativeCount) {
        prediction = 'positive';
        confidence = 0.7 + (positiveCount * 0.1);
    } else if (negativeCount > positiveCount) {
        prediction = 'negative';
        confidence = 0.7 + (negativeCount * 0.1);
    }
    
    return {
        text: text,
        prediction: prediction,
        confidence: Math.min(confidence, 0.95)
    };
}

// Uncomment the line below to use mock API for testing
// window.mockAnalyzeSentiment = mockAnalyzeSentiment;

// Add some helpful keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + Enter to analyze
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        analyzeSentiment();
    }
    
    // Escape to clear
    if (e.key === 'Escape') {
        clearForm();
    }
});

// Add some visual feedback for the textarea
feedbackText.addEventListener('input', () => {
    if (feedbackText.value.trim()) {
        analyzeBtn.classList.add('active');
    } else {
        analyzeBtn.classList.remove('active');
    }
});

// Initialize the page
document.addEventListener('DOMContentLoaded', () => {
    // Focus on the textarea
    feedbackText.focus();
    
    // Add some helpful instructions
    console.log('💡 Tips:');
    console.log('- Press Ctrl+Enter to analyze');
    console.log('- Press Escape to clear');
    console.log('- Try the example buttons below');
});
