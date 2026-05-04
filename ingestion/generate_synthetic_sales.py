import random
import pandas as pd
from pathlib import Path

random.seed(42)

DATA_RAW = Path("./data/raw")

cost_df = pd.read_excel(DATA_RAW / "bronze_synthetic_planned_cost.xlsx")
cost_df["month_key"] = cost_df["month_key"].astype(str)

prod_df = pd.read_excel(DATA_RAW / "bronze_production_plan.xlsx")
prod_df["month_key"] = pd.to_datetime(prod_df["production_date"]).dt.strftime("%Y%m")
prod_df["product_line"] = prod_df["sku"].map({"PAO_DE_MEL": "pao_de_mel", "TRUFA": "trufa"})

monthly_units = (
    prod_df.groupby(["product_line", "month_key"])["units_produced"]
    .sum()
    .reset_index()
    .rename(columns={"units_produced": "planned_units"})
)

merged = cost_df.merge(monthly_units, on=["product_line", "month_key"], how="inner")

records = []
for _, row in merged.iterrows():
    cost_per_unit = row["planned_cost_brl"] / row["planned_units"]
    price_per_unit = cost_per_unit * random.uniform(1.40, 1.60)

    sell_rate = random.uniform(0.80, 0.95)
    variance = random.uniform(0.85, 1.15)
    units_sold = int(row["planned_units"] * sell_rate * variance)

    records.append({
        "month_key": row["month_key"],
        "sku_name": row["product_line"],
        "units_sold": units_sold,
        "revenue_brl": round(units_sold * price_per_unit, 2),
    })

df = pd.DataFrame(records).sort_values(["month_key", "sku_name"]).reset_index(drop=True)
df.to_csv(DATA_RAW / "bronze_synthetic_sales.csv", index=False)

print(f"Generated {len(df)} records ({df['sku_name'].nunique()} SKUs × {df['month_key'].nunique()} months)")
print(df.groupby("sku_name")[["units_sold", "revenue_brl"]].mean().round(0).to_string())
