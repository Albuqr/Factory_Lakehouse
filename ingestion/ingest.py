import pandas as pd
from google.cloud import bigquery
from dotenv import load_dotenv
import os
import re
from unidecode import unidecode

load_dotenv()

_creds_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
if not _creds_path:
    raise EnvironmentError(
        "GOOGLE_APPLICATION_CREDENTIALS is not set. "
        "Copy .env.example to .env and point it at your service account JSON file."
    )
client = bigquery.Client.from_service_account_json(_creds_path)

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
    load_job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    load_job.result()
    rows = client.get_table(table_id).num_rows
    if rows != len(df):
        raise ValueError(f'rows = {rows} , not equal to len = {len(df)} on {table_id}')

def ingest_budget_fn():
    df = pd.read_excel("./data/raw/Brumelli.xlsx", sheet_name="DRE", header=None)
    df.columns = df.columns.astype(str)
    cols_to_convert = [c for c in df.columns if c != "ingestion_date"]
    df[cols_to_convert] = df[cols_to_convert].astype(str)
    df["ingestion_date"] = pd.Timestamp.now()
    table_id = "factory-lakehouse.factory_lakehouse.bronze_budget"
    load_job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    load_job.result()
    rows = client.get_table(table_id).num_rows
    if rows != len(df):
        raise ValueError(f'rows = {rows} , not equal to len = {len(df)} on {table_id}')

def ingest_equipment_fn():
    df = pd.read_excel("./data/raw/Inventario.xlsx")
    df.columns = [re.sub(r'[^a-z0-9_]', '_', unidecode(col).lower().strip()) for col in df.columns]
    df["ingestion_date"] = pd.Timestamp.now()
    table_id = "factory-lakehouse.factory_lakehouse.bronze_equipment"
    load_job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    load_job.result()
    rows = client.get_table(table_id).num_rows
    if rows != len(df):
        raise ValueError(f'rows = {rows} , not equal to len = {len(df)} on {table_id}')

def ingest_production_plan_fn():
    df = pd.read_excel("./data/raw/bronze_production_plan.xlsx")
    df["ingestion_date"] = pd.Timestamp.now()
    table_id = "factory-lakehouse.factory_lakehouse.bronze_production_plan"
    load_job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    load_job.result()
    rows = client.get_table(table_id).num_rows
    if rows != len(df):
        raise ValueError(f'rows = {rows} , not equal to len = {len(df)} on {table_id}')

def ingest_maintenance_logs_fn():
    df = pd.read_excel("./data/raw/bronze_maintenance_logs.xlsx")
    df["ingestion_date"] = pd.Timestamp.now()
    table_id = "factory-lakehouse.factory_lakehouse.bronze_maintenance_logs"
    load_job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    load_job.result()
    rows = client.get_table(table_id).num_rows
    if rows != len(df):
        raise ValueError(f'rows = {rows} , not equal to len = {len(df)} on {table_id}')

def ingest_r_produto_fn():
    df = pd.read_excel("./data/raw/Brumelli.xlsx", sheet_name="R. Produto", header=None)
    df.columns = df.columns.astype(str)
    cols_to_convert = [c for c in df.columns if c != "ingestion_date"]
    df[cols_to_convert] = df[cols_to_convert].astype(str)
    df["ingestion_date"] = pd.Timestamp.now()
    table_id = "factory-lakehouse.factory_lakehouse.bronze_r_produto"
    load_job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    load_job.result()
    rows = client.get_table(table_id).num_rows
    if rows != len(df):
        raise ValueError(f'rows = {rows} , not equal to len = {len(df)} on {table_id}')

def ingest_synthetic_sales_fn():
    df = pd.read_csv("./data/raw/bronze_synthetic_sales.csv")
    df["ingestion_date"] = pd.Timestamp.now()
    table_id = "factory-lakehouse.factory_lakehouse.bronze_synthetic_sales"
    load_job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    load_job.result()
    rows = client.get_table(table_id).num_rows
    if rows != len(df):
        raise ValueError(f'rows = {rows} , not equal to len = {len(df)} on {table_id}')


def ingest_synthetic_budget_fn():
    df = pd.read_excel("./data/raw/bronze_synthetic_budget.xlsx")
    df["ingestion_date"] = pd.Timestamp.now()
    table_id = "factory-lakehouse.factory_lakehouse.bronze_synthetic_budget"
    load_job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    load_job.result()
    rows = client.get_table(table_id).num_rows
    if rows != len(df):
        raise ValueError(f'rows = {rows} , not equal to len = {len(df)} on {table_id}')

def ingest_synthetic_planned_cost_fn():
    df = pd.read_excel("./data/raw/bronze_synthetic_planned_cost.xlsx")
    df["ingestion_date"] = pd.Timestamp.now()
    table_id = "factory-lakehouse.factory_lakehouse.bronze_synthetic_planned_cost"
    load_job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    load_job.result()
    rows = client.get_table(table_id).num_rows
    if rows != len(df):
        raise ValueError(f'rows = {rows} , not equal to len = {len(df)} on {table_id}')


