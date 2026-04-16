import random
import pandas as pd


skus = ["TRUFA", "PAO_DE_MEL"]


months = []
for year in [2025, 2026]:
    for month in range(1, 13):
        if year == 2026 and month > 4:
            break
        months.append((year, month))


records = []


for sku in skus:
        for year, month in months:
            # generate record here

            if sku == "TRUFA":
                units = random.randint(int(3000 * 0.85), int(3000 * 1.15))
                revenue = random.randint(int(280000 * 0.85), int(280000 * 1.15))
            else:
                units = random.randint(int(5000 * 0.85), int(5000 * 1.15))
                revenue = random.randint(int(240000 * 0.85), int(240000 * 1.15))

            records.append({
            "sku_name": sku,
            "units_sold": units,
            "revenue_brl": revenue,
            "month_key": f"{year}{month:02d}",
            })

df = pd.DataFrame(records)

df.to_excel("./data/raw/bronze_synthetic_sales.xlsx", index=False)