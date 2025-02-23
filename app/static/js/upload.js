const API_BASE_URL = '/api/v1';

// File upload handling
const uploadBox = document.getElementById('uploadBox');
const fileInput = document.getElementById('fileInput');
const uploadStatus = document.getElementById('uploadStatus');

uploadBox.addEventListener('click', () => fileInput.click());

uploadBox.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadBox.classList.add('dragover');
});

uploadBox.addEventListener('dragleave', () => {
    uploadBox.classList.remove('dragover');
});

uploadBox.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadBox.classList.remove('dragover');
    const files = e.dataTransfer.files;
    handleFiles(files);
});

fileInput.addEventListener('change', (e) => {
    handleFiles(e.target.files);
});

async function handleFiles(files) {
    const file = files[0];
    if (!file) return;

    // Validate file type
    if (!file.name.toLowerCase().endsWith('.txt')) {
        uploadStatus.innerHTML = 'Please upload a .txt file';
        return;
    }

    // Validate file size
    if (file.size > 25 * 1024) { // 25KB
        uploadStatus.innerHTML = 'File size must be less than 25KB';
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    uploadStatus.innerHTML = 'Uploading...';

    try {
        const response = await fetch(`${API_BASE_URL}/documents/upload`, {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const data = await response.json();
            uploadStatus.innerHTML = `Success! Processed ${data.chunks_processed} chunks from ${data.filename}`;
        } else {
            throw new Error('Upload failed');
        }
    } catch (error) {
        console.error('Error:', error);
        uploadStatus.innerHTML = 'Failed to upload file';
    }
} 