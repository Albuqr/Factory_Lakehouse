import os
import json
from google.cloud import bigquery
from google.oauth2 import service_account
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

PROJECT_ID = "factory-lakehouse"
DATASET_ID = "factory_lakehouse"

_BQ_SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]

creds_json = os.environ.get("GCP_CREDENTIALS_JSON")
creds_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

if creds_json:
    # VPS/production: JSON string passed as env var, no file mount needed
    _info = json.loads(creds_json)
    _credentials = service_account.Credentials.from_service_account_info(_info, scopes=_BQ_SCOPES)
    client = bigquery.Client(credentials=_credentials, project=PROJECT_ID)
elif creds_path:
    if not os.path.isabs(creds_path):
        creds_path = os.path.join(os.path.dirname(__file__), '..', creds_path)
    client = bigquery.Client.from_service_account_json(creds_path, project=PROJECT_ID)
else:
    # Cloud Run / GKE: ADC injected by the platform
    client = bigquery.Client(project=PROJECT_ID)