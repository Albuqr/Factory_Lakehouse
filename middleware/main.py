from config import client, PROJECT_ID, DATASET_ID

from fastapi import FastAPI

app = FastAPI()

@app.get("/api/budget-variance")
def budget_variance():
    query = """
        select cost_center, budget_amount_brl, month_key

        from  

        `factory-lakehouse.factory_lakehouse.silver_budget`
            where month_key = (
            SELECT max(month_key) FROM `factory-lakehouse.factory_lakehouse.silver_budget`)
    """
    query_job = client.query(query)
    results = query_job.result()
    data = [{**dict(row.items()), "variance_brl": None, "variance_pct": None, "status_flag": None} for row in results]

    return {"data": data}

@app.get("/api/equipment_status")
def equipment_status():
    query = """
        select *
        
        from

        `factory-lakehouse.factory_lakehouse.gold_equipment_status`
    """
    query_job = client.query(query)
    results = query_job.result()
    data = [dict(row.items()) for row in results]

    return {"data": data}


@app.get("/api/sku_economics")
def sku_economics():
    query = """
        select *

        from

        `factory-lakehouse.factory_lakehouse.gold_cost_per_unit`
        where month_key = (
            SELECT max(month_key) FROM `factory-lakehouse.factory_lakehouse.gold_cost_per_unit`)
    """
    query_job = client.query(query)
    results = query_job.result()
    data = [dict(row.items()) for row in results]

    return {"data": data}