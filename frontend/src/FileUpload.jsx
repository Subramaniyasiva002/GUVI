import { useState } from 'react';

const FileUpload = ({ onUploadSuccess }) => {
    const [file, setFile] = useState(null);
    const [status, setStatus] = useState('');
    const [uploading, setUploading] = useState(false);

    const handleFileChange = (e) => {
        if (e.target.files) {
            setFile(e.target.files[0]);
        }
    };

    const handleUpload = async () => {
        if (!file) return;

        setUploading(true);
        setStatus('Uploading...');

        const formData = new FormData();
        formData.append('file', file);

        try {
            const apiBase = import.meta.env.VITE_API_URL || "http://localhost:8000";
            const response = await fetch(`${apiBase}/upload`, {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error('Upload failed');
            }

            const result = await response.json();

            if (result.duplicate && result.assessment) {
                // File was duplicate and assessment exists - show it immediately
                setStatus(`✅ ${result.message} Analysis loaded automatically!`);
            } else if (result.duplicate) {
                // File was duplicate but no assessment yet
                setStatus(`ℹ️ ${result.message}`);
            } else {
                // New file uploaded
                setStatus(`✅ Success: ${result.message}`);
            }

            if (onUploadSuccess) onUploadSuccess(result);
        } catch (error) {
            setStatus(`❌ Error: ${error.message}`);
        } finally {
            setUploading(false);
        }
    };

    return (
        <div className="file-upload">
            <input type="file" accept=".csv,.xlsx" onChange={handleFileChange} />
            <button onClick={handleUpload} disabled={!file || uploading}>
                {uploading ? 'Uploading...' : 'Upload Data'}
            </button>
            {status && <p className="status-message">{status}</p>}
        </div>
    );
};

export default FileUpload;
