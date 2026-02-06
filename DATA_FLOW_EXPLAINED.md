# Complete Data Flow: Upload → Processing → AI → Database

## 📤 Step 1: File Upload

**User Action:** Upload `sample_financial_data.csv`

**File Content Example:**
```csv
date,category,amount,type
2023-10-01,Sales Revenue,50000,Revenue
2023-10-02,Office Rent,15000,Expense
2023-10-03,Salaries,30000,Expense
2023-10-04,Product Sales,75000,Revenue
... (more rows)
```

**Frontend (`FileUpload.jsx`):**
```javascript
POST http://localhost:8000/upload
Content-Type: multipart/form-data
Body: [CSV file bytes]
```

---

## 🔄 Step 2: Backend Processing

### 2.1 File Reception (`main.py` - `/upload` endpoint)
```python
file.read()  # Reads raw bytes
filename = "sample_financial_data.csv"
```

### 2.2 Parsing (`processor.py`)
```python
# Converts bytes → DataFrame
df = pd.read_csv(BytesIO(file_content))

# Normalizes column names to lowercase
df.columns = ['date', 'category', 'amount', 'type']

# Converts to list of dictionaries
records = [
    {'date': '2023-10-01', 'category': 'Sales Revenue', 'amount': 50000.0, 'type': 'Revenue'},
    {'date': '2023-10-02', 'category': 'Office Rent', 'amount': 15000.0, 'type': 'Expense'},
    {'date': '2023-10-03', 'category': 'Salaries', 'amount': 30000.0, 'type': 'Expense'},
    # ... all rows
]
```

### 2.3 Database Storage (`main.py`)

**Step A: Find/Create Company**
```sql
SELECT * FROM companies WHERE id = 1;
-- If not found, creates:
INSERT INTO companies (name, industry) VALUES ('Demo SME', 'Retail');
-- Returns: company_id = 1
```

**Step B: Store Each Record**
```sql
-- For EACH row in CSV:
INSERT INTO financial_records (
    company_id, category, amount, record_type, date, source_document
) VALUES (
    1, 'Sales Revenue', 50000.0, 'Revenue', '2023-10-01', 'sample_financial_data.csv'
);
-- Repeats for all 13 rows in your sample CSV
```

**Database After Upload:**
```
companies table:
+----+-----------+----------+
| id | name      | industry |
+----+-----------+----------+
| 1  | Demo SME  | Retail   |
+----+-----------+----------+

financial_records table:
+----+------------+---------------+--------+-------------+------------+
| id | company_id | category      | amount | record_type | date       |
+----+------------+---------------+--------+-------------+------------+
| 1  | 1          | Sales Revenue | 50000  | Revenue     | 2023-10-01 |
| 2  | 1          | Office Rent   | 15000  | Expense     | 2023-10-02 |
| 3  | 1          | Salaries      | 30000  | Expense     | 2023-10-03 |
... (13 total rows)
```

**Response to Frontend:**
```json
{
  "message": "Successfully processed 13 records.",
  "company_id": 1
}
```

---

## 🤖 Step 3: AI Analysis (When User Clicks "Load Analysis")

### 3.1 Fetch Data from Database
```sql
SELECT category, amount, record_type 
FROM financial_records 
WHERE company_id = 1;
```

**Retrieved Data (all 13 records):**
```python
data_for_ai = [
    {'category': 'Sales Revenue', 'amount': 50000.0, 'type': 'Revenue'},
    {'category': 'Office Rent', 'amount': 15000.0, 'type': 'Expense'},
    {'category': 'Salaries', 'amount': 30000.0, 'type': 'Expense'},
    # ... 10 more records
]
```

### 3.2 Data Reduction (`ai_service.py`)

**IMPORTANT: Only 20 records max sent to AI**
```python
limited_data = data_for_ai[:20]  # Takes first 20 only

# Calculate summary metrics
total_revenue = 125000.0  # Sum of all Revenue records
total_expense = 45000.0   # Sum of all Expense records
net_income = 80000.0      # Revenue - Expense

# Only send 5 sample records + summary
data_summary = "Revenue: 125000.0, Expenses: 45000.0, Net: 80000.0"
sample_records = limited_data[:5]  # Only first 5 records
```

### 3.3 Prompt Sent to LLM

**Exact Content Sent to OpenRouter API:**
```
Analyze this SME financial data and respond ONLY with valid JSON:

Data: Revenue: 149500.0, Expenses: 82200.0, Net: 67300.0
Sample records: [
    {'category': 'Product Sales', 'amount': 45000.0, 'type': 'Revenue'},
    {'category': 'Consulting Fee', 'amount': 12000.0, 'type': 'Revenue'},
    ... (all 14 rows)
]
```
Provide JSON with these exact keys:
{"score": <0-100>, "risk_level": "<Low/Medium/High>", "narrative": "<brief assessment>", "recommendations": ["<tip1>", "<tip2>", "<tip3>"]}

**Token Count:**
- Input: ~600-800 tokens (very small!)
- Max output: 800 tokens

### 3.4 LLM Response

**What OpenRouter Returns:**
```json
{
  "score": 85,
  "risk_level": "Low",
  "narrative": "The company shows strong financial health with positive net income of ₹80,000. Revenue significantly exceeds expenses, indicating good profitability. The business has healthy cash flow with diverse revenue streams.",
  "recommendations": [
    "Consider investing surplus in growth opportunities",
    "Build emergency fund equal to 3 months expenses",
    "Explore tax-saving investment options"
  ]
}
```

### 3.5 Store Assessment in Database

```sql
INSERT INTO assessments (
    company_id, overall_score, risk_level, summary_narrative, recommendations
) VALUES (
    1,
    85.0,
    'Low',
    'The company shows strong financial health...',
    '["Consider investing surplus...", "Build emergency fund...", "Explore tax-saving..."]'
);
-- Returns: assessment_id = 1
```

**Database After Analysis:**
```
assessments table:
+----+------------+-------+-----------+---------------------------+
| id | company_id | score | risk_level| summary_narrative         |
+----+------------+-------+-----------+---------------------------+
| 1  | 1          | 85.0  | Low       | The company shows strong...|
+----+------------+-------+-----------+---------------------------+
```

### 3.6 Response to Frontend

```json
{
  "company": "Demo SME",
  "assessment": {
    "score": 85,
    "risk_level": "Low",
    "narrative": "The company shows strong financial health...",
    "recommendations": ["tip1", "tip2", "tip3"]
  },
  "assessment_id": 1
}
```

---

## 📥 Step 4: PDF Download

**User clicks "Download Report"**

### 4.1 Fetch Stored Assessment (NO AI CALL!)
```sql
SELECT * FROM assessments 
WHERE company_id = 1 
ORDER BY created_at DESC 
LIMIT 1;
-- Returns the SAME assessment from Step 3.5
```

### 4.2 Generate PDF
- Uses stored assessment (score: 85, risk: Low, etc.)
- Calculates financial summary from `financial_records`
- Creates PDF with ReportLab

**Result:** PDF contains **exact same content** as UI ✅

---

## 📊 Summary: What Gets Sent to LLM

| Item | Amount Sent |
|------|-------------|
| **Full CSV rows** | 14 rows uploaded |
| **Stored in DB** | All 14 rows |
| **Sent to AI** | All 14 records + summary metrics |
| **AI Input Tokens** | ~600-800 tokens |
| **AI Output Tokens** | ~200-300 tokens |
| **Total Cost** | Nearly free (well under 4096 limit) |

---

## 🔄 Database Usage Timeline

```
1. Upload CSV
   ↓
   [DB] Store all 13 records in financial_records
   
2. Click "Load Analysis"
   ↓
   [DB] Fetch all 14 records
   ↓
   [AI] Send all 14 records + summary (800 tokens)
   ↓
   [AI] Returns assessment (300 tokens)
   ↓
   [DB] Store assessment in assessments table
   ↓
   [UI] Display assessment
   
3. Click "Download Report"
   ↓
   [DB] Fetch stored assessment (NO AI CALL)
   ↓
   [PDF] Generate report with same data
```

---

## 🎯 Key Points

1. **All CSV data stored** in database
2. **Only 5 records + summary** sent to AI (saves tokens)
3. **AI called once** per analysis
4. **Assessment stored** in database
5. **PDF uses stored assessment** (consistent with UI)
6. **Total tokens: ~600** (very efficient!)
