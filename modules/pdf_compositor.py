from weasyprint import HTML
from jinja2 import Template
import tempfile

def compose_pdf(cover_title, data_profile, chart_infos, chart_narrations, forecast, narrative, quality_notes=None, recommendations=None):
    template = """
    <html>
    <head>
      <style>
        body { font-family: Arial, sans-serif; margin: 32px; }
        h1, h2, h3 { color: #2d3e50; }
        .chart-section { margin-bottom: 40px; }
        img { width: 60%; border: 1px solid #ddd; margin: 16px 0; }
      </style>
    </head>
    <body>
      <h1>{{ cover_title }}</h1>
      <h2>Executive Summary</h2>
      <p>{{ narrative }}</p>
      <h2>Dataset Profile</h2>
      <pre>{{ data_profile }}</pre>
      <h2>Charts and Visual Explanations</h2>
      {% for chart, explanation in charts %}
        <div class="chart-section">
          <h3>{{ chart.title }}</h3>
          <img src="file://{{ chart.img_path }}" />
          <p><b>Explanation:</b> {{ explanation }}</p>
        </div>
      {% endfor %}
      {% if forecast %}
        <h2>ML Forecasting</h2>
        <img src="file://{{ forecast.plot }}" />
        <p><b>Explanation:</b> {{ forecast.explanation }}</p>
      {% endif %}
      {% if quality_notes %}
        <h2>Data Quality Notes</h2>
        <p>{{ quality_notes }}</p>
      {% endif %}
      {% if recommendations %}
        <h2>Conclusion & Recommendations</h2>
        <p>{{ recommendations }}</p>
      {% endif %}
    </body>
    </html>
    """
    html = Template(template).render(
        cover_title=cover_title,
        data_profile=data_profile,
        charts=zip(chart_infos, chart_narrations),
        forecast=forecast,
        narrative=narrative,
        quality_notes=quality_notes,
        recommendations=recommendations
    )
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
        HTML(string=html).write_pdf(f.name)
        f.seek(0)
        pdf_bytes = f.read()
    return pdf_bytes
