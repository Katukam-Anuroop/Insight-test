import os
import google.generativeai as genai
from dotenv import load_dotenv
import json
import re

load_dotenv()

def plan_charts(profile_json):
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    prompt = f"""
    Given this data profile (JSON), list up to 6 chart types (with columns) that best explain the data to a non-technical manager. Output as a JSON array of objects: [{{type, columns, rationale}}]. Do not include any explanations or extra text, just the JSON.
    Data Profile: {profile_json}
    """
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    # Extract JSON block robustly
    text = response.text.strip()
    # Remove Markdown code block markers if present
    if text.startswith("```json"):
        text = text.lstrip("```json").rstrip("```").strip()
    elif text.startswith("```"):
        text = text.lstrip("```").rstrip("```").strip()
    # Try to find JSON array with regex if output contains explanation
    match = re.search(r'(\[.*\])', text, re.DOTALL)
    if match:
        json_str = match.group(1)
    else:
        json_str = text
    try:
        chart_plan = json.loads(json_str)
    except Exception as e:
        raise RuntimeError(f"Could not parse chart plan from Gemini response: {text}\nError: {e}")
    return chart_plan
