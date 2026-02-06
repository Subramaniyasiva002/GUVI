# 🚀 SME Financial Health Platform

A comprehensive, AI-powered financial diagnostic tool designed specifically for Small and Medium Enterprises (SMEs). This platform transforms raw financial data (CSV/Excel) into actionable business intelligence with full support for local Indian languages.

---

## 🛑 The Problem
Many SME owners in India face two major hurdles:
1. **Data Complexity**: Financial statements are often overwhelming and difficult to interpret without an accounting background.
2. **Language Barrier**: Most sophisticated analytical tools are strictly in English, making them less accessible to a significant portion of the business community.

## ✅ Our Solution
This platform bridges the gap between raw numbers and strategic decision-making by providing:
- **Instant AI Diagnostics**: Uses advanced LLMs to identify trends, risks, and health scores in seconds.
- **Multilingual Native Support**: Offers insights in **English**, **Hindi (हिंदी)**, and **Tamil (தமிழ்)** to ensure no business owner is left behind.
- **Financial "GP" Service**: Acts like a general practitioner for business health—flagging issues before they become terminal and suggesting healthy "best practices."

---

## ✨ Key Features

### 1. 🤖 Context-Aware AI Analysis
- **Smart Sampling**: Efficiently processes CSV data by combining total aggregates with representative samples.
- **Health Scoring**: Generates a 0-100 score based on revenue-to-expense ratios, profitability, and consistency.
- **Risk Assessment**: Categorizes business status into Low, Medium, or High risk with clear justifications.

### 2. 🌐 Localized Experience
- **Dynamic Translation**: The entire dashboard and AI-generated narrative switch seamlessly between English, Hindi, and Tamil.
- **Localized Prompts**: AI outputs are fine-tuned to use business-appropriate terminology in the selected language.

### 3. 📄 Automated Reporting
- **PDF Generation**: One-click download of professional financial reports (available for English analysis).
- **Data Persistence**: All assessments are stored in a PostgreSQL database (Neon) for future review and audit trails.

### 4. ⚡ Intelligent Performance
- **Duplicate Detection**: Uses MD5 file hashing to recognize previously processed files, saving AI costs and providing instant results for re-uploads.
- **Cloud-Native**: Ready for deployment on modern platforms like Render (Backend) and Vercel/Netlify (Frontend).

---

## 🛠️ Technology Stack
- **Backend**: FastAPI (Python), SQLAlchemy, PostgreSQL (Neon.tech), ReportLab (PDFs).
- **Frontend**: React.js (Vite), Pure CSS3 (Modern Glassmorphism aesthetics).
- **AI Engine**: OpenRouter API (GPT models) for high-quality, cost-effective reasoning.

---

## 📦 How to Run

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

---

## 🌟 Vision
To empower every small business owner in India with the same quality of financial analysis previously reserved only for large corporations with expensive CFOs.
