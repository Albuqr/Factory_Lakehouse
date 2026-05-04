FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY Home.py config.py queries.py sidebar.py ./
COPY pages/ pages/
COPY .streamlit/ .streamlit/

EXPOSE 8765

CMD ["streamlit", "run", "Home.py", \
     "--server.port=8765", \
     "--server.address=0.0.0.0", \
     "--server.headless=true", \
     "--server.enableCORS=false", \
     "--server.enableXsrfProtection=false"]
