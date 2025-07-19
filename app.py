import streamlit as st
import tempfile
from modules.profiler import profile_data
from modules.chart_planner import plan_charts
from modules.visual_builder import build_charts
from modules.forecaster import forecast_series
from modules.narrator import generate_narrative
from modules.chart_narrator import narrate_chart

from modules.pdf_compositor import compose_pdf
import pandas as pd
import os

st.set_page_config(page_title="InsightPress", layout="wide")
st.title("InsightPress: Data → Insight PDF with Forecasts and Narratives")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("CSV uploaded! Starting analysis...")

    # 1. Data Profiling
    with st.spinner("Profiling data..."):
        profile_json, profile_summary = profile_data(df)
        st.json(profile_summary)

    # 2. Chart Planning (via Gemini prompt)
    with st.spinner("Selecting best charts..."):
        chart_plan = plan_charts(profile_json)
        st.write("Recommended Charts:", chart_plan)

    with st.spinner("Building charts..."):
        chart_infos = build_charts(df, chart_plan)
        for chart in chart_infos:
            st.image(chart["img_path"], caption=chart["title"])

    # 4. Generate narrations for each chart
    with st.spinner("Generating chart explanations..."):
        chart_narrations = []
        for chart in chart_infos:
            narration = narrate_chart(chart, df)
            st.write(f"**{chart['title']}**: {narration}")
            chart_narrations.append(narration)

    # 4. Time-Series Forecasting (if date columns)
    with st.spinner("Checking for time-series columns..."):
        forecast_result = forecast_series(df, chart_plan)
        if forecast_result:
            st.image(forecast_result['forecast_plot'])
            st.write("Forecast MAPE:", forecast_result['mape'])

    # 5. Narrative Generation (Gemini or GPT)
    with st.spinner("Generating natural-language summary..."):
        narrative = generate_narrative(profile_summary, chart_plan, forecast_result)
        st.write(narrative)

    # 6. PDF Generation
    if st.button("Generate PDF Report"):
        with st.spinner("Composing PDF..."):
            pdf_bytes = compose_pdf(
                cover_title="InsightPress - Automated Data-to-Insight PDF",
                data_profile=profile_summary,
                chart_infos=chart_infos,
                chart_narrations=chart_narrations,
                forecast=forecast_result,
                narrative=narrative
            )
            st.success("PDF ready! Download below:")
            st.download_button(
                label="Download PDF",
                data=pdf_bytes,
                file_name="insightpress_report.pdf",
                mime="application/pdf"
            )