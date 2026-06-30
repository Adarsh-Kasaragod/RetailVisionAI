document.addEventListener('DOMContentLoaded', () => {
    // Only run on the upload page
    if (!document.getElementById('drop-zone')) return;

    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const previewContainer = document.getElementById('preview-container');
    const imagePreview = document.getElementById('image-preview');
    const removeBtn = document.getElementById('remove-btn');
    const predictBtn = document.getElementById('predict-btn');
    const uploadCard = document.querySelector('.upload-card');
    const loadingState = document.getElementById('loading-state');
    const resultState = document.getElementById('result-state');
    const resetBtn = document.getElementById('reset-btn');
    
    let selectedFile = null;

    // Drag and drop events
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => dropZone.classList.add('dragover'), false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => dropZone.classList.remove('dragover'), false);
    });

    dropZone.addEventListener('drop', handleDrop, false);
    fileInput.addEventListener('change', handleFileSelect, false);
    removeBtn.addEventListener('click', clearFile);
    predictBtn.addEventListener('click', uploadAndPredict);
    resetBtn.addEventListener('click', resetUI);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles(files);
    }

    function handleFileSelect(e) {
        const files = e.target.files;
        handleFiles(files);
    }

    function handleFiles(files) {
        if (files.length > 0) {
            const file = files[0];
            // Validate file type
            if (!file.type.match('image.*')) {
                alert('Please select an image file (JPG, PNG, WEBP).');
                return;
            }
            selectedFile = file;
            showPreview(file);
        }
    }

    function showPreview(file) {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onloadend = function() {
            imagePreview.src = reader.result;
            previewContainer.classList.remove('hidden');
            predictBtn.disabled = false;
        }
    }

    function clearFile(e) {
        if(e) e.stopPropagation();
        selectedFile = null;
        fileInput.value = '';
        imagePreview.src = '';
        previewContainer.classList.add('hidden');
        predictBtn.disabled = true;
    }

    function resetUI() {
        clearFile();
        resultState.classList.add('hidden');
        uploadCard.classList.remove('hidden');
    }

    async function uploadAndPredict() {
        if (!selectedFile) return;

        // Update UI
        uploadCard.classList.add('hidden');
        loadingState.classList.remove('hidden');

        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            loadingState.classList.add('hidden');

            if (response.ok) {
                // Show results
                document.getElementById('result-class').textContent = data.prediction;
                document.getElementById('result-confidence').textContent = data.confidence + '%';
                
                // Animate progress bar
                setTimeout(() => {
                    document.getElementById('confidence-fill').style.width = data.confidence + '%';
                }, 100);

                resultState.classList.remove('hidden');
            } else {
                alert(data.error || 'An error occurred during prediction.');
                resetUI();
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Failed to connect to the server.');
            loadingState.classList.add('hidden');
            resetUI();
        }
    }
});
