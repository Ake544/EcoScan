const materialPrices = {
    'plastic': 30.00,
    'paper': 22.50,
    'cardboard': 15.00,
    'metal': 75.00,
    'glass': 8.00,
    'battery': 120.00,
    'biological': 8.00,
    'clothes': 45,
    'shoes': 38.00,
    'trash': 0.00,
    'brown-glass': 8.00,
    'green-glass': 8.00,
    'white-glass': 8.00
};

const recyclingTips = {
    'plastic': 'Rinse containers before recycling. Remove caps and labels if required.',
    'paper': 'Keep paper dry and clean. Remove any plastic windows from envelopes.',
    'cardboard': 'Flatten boxes to save space. Remove tape and shipping labels.',
    'metal': 'Rinse cans thoroughly. Separate aluminum and steel if required.',
    'glass': 'Rinse bottles and jars. Separate by color if your facility requires it.',
    'battery': 'Do not dispose in regular trash. Take to designated battery recycling points.',
    'biological': 'Compost if possible. Check local guidelines for food waste disposal.',
    'clothes': 'Donate if in good condition. Otherwise, recycle as textile waste.',
    'shoes': 'Donate wearable pairs. Recycle unwearable shoes as textile waste.',
    'trash': 'Dispose in regular waste bin. Consider if any parts can be recycled separately.',
    'brown-glass': 'Rinse thoroughly. Brown glass is often used for beer bottles.',
    'green-glass': 'Rinse thoroughly. Green glass is commonly used for wine bottles.',
    'white-glass': 'Rinse thoroughly. Clear glass has the highest recycling value.'
};

const fileInput = document.getElementById('file-input');
const dropArea = document.getElementById('drop-area');
const scanButton = document.getElementById('scan-button');
const imagePreview = document.getElementById('image-preview');
const imagePreviewContainer = document.getElementById('image-preview-container');
const loadingElement = document.getElementById('loading');
const errorElement = document.getElementById('error-message');
const resultImage = document.getElementById('result-image');
const predictedMaterial = document.getElementById('predicted-material');
const confidenceValue = document.getElementById('confidence-value');
const confidenceBar = document.getElementById('confidence-bar');
const estimatedValue = document.getElementById('estimated-value');
const recyclingTip = document.getElementById('recycling-tip');
const weightInput = document.getElementById('weight');

fileInput.addEventListener('change', handleFileSelect);
dropArea.addEventListener('dragover', handleDragOver);
dropArea.addEventListener('drop', handleDrop);
scanButton.addEventListener('click', analyzeImage);

fileInput.addEventListener('change', function() {
    scanButton.disabled = !this.files.length;
});

function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    dropArea.classList.add('border-primary');
}

function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    dropArea.classList.remove('border-primary');
    
    const files = e.dataTransfer.files;
    if (files.length) {
    fileInput.files = files;
    handleFileSelect();
    scanButton.disabled = false;
    }
}

function handleFileSelect() {
    errorElement.classList.add('hidden');
    
    if (fileInput.files && fileInput.files[0]) {
    const file = fileInput.files[0];
    
    if (!file.type.match('image.*')) {
        showError('Please select an image file (JPEG, PNG, etc.)');
        return;
    }
    
    const reader = new FileReader();
    reader.onload = function(e) {
        imagePreview.src = e.target.result;
        resultImage.src = e.target.result;
        imagePreviewContainer.classList.remove('hidden');
    };
    reader.readAsDataURL(file);
    }
}

async function analyzeImage() {
    const API_URL = 'https://ecoscan-backend.onrender.com';
    if (!fileInput.files.length) return;
    
    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('file', file);
    
    loadingElement.classList.remove('hidden');
    scanButton.disabled = true;
    errorElement.classList.add('hidden');
    
    try {
    const response = await fetch(`${API_URL}/predict`, {
        method: 'POST',
        body: formData
    });
    
    if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
    }
    
    const result = await response.json();
    displayResults(result);
    
    } catch (error) {
    showError(error.message || 'Failed to analyze image. Please try again.');
    } finally {
    loadingElement.classList.add('hidden');
    scanButton.disabled = false;
    }
}

function displayResults(result) {
    if (result.status !== 'success') {
    showError(result.message || 'Analysis failed');
    return;
    }
    
    predictedMaterial.textContent = result.prediction;
    
    const confidencePercent = Math.round(result.confidence * 100);
    confidenceValue.textContent = `${confidencePercent}%`;
    confidenceBar.style.width = `${confidencePercent}%`;
    
    const weight = parseFloat(weightInput.value) || 1;
    const pricePerKg = materialPrices[result.prediction.toLowerCase()] || 0;
    const value = (weight * pricePerKg).toFixed(2);
    estimatedValue.textContent = `${value} Birr`;
    
    recyclingTip.textContent = recyclingTips[result.prediction.toLowerCase()] || 
                            'Ensure the material is clean and free of contaminants for recycling.';
}

function showError(message) {
    errorElement.textContent = message;
    errorElement.classList.remove('hidden');
}

document.getElementById('mobile-menu-button').addEventListener('click', function() {
    alert('Mobile menu would open here');
});

weightInput.addEventListener('input', function() {
    if (predictedMaterial.textContent !== 'Select an image') {
    const weight = parseFloat(this.value) || 1;
    const material = predictedMaterial.textContent.toLowerCase();
    const pricePerKg = materialPrices[material] || 0;
    const value = (weight * pricePerKg).toFixed(2);
    estimatedValue.textContent = `${value} Birr`;
    }
});