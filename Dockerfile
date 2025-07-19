FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for ydata-profiling, wordcloud, phik, and WeasyPrint
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    cmake \
    libcairo2 \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    libxml2 \
    libxml2-dev \
    libxslt1.1 \
    libxslt1-dev \
    libfreetype6 \
    gobject-introspection \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
