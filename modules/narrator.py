import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def generate_narrative(profile_summary, chart_plan, forecast_result):
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    prompt = f"""
    You are a data analyst. Write a concise executive-level narrative based on these:
    - Data summary: {profile_summary}
    - Recommended charts: {chart_plan}
    - Forecast result: {forecast_result}
    Focus on key findings, outliers, correlations, data quality issues, and the forecast. Use clear, non-technical language.
    """
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    return response.text.strip()
