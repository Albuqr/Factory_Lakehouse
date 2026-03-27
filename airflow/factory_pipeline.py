from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from ingestion.ingest import ingest_transactions_fn, ingest_budget_fn, ingest_production_plan_fn, ingest_maintenance_logs_fn, ingest_equipment_fn

default_args = {
    'owner': 'Joao',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': True,
    'email': ['jpcaastroo@gmail.com']
}

with DAG(
    dag_id='factory_daily_pipeline',
    default_args=default_args,
    schedule_interval='0 6 * * *',
    start_date=datetime(2026, 1, 1),
    catchup=False,
) as dag:

    ingest_transactions = PythonOperator(
        task_id='ingest_transactions',
        python_callable=ingest_transactions_fn,
    )

    ingest_budget = PythonOperator(
        task_id='ingest_budget',
        python_callable=ingest_budget_fn,
    )

    ingest_equipment = PythonOperator(
        task_id='ingest_equipment',
        python_callable=ingest_equipment_fn,
    )

    ingest_production_plan = PythonOperator(
        task_id='ingest_production_plan',
        python_callable=ingest_production_plan_fn,
    )

    ingest_maintenance_logs = PythonOperator(
        task_id='ingest_maintenance_logs',
        python_callable=ingest_maintenance_logs_fn,
    )

    run_silver = BashOperator(
        task_id='run_silver',
        bash_command='dbt run --select silver_transactions,silver_budget,silver_equipment',
    )

    run_gold = BashOperator(
        task_id='run_gold',
        bash_command='dbt run --select gold_budget_vs_actual,gold_cost_per_unit,gold_equipment_status',
    )

    [ingest_transactions, ingest_budget, ingest_equipment, ingest_production_plan, ingest_maintenance_logs] >> run_silver >> run_gold