import random
import pandas as pd



months = []
for year in [2025, 2026]:
    for month in range(1, 13):
        if year == 2026 and month > 4:
            break
        months.append((year, month))


records = []


cost_centers = {
    "Producao": 176000,
    "Materia_Prima": 50000,
    "RH": 25000,
    "Fixas": 2000,
    "Marketing": 1000,
    "Impostos": 6000,
    "Logistica": 3000,
    "Manutencao": 1500,
}

for cost_center, base_amount in cost_centers.items():
    for year, month in months:
        amount = random.randint(int(base_amount * 0.90), int(base_amount * 1.10))
        records.append({
            "cost_center": cost_center,
            "month_key": f"{year}{month:02d}",
            "budget_amount_brl": amount,
        })

df = pd.DataFrame(records)

df.to_excel("./data/raw/bronze_synthetic_budget.xlsx", index=False)