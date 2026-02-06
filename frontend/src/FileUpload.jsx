import { useState } from 'react';

const TRANSLATIONS = {
    en: { uploadSection: "Upload Financial Documents" },
    hi: { uploadSection: "वित्तीय दस्तावेज़ अपलोड करें" },
    ta: { uploadSection: "நிதி ஆவணங்களை பதிவேற்றவும்" }
};

const FileUpload = ({ onUploadSuccess, language = 'en' }) => {
    const t = TRANSLATIONS[language] || TRANSLATIONS.en;
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

    const resetDatabase = async () => {
        if (!window.confirm("This will delete ALL data. Are you sure?")) return;

        try {
            const apiBase = import.meta.env.VITE_API_URL || "http://localhost:8000";
            const response = await fetch(`${apiBase}/reset-db`, { method: 'POST' });
            if (response.ok) {
                alert("Database reset! You can now upload new files.");
                window.location.reload();
            }
        } catch (err) {
            alert("Reset failed: " + err.message);
        }
    };

    return (
        <div className="file-upload">
            <h3>{t.uploadSection}</h3>
            <div className="upload-box">
                <input type="file" onChange={handleFileChange} accept=".csv,.xlsx" />
                <button onClick={handleUpload} disabled={!file || uploading}>
                    {uploading ? 'Processing...' : 'Process Now'}
                </button>
            </div>
            {status && <p className="status-msg">{status}</p>}

            <div>
                <button
                    onClick={resetDatabase}
                    style={{ backgroundColor: '#ff4444', color: 'white', border: 'none', borderRadius: '4px', padding: '8px 12px', cursor: 'pointer' }}
                >
                    🗑️ Reset Demo Data
                </button>
            </div>
        </div>
    );
};

export default FileUpload;
