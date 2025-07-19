import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def narrate_chart(chart, df):
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    sample = df[chart["columns"]].head(10).to_dict(orient='records')
    prompt = f"""
You are a data analyst. Explain the following chart for a business reader:
- Chart Type: {chart['type']}
- Columns: {', '.join(chart['columns'])}
- Chart Title: {chart['title']}
- Chart Rationale: {chart['rationale']}
- Data Sample: {sample}
In 2-3 sentences, describe what this chart shows, mention any visible trends, clusters, or outliers, and provide an actionable insight if possible.
"""
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    return response.text.strip()
