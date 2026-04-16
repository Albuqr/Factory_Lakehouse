import pandas as pd
from google.cloud import bigquery
from dotenv import load_dotenv
import os
import re
from unidecode import unidecode

load_dotenv()
client = bigquery.Client.from_service_account_json(os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))

job_config = bigquery.LoadJobConfig(
    write_disposition="WRITE_TRUNCATE",
    time_partitioning=bigquery.TimePartitioning(
        field="ingestion_date"
    )
)

def ingest_transactions_fn():
    df = pd.read_excel("./data/raw/Brumelli.xlsx", sheet_name="DFC")

    df["ingestion_date"] = pd.Timestamp.now()
    table_id = "factory-lakehouse.factory_lakehouse.bronze_transactions"
    client.load_table_from_dataframe(df, table_id, job_config=job_config)

def ingest_budget_fn():
    df = pd.read_excel("./data/raw/Brumelli.xlsx", sheet_name="DRE", header=None)
    df.columns = df.columns.astype(str)
    cols_to_convert = [c for c in df.columns if c != "ingestion_date"]
    df[cols_to_convert] = df[cols_to_convert].astype(str)
    df["ingestion_date"] = pd.Timestamp.now()
    table_id = "factory-lakehouse.factory_lakehouse.bronze_budget"
    client.load_table_from_dataframe(df, table_id, job_config=job_config)

def ingest_equipment_fn():
    df = pd.read_excel("./data/raw/Inventario.xlsx")
    df.columns = [re.sub(r'[^a-z0-9_]', '_', unidecode(col).lower().strip()) for col in df.columns]
    df["ingestion_date"] = pd.Timestamp.now()
    table_id = "factory-lakehouse.factory_lakehouse.bronze_equipment"
    client.load_table_from_dataframe(df, table_id, job_config=job_config)

def ingest_production_plan_fn():
    df = pd.read_excel("./data/raw/bronze_production_plan.xlsx")
    df["ingestion_date"] = pd.Timestamp.now()
    table_id = "factory-lakehouse.factory_lakehouse.bronze_production_plan"
    client.load_table_from_dataframe(df, table_id, job_config=job_config)

def ingest_maintenance_logs_fn():
    df = pd.read_excel("./data/raw/bronze_maintenance_logs.xlsx")
    df["ingestion_date"] = pd.Timestamp.now()
    table_id = "factory-lakehouse.factory_lakehouse.bronze_maintenance_logs"
    client.load_table_from_dataframe(df, table_id, job_config=job_config)

def ingest_r_produto_fn():
    df = pd.read_excel("./data/raw/Brumelli.xlsx", sheet_name="R. Produto", header=None)
    df.columns = df.columns.astype(str)
    cols_to_convert = [c for c in df.columns if c != "ingestion_date"]
    df[cols_to_convert] = df[cols_to_convert].astype(str)
    df["ingestion_date"] = pd.Timestamp.now()
    table_id = "factory-lakehouse.factory_lakehouse.bronze_r_produto"
    client.load_table_from_dataframe(df, table_id, job_config=job_config)