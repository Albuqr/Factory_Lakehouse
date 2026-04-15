from datetime import date, timedelta
import random
import calendar
import pandas as pd

production_machines = [
    {"machine_id": 2, "machine_name": "Moinho/Triturador Industrial", "location": "Cozinha", "skus": ["PAO_DE_MEL", "TRUFA"]},
    {"machine_id": 3, "machine_name": "Marcepan Rototurbo RT4", "location": "Cozinha", "skus": ["PAO_DE_MEL", "TRUFA"]},
    {"machine_id": 4, "machine_name": "Dosadora de Pão de Mel", "location": "Cozinha", "skus": ["PAO_DE_MEL"]},
    {"machine_id": 5, "machine_name": "Batedeira Industrial Planetária Grande", "location": "Cozinha", "skus": ["PAO_DE_MEL", "TRUFA"]},
    {"machine_id": 6, "machine_name": "Tanque Encamisado com Agitador (Chocolate)", "location": "Cozinha", "skus": ["PAO_DE_MEL", "TRUFA"]},
    {"machine_id": 7, "machine_name": "Tanque Encamisado com Descarga Inferior", "location": "Cozinha", "skus": ["PAO_DE_MEL", "TRUFA"]},
    {"machine_id": 8, "machine_name": "Tanque Elétrico com Resistências", "location": "Cozinha", "skus": ["PAO_DE_MEL", "TRUFA"]},
    {"machine_id": 9, "machine_name": "Batedeira Planetária Industrial", "location": "Cozinha", "skus": ["PAO_DE_MEL", "TRUFA"]},
    {"machine_id": 10, "machine_name": "Tanque SIDMAQ", "location": "Cozinha", "skus": ["PAO_DE_MEL", "TRUFA"]},
    {"machine_id": 11, "machine_name": "Embaladora Dupla Torção ICMO", "location": "Estoque", "skus": ["PAO_DE_MEL", "TRUFA"]},
    {"machine_id": 12, "machine_name": "Seladora Térmica B-80", "location": "Estoque", "skus": ["PAO_DE_MEL", "TRUFA"]},
    {"machine_id": 13, "machine_name": "Tanque Encamisado com Painel Elétrico", "location": "Cozinha", "skus": ["PAO_DE_MEL", "TRUFA"]},
    {"machine_id": 14, "machine_name": "Enrobadora de Pão de Mel", "location": "Cozinha", "skus": ["PAO_DE_MEL"]},
    {"machine_id": 15, "machine_name": "Embaladora Flow Pack 1", "location": "Estoque", "skus": ["PAO_DE_MEL", "TRUFA"]},
    {"machine_id": 16, "machine_name": "Embaladora Flow Pack Rodopac", "location": "Estoque", "skus": ["PAO_DE_MEL", "TRUFA"]},
    {"machine_id": 18, "machine_name": "Dosadora Volumétrica", "location": "Cozinha", "skus": ["TRUFA"]},
    {"machine_id": 19, "machine_name": "Dosadora Linear com Esteira", "location": "Cozinha", "skus": ["TRUFA"]},
    {"machine_id": 22, "machine_name": "Túnel de Resfriamento", "location": "Cozinha", "skus": ["PAO_DE_MEL", "TRUFA"]},
    {"machine_id": 23, "machine_name": "Formadora e Cortadora de Massas", "location": "Cozinha", "skus": ["PAO_DE_MEL"]},
    {"machine_id": 24, "machine_name": "Extrusora de Massas", "location": "Cozinha", "skus": ["PAO_DE_MEL"]},
    {"machine_id": 25, "machine_name": "Dosadora One Shot Pirog", "location": "Cozinha", "skus": ["TRUFA"]},
    {"machine_id": 26, "machine_name": "Moedor/Triturador de Sólidos", "location": "Estoque", "skus": ["PAO_DE_MEL", "TRUFA"]},
    {"machine_id": 27, "machine_name": "Guilhotina ENGEMAQ", "location": "Estoque", "skus": ["PAO_DE_MEL", "TRUFA"]},
    {"machine_id": 28, "machine_name": "Forno Industrial a Gás", "location": "Cozinha", "skus": ["PAO_DE_MEL", "TRUFA"]},
]


records = []

start_date = date(2025, 1, 1)
end_date = date(2026, 4, 14)

for machine in production_machines:
    for sku in machine["skus"]:
        current_date = start_date
        while current_date <= end_date:
            # generate record here

            if sku == "TRUFA":
                units = random.randrange(100, 401)
            else:
                units = random.randrange(200, 801)

            shift = random.choice(
                ["Manhã", "Tarde", "Noite"]
            )
            records.append({
            "machine_id": machine["machine_id"],
            "machine_name": machine["machine_name"],
            "location": machine["location"],
            'sku': sku,
            "units_produced": units,
            "production_date": current_date,
            "shifted": shift,
            })

            current_date += timedelta(days=1)
df = pd.DataFrame(records)

df.to_excel("./data/raw/bronze_production_plan.xlsx", index=False)