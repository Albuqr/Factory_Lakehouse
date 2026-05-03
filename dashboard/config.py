import os
from google.cloud import bigquery
from dotenv import load_dotenv

load_dotenv(dotenv_path='../.env')

creds_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
if not creds_path.startswith('/'):

    creds_path = os.path.join(os.path.dirname(__file__), '..', creds_path)

client = bigquery.Client.from_service_account_json(creds_path)

PROJECT_ID = "factory-lakehouse"
DATASET_ID = "factory_lakehouse"