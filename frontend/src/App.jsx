import { useState } from 'react'
import './App.css'
import Dashboard from './Dashboard'
import FileUpload from './FileUpload'

function App() {
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const [uploadResult, setUploadResult] = useState(null);

  const handleUploadSuccess = (result) => {
    setUploadResult(result);
    // Trigger dashboard refresh
    setRefreshTrigger(prev => prev + 1);
  }

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>SME Financial Health Platform</h1>
      </header>
      <main className="app-main">
        <section className="upload-section">
          <h2>Upload Financial Documents</h2>
          <FileUpload onUploadSuccess={handleUploadSuccess} />
        </section>
        <section className="dashboard-section">
          <h2>Financial Dashboard</h2>
          <Dashboard key={refreshTrigger} uploadResult={uploadResult} />
        </section>
      </main>
    </div>
  )
}

export default App
