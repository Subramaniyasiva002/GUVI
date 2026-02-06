import pandas as pd
from typing import List, Dict, Any
import io

def parse_financial_document(file_content: bytes, filename: str) -> List[Dict[str, Any]]:
    """
    Parses a financial document (CSV or XLSX) and returns a list of records.
    Assumes a standard format for simplicity: Date, Category, Amount, Type (Revenue/Expense).
    """
    filename = filename.lower()
    try:
        if filename.endswith('.csv'):
            try:
                # Default UTF-8
                df = pd.read_csv(io.BytesIO(file_content))
            except UnicodeDecodeError:
                # Fallback for Windows Excel CSVs
                df = pd.read_csv(io.BytesIO(file_content), encoding='cp1252')
        elif filename.endswith('.xlsx'):
            df = pd.read_excel(io.BytesIO(file_content))
        else:
            raise ValueError("Unsupported file format. Please upload CSV or XLSX.")

        # Basic standardization - expects specific columns or tries to guess
        # Normalizing column names to lowercase
        df.columns = [c.lower() for c in df.columns]

        required_cols = ['date', 'amount', 'category', 'type']
        
        # Convert date to string (ISO format) for JSON serialization
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
        
        # Fill NaN for optional fields if needed, or handle in loop
        df = df.fillna('')
            
        return df.to_dict(orient='records')
        
    except Exception as e:
        print(f"Error parsing file: {e}")
        raise e
