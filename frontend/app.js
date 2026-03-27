const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const fileQueue = document.getElementById('file-queue');
const fileListContainer = document.getElementById('file-list-container');
const clearAllBtn = document.getElementById('clear-all');

const API_BASE = '/api';

// --- Event Listeners ---

dropZone.addEventListener('click', () => fileInput.click());

fileInput.addEventListener('change', (e) => {
    handleFiles(e.target.files);
});

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('active');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('active');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('active');
    handleFiles(e.dataTransfer.files);
});

clearAllBtn.addEventListener('click', () => {
    fileQueue.innerHTML = '';
    fileListContainer.classList.add('hidden');
});

// --- Core Logic ---

function handleFiles(files) {
    if (files.length === 0) return;
    
    fileListContainer.classList.remove('hidden');
    
    Array.from(files).forEach(file => {
        if (file.type !== 'application/pdf') {
            alert(`ไฟล์ ${file.name} ไม่ใช่ PDF`);
            return;
        }
        uploadFile(file);
    });
}

async function uploadFile(file) {
    const fileId = Math.random().toString(36).substring(7);
    const item = createFileItem(file.name, fileId);
    fileQueue.appendChild(item);

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch(`${API_BASE}/upload`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) throw new Error('Upload failed');
        
        const data = await response.json();
        const taskId = data.task_id;
        
        // Start polling for status
        pollStatus(taskId, item);
        
    } catch (err) {
        console.error(err);
        updateItemStatus(item, 'FAILED', 0, 'เกิดข้อผิดพลาดในการอัพโหลด');
    }
}

function pollStatus(taskId, item) {
    const interval = setInterval(async () => {
        try {
            const res = await fetch(`${API_BASE}/status/${taskId}`);
            const data = await res.json();

            if (data.status === 'SUCCESS') {
                clearInterval(interval);
                updateItemStatus(item, 'COMPLETED', 100);
                setupDownload(item, taskId);
            } else if (data.status === 'PROGRESS') {
                updateItemStatus(item, 'PROCESSING', data.progress);
            } else if (data.status === 'FAILURE') {
                clearInterval(interval);
                updateItemStatus(item, 'FAILED', 0, data.error);
            } else if (data.status === 'PENDING' || data.status === 'QUEUED') {
                updateItemStatus(item, 'QUEUED', 0);
            }
        } catch (err) {
            console.error('Polling error:', err);
        }
    }, 2000); // Poll every 2 seconds
}

// --- UI Helpers ---

function createFileItem(name, id) {
    const div = document.createElement('div');
    div.className = 'file-item';
    div.id = `item-${id}`;
    div.innerHTML = `
        <span class="f-icon">📄</span>
        <div class="f-info">
            <div class="f-name">${name}</div>
            <div class="progress-container">
                <div class="progress-bar"></div>
            </div>
        </div>
        <div class="status-box">
            <span class="status-badge status-queued">กำลังเข้าคิว</span>
        </div>
    `;
    return div;
}

function updateItemStatus(item, status, progress, errorMsg = '') {
    const bar = item.querySelector('.progress-bar');
    const badge = item.querySelector('.status-badge');
    
    bar.style.width = `${progress}%`;
    
    switch (status) {
        case 'QUEUED':
            badge.className = 'status-badge status-queued';
            badge.innerText = 'รอคิว...';
            break;
        case 'PROCESSING':
            badge.className = 'status-badge status-processing';
            badge.innerText = `กำลังแปลง ${progress}%`;
            break;
        case 'COMPLETED':
            badge.className = 'status-badge status-completed';
            badge.innerText = 'สำเร็จ! คลิกโหลด';
            bar.style.background = 'var(--success)';
            break;
        case 'FAILED':
            badge.className = 'status-badge status-failed';
            badge.innerText = 'ล้มเหลว';
            alert(`ข้อผิดพลาด (${item.querySelector('.f-name').innerText}): ${errorMsg}`);
            break;
    }
}

function setupDownload(item, taskId) {
    const badge = item.querySelector('.status-completed');
    badge.addEventListener('click', () => {
        window.location.href = `${API_BASE}/download/${taskId}`;
    });
    
    // Auto-trigger download
    setTimeout(() => {
        window.location.href = `${API_BASE}/download/${taskId}`;
    }, 500);
}
