import pandas as pd
from google.cloud import bigquery

client = bigquery.Client.from_service_account_json('./gcp-credentials.json')

job_config = bigquery.LoadJobConfig(
    time_partitioning=bigquery.TimePartitioning(
        field="ingestion_date"
    )
)

def ingest_transactions_fn():
    df = pd.read_excel("./data/raw/bronze_transactions.xlsx")
    df["ingestion_date"] = pd.Timestamp.now()
    table_id = "factory-lakehouse.factory_lakehouse.bronze_transactions"
    client.load_table_from_dataframe(df, table_id, job_config=job_config)

def ingest_budget_fn():
    df = pd.read_excel("./data/raw/bronze_budget.xlsx")
    df["ingestion_date"] = pd.Timestamp.now()
    table_id = "factory-lakehouse.factory_lakehouse.bronze_budget"
    client.load_table_from_dataframe(df, table_id, job_config=job_config)

def ingest_equipment_fn():
    df = pd.read_excel("./data/raw/bronze_equipment.xlsx")
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