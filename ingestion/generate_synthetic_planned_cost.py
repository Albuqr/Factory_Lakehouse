import random
import pandas as pd
from datetime import date


df = pd.read_excel("data/raw/Brumelli.xlsx", sheet_name='R. Produto', header=None)
filtered_df = df[df[0].astype(str).str.contains('trufa|pão de mel', case=False, na=False)]


trufa_row = 0 if 'trufa' in str(filtered_df.iloc[0, 0]).lower() else 1
pao_row = 1 - trufa_row

months = []
for year in [2025, 2026]:
    for month in range(1, 13):
        if year == 2026 and month > 4:
            break
        months.append((year, month))


rows = []

for year, month in months:

    month_key = f"{year}{month:02}"

    for product_line, row_index in [('pao_de_mel', pao_row), ('trufa', trufa_row)]:

        base_cost = filtered_df.iloc[row_index, month]

        varied_cost = random.randint(int(base_cost * 0.9), int(base_cost * 1.1))

        rows.append({
            'product_line': product_line,
            'month_key': month_key,
            'planned_cost_brl': varied_cost,
            'ingestion_date': date.today()
        })

final = pd.DataFrame(rows)

final.to_excel("./data/raw/bronze_synthetic_planned_cost.xlsx", index=False)
