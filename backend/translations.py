"""
Multilingual support for SME Financial Health Platform
Supports: English, Hindi, Tamil
"""

TRANSLATIONS = {
    "en": {
        "app_title": "SME Financial Health Platform",
        "upload_section": "Upload Financial Documents",
        "dashboard_section": "Financial Dashboard",
        "upload_button": "Upload Data",
        "analyze_button": "Load Analysis",
        "refresh_button": "Refresh Analysis",
        "download_report": "Download Report",
        "loading": "Loading Analysis...",
        "no_data": "No analysis data available.",
        "score_label": "Financial Health Score",
        "risk_label": "Risk Level",
        "assessment_label": "Assessment",
        "recommendations_label": "Recommendations",
        "error_upload": "Upload failed",
        "error_analysis": "Analysis failed",
        "success_upload": "Successfully processed",
    },
    "hi": {  # Hindi
        "app_title": "लघु एवं मध्यम उद्यम वित्तीय स्वास्थ्य मंच",
        "upload_section": "वित्तीय दस्तावेज़ अपलोड करें",
        "dashboard_section": "वित्तीय डैशबोर्ड",
        "upload_button": "डेटा अपलोड करें",
        "analyze_button": "विश्लेषण लोड करें",
        "refresh_button": "विश्लेषण रीफ्रेश करें",
        "download_report": "रिपोर्ट डाउनलोड करें",
        "loading": "विश्लेषण लोड हो रहा है...",
        "no_data": "कोई विश्लेषण डेटा उपलब्ध नहीं है।",
        "score_label": "वित्तीय स्वास्थ्य स्कोर",
        "risk_label": "जोखिम स्तर",
        "assessment_label": "मूल्यांकन",
        "recommendations_label": "सिफारिशें",
        "error_upload": "अपलोड विफल",
        "error_analysis": "विश्लेषण विफल",
        "success_upload": "सफलतापूर्वक संसाधित",
    },
    "ta": {  # Tamil
        "app_title": "சிறு மற்றும் நடுத்தர நிறுவன நிதி சுகாதார தளம்",
        "upload_section": "நிதி ஆவணங்களை பதிவேற்றவும்",
        "dashboard_section": "நிதி டாஷ்போர்டு",
        "upload_button": "தரவை பதிவேற்றவும்",
        "analyze_button": "பகுப்பாய்வை ஏற்றவும்",
        "refresh_button": "பகுப்பாய்வை புதுப்பிக்கவும்",
        "download_report": "அறிக்கையை பதிவிறக்கவும்",
        "loading": "பகுப்பாய்வு ஏற்றப்படுகிறது...",
        "no_data": "பகுப்பாய்வு தரவு இல்லை.",
        "score_label": "நிதி சுகாதார மதிப்பெண்",
        "risk_label": "ஆபத்து நிலை",
        "assessment_label": "மதிப்பீடு",
        "recommendations_label": "பரிந்துரைகள்",
        "error_upload": "பதிவேற்றம் தோல்வியடைந்தது",
        "error_analysis": "பகுப்பாய்வு தோல்வியடைந்தது",
        "success_upload": "வெற்றிகரமாக செயலாக்கப்பட்டது",
    }
}

def get_text(key: str, lang: str = "en") -> str:
    """Get translated text for a given key and language"""
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)
