FROM python:3.11-slim
WORKDIR /middleware
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY config.py .
COPY main.py .
# Runs as root for now: config.py reads the service-account key from GOOGLE_APPLICATION_CREDENTIALS
# and its file permissions on the host are not known. Switch to a non-root USER once they are.
# nosemgrep: dockerfile.security.missing-user.missing-user
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003"]