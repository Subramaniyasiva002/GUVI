import { useState, useEffect } from 'react';

const TRANSLATIONS = {
    en: {
        title: "SME Financial Health Platform",
        uploadSection: "Upload Financial Documents",
        dashboardSection: "Financial Dashboard",
        loadAnalysis: "Load Analysis",
        refreshAnalysis: "Refresh Analysis",
        downloadReport: "Download Report",
        loading: "⏳ Loading Analysis...",
        noData: "No analysis data available.",
        score: "Financial Health Score",
        riskLevel: "Risk Level",
        assessment: "Assessment",
        recommendations: "Recommendations",
        languageNotice: "Select language before loading analysis for results in your preferred language",
    },
    hi: {
        title: "लघु एवं मध्यम उद्यम वित्तीय स्वास्थ्य मंच",
        uploadSection: "वित्तीय दस्तावेज़ अपलोड करें",
        dashboardSection: "वित्तीय डैशबोर्ड",
        loadAnalysis: "विश्लेषण लोड करें",
        refreshAnalysis: "विश्लेषण रीफ्रेश करें",
        downloadReport: "रिपोर्ट डाउनलोड करें",
        loading: "⏳ विश्लेषण लोड हो रहा है...",
        noData: "कोई विश्लेषण डेटा उपलब्ध नहीं है।",
        score: "वित्तीय स्वास्थ्य स्कोर",
        riskLevel: "जोखिम स्तर",
        assessment: "मूल्यांकन",
        recommendations: "सिफारिशें",
        languageNotice: "अपनी पसंदीदा भाषा में परिणाम के लिए विश्लेषण लोड करने से पहले भाषा चुनें",
    },
    ta: {
        title: "சிறு மற்றும் நடுத்தர நிறுவன நிதி சுகாதார தளம்",
        uploadSection: "நிதி ஆவணங்களை பதிவேற்றவும்",
        dashboardSection: "நிதி டாஷ்போர்டு",
        loadAnalysis: "பகுப்பாய்வை ஏற்றவும்",
        refreshAnalysis: "பகுப்பாய்வை புதுப்பிக்கவும்",
        downloadReport: "அறிக்கையை பதிவிறக்கவும்",
        loading: "⏳ பகுப்பாய்வு ஏற்றப்படுகிறது...",
        noData: "பகுப்பாய்வு தரவு இல்லை.",
        score: "நிதி சுகாதார மதிப்பெண்",
        riskLevel: "ஆபத்து நிலை",
        assessment: "மதிப்பீடு",
        recommendations: "பரிந்துரைகள்",
        languageNotice: "உங்கள் விருப்பமான மொழியில் முடிவுகளுக்கு பகுப்பாய்வை ஏற்றுவதற்கு முன் மொழியைத் தேர்ந்தெடுக்கவும்",
    }
};

const Dashboard = ({ uploadResult }) => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [companyId, setCompanyId] = useState(1);
    const [language, setLanguage] = useState('en');

    const t = TRANSLATIONS[language];

    // Auto-load assessment if duplicate file was uploaded
    useEffect(() => {
        if (uploadResult?.duplicate && uploadResult?.assessment) {
            // Duplicate file with existing assessment - show it immediately
            setData({
                company: "Demo SME",
                assessment: uploadResult.assessment
            });
        } else if (uploadResult?.company_id) {
            // New upload - update company ID
            setCompanyId(uploadResult.company_id);
        }
    }, [uploadResult]);

    const fetchAnalysis = async () => {
        setLoading(true);
        setError(null);
        try {
            const apiBase = import.meta.env.VITE_API_URL || "http://localhost:8000";
            const response = await fetch(`${apiBase}/analyze/${companyId}?language=${language}`, {
                method: 'POST'
            });

            if (!response.ok) {
                if (response.status === 404) {
                    throw new Error("No data found. Please upload a file first.");
                }
                throw new Error("Analysis failed");
            }

            const result = await response.json();
            console.log('📊 Full API Response:', result);
            setData(result);
        } catch (err) {
            console.error('❌ Error:', err);
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const downloadReport = () => {
        const apiBase = import.meta.env.VITE_API_URL || "http://localhost:8000";
        window.open(`${apiBase}/download-report/${companyId}`, '_blank');
    };

    if (loading) return <div className="loading">{t.loading}</div>;
    if (error) return <div className="error">❌ Error: {error}</div>;
    if (!data) return (
        <div>
            <div className="language-selector">
                <button onClick={() => setLanguage('en')} className={language === 'en' ? 'active' : ''}>English</button>
                <button onClick={() => setLanguage('hi')} className={language === 'hi' ? 'active' : ''}>हिंदी</button>
                <button onClick={() => setLanguage('ta')} className={language === 'ta' ? 'active' : ''}>தமிழ்</button>
            </div>
            <p className="language-notice">💡 {t.languageNotice}</p>
            <p>{t.noData}</p>
            <button onClick={fetchAnalysis}>{t.loadAnalysis}</button>
        </div>
    );

    const { company, assessment } = data;

    // Use the assessment object directly as it is now guaranteed to be flat from the backend
    const parsedAssessment = assessment || {
        score: "N/A",
        risk_level: "Unknown",
        narrative: "No assessment available",
        recommendations: []
    };

    return (
        <div className="dashboard">
            <h3>{t.assessment} for {company} <span style={{ fontSize: '0.8em', color: '#666' }}>({language === 'en' ? 'English' : language === 'hi' ? 'हिंदी' : 'தமிழ்'})</span></h3>

            <div className="score-card">
                <h4>{t.score}</h4>
                <div className="score-circle">
                    {parsedAssessment.score || "N/A"}
                </div>
                <p>{t.riskLevel}: <strong>{parsedAssessment.risk_level || "Unknown"}</strong></p>
            </div>

            <div className="narrative">
                <h4>{t.assessment}</h4>
                <p style={{ whiteSpace: 'pre-wrap' }}>
                    {parsedAssessment.narrative || "No narrative available"}
                </p>
            </div>

            <div className="recommendations">
                <h4>{t.recommendations}</h4>
                <ul>
                    {parsedAssessment.recommendations && Array.isArray(parsedAssessment.recommendations) && parsedAssessment.recommendations.length > 0
                        ? parsedAssessment.recommendations.map((rec, idx) => (
                            <li key={idx}>{typeof rec === 'string' ? rec : (rec.title || rec)}</li>
                        ))
                        : <li>No specific recommendations available</li>
                    }
                </ul>
            </div>

            <div className="action-buttons">
                <button onClick={fetchAnalysis}>{t.refreshAnalysis}</button>
                {language === 'en' && (
                    <button onClick={downloadReport} className="download-btn">📥 {t.downloadReport}</button>
                )}
            </div>
        </div>
    );
};

export default Dashboard;
