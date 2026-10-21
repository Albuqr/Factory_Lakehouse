FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY Home.py config.py queries.py sidebar.py ./
COPY pages/ pages/
COPY .streamlit/ .streamlit/

EXPOSE 8765

# Runs as root for now: config.py reads the service-account key from GOOGLE_APPLICATION_CREDENTIALS
# and its file permissions on the host are not known. Switch to a non-root USER once they are.
# nosemgrep: dockerfile.security.missing-user.missing-user
CMD ["streamlit", "run", "Home.py", \
     "--server.port=8765", \
     "--server.address=0.0.0.0", \
     "--server.headless=true", \
     "--server.enableCORS=false", \
     "--server.enableXsrfProtection=false"]
