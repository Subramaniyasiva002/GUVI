import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = "openai/gpt-oss-20b:free"  # You can change model here

def query_openrouter(prompt):
    """Query OpenRouter API with rate limiting"""
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://sme-health-platform.com",  # REQUIRED by OpenRouter
        "X-Title": "SME Financial Health"  # Custom title (mandatory)
    }
    data = {
        "model": OPENROUTER_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 1000  # Limit response to stay within budget
    }

    try:
        # Add delay before API call to avoid rate limits (reduced for better UX)
        time.sleep(0.5)  # 0.5 second delay
        
        print(f"🔄 Calling OpenRouter with model: {OPENROUTER_MODEL}")
        response = requests.post(url, headers=headers, json=data)
        res_json = response.json()
        print(f"✅ OpenRouter Response Status: {response.status_code}")

        # Handle API errors safely
        if "choices" in res_json:
            return res_json["choices"][0]["message"]["content"]
        elif "error" in res_json:
            print("🚨 OpenRouter Error:", res_json["error"])
            return f"[Error: {res_json['error'].get('message', 'Unknown error')}]"
        else:
            print("⚠️ Unexpected Response:", res_json)
            return "[Error: Unexpected API response]"

    except Exception as e:
        print("❌ Exception calling OpenRouter:", e)
        return f"[Exception: {str(e)}]"


def generate_financial_assessment(financial_data: list, language: str = "en") -> dict:
    """
    Sends financial data to OpenRouter to generate an assessment.
    
    Args:
        financial_data: List of financial records
        language: Language code ('en', 'hi', 'ta') for response
    """
    
    # Language mapping
    language_names = {
        "en": "English",
        "hi": "Hindi (हिंदी)",
        "ta": "Tamil (தமிழ்)"
    }
    
    lang_name = language_names.get(language, "English")
    
    # Limit data to avoid context length issues (max 20 records)
    limited_data = financial_data[:20]
    
    # Calculate basic metrics to reduce token usage
    total_revenue = sum(r['amount'] for r in limited_data if r.get('type') == 'Revenue')
    total_expense = sum(r['amount'] for r in limited_data if r.get('type') == 'Expense')
    net_income = total_revenue - total_expense
    
    # Create concise data summary
    data_summary = f"Revenue: {total_revenue}, Expenses: {total_expense}, Net: {net_income}"
    
    # Language-specific prompt
    prompt = f"""Analyze this SME financial data and respond in {lang_name} language.

Data: {data_summary}
Sample records: {str(limited_data[:14])}

IMPORTANT: Respond ONLY in {lang_name}. Provide JSON with these exact keys:
{{"score": <0-100>, "risk_level": "<Low/Medium/High>", "narrative": "<brief assessment in {lang_name}>", "recommendations": ["<tip1 in {lang_name}>", "<tip2 in {lang_name}>", "<tip3 in {lang_name}>"]}}"""

    try:
        response_content = query_openrouter(prompt)
        
        # Check for error responses
        if response_content.startswith("[Error:") or response_content.startswith("[Exception:"):
            return {
                "error": response_content,
                "narrative": "Could not generate assessment due to an API error."
            }
        
        # Aggressive JSON extraction
        import json
        import re
        
        try:
            # 1. Try to find JSON block in markdown
            cleaned = response_content.strip()
            json_match = re.search(r'\{.*\}', cleaned, re.DOTALL)
            
            if json_match:
                cleaned = json_match.group(0)
            
            parsed = json.loads(cleaned)
            
            # 2. Flatten nested response if necessary
            if isinstance(parsed, dict):
                # Handle cases where model wraps everything in a top-level key
                for nested_key in ['assessment', 'financial_assessment', 'result', 'analysis', 'data']:
                    if nested_key in parsed and isinstance(parsed[nested_key], dict):
                        parsed = parsed[nested_key]
                        break
            
            # 3. Normalize keys with flexible mapping
            def get_val(keys, default=""):
                for k in keys:
                    if k in parsed: return parsed[k]
                return default

            result = {
                "score": get_val(['score', 'health_score', 'overall_score', 'financial_health_score'], "N/A"),
                "risk_level": get_val(['risk_level', 'risk', 'risk_assessment', 'risk_category'], "Unknown"),
                "narrative": get_val(['narrative', 'assessment', 'summary', 'analysis', 'detailed_assessment'], ""),
                "recommendations": get_val(['recommendations', 'tips', 'action_items', 'suggestions'], [])
            }
            
            # 4. Final Cleanup: If narrative is empty, use the whole original string (sanitized)
            if not result['narrative'] or len(str(result['narrative'])) < 10:
                # If we couldn't find a narrative but found other keys, 
                # maybe the AI put the narrative in a non-standard key
                potential_narrative = ""
                for k, v in parsed.items():
                    if isinstance(v, str) and len(v) > 50 and k not in ['risk_level', 'score']:
                        potential_narrative = v
                        break
                result['narrative'] = potential_narrative or "Assessment generated successfully."
                
            return result
            
        except (json.JSONDecodeError, Exception) as e:
            print(f"⚠️ JSON Parse Attempt Failed: {e}")
            # Mega fallback: Return the raw content in narrative so at least something shows
            return {
                "score": "N/A",
                "risk_level": "Unknown",
                "narrative": response_content,
                "recommendations": []
            }
        
    except Exception as e:
        print(f"AI Generation Error: {e}")
        return {"error": str(e), "narrative": "Could not generate assessment due to an error."}
