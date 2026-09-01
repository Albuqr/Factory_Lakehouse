from datetime import date, timedelta
import random
import pandas as pd


machines = [
    {"machine_id": 1, "machine_name": "Empilhadeira Semi-Elétrica", "location": "Estoque"},
    {"machine_id": 2, "machine_name": "Moinho/Triturador Industrial", "location": "Cozinha"},
    {"machine_id": 3, "machine_name": "Marcepan Rototurbo RT4", "location": "Cozinha"},
    {"machine_id": 4, "machine_name": "Dosadora de Pão de Mel", "location": "Cozinha"},
    {"machine_id": 5, "machine_name": "Batedeira Industrial Planetária Grande", "location": "Cozinha"},
    {"machine_id": 6, "machine_name": "Tanque Encamisado com Agitador (Chocolate)", "location": "Cozinha"},
    {"machine_id": 7, "machine_name": "Tanque Encamisado com Descarga Inferior", "location": "Estoque"},
    {"machine_id": 8, "machine_name": "Tanque Elétrico com Resistências", "location": "Cozinha"},
    {"machine_id": 9, "machine_name": "Batedeira Planetária Industrial", "location": "Cozinha"},
    {"machine_id": 10, "machine_name": "Tanque SIDMAQ", "location": "Cozinha"},
    {"machine_id": 11, "machine_name": "Embaladora Dupla Torção ICMO", "location": "Estoque"},
    {"machine_id": 12, "machine_name": "Seladora Térmica B-80", "location": "Estoque"},
    {"machine_id": 13, "machine_name": "Tanque Encamisado com Painel Elétrico", "location": "Cozinha"},
    {"machine_id": 14, "machine_name": "Enrobadora de Pão de Mel", "location": "Cozinha"},
    {"machine_id": 15, "machine_name": "Embaladora Flow Pack 1", "location": "Estoque"},
    {"machine_id": 16, "machine_name": "Embaladora Flow Pack Rodopac", "location": "Estoque"},
    {"machine_id": 17, "machine_name": "Conjunto AC LG 1", "location": "Galpão"},
    {"machine_id": 18, "machine_name": "Dosadora Volumétrica", "location": "Cozinha"},
    {"machine_id": 19, "machine_name": "Dosadora Linear com Esteira", "location": "Cozinha"},
    {"machine_id": 20, "machine_name": "Conjunto AC LG 2", "location": "Galpão"},
    {"machine_id": 21, "machine_name": "Conjunto AC LG 3", "location": "Galpão"},
    {"machine_id": 22, "machine_name": "Túnel de Resfriamento", "location": "Cozinha"},
    {"machine_id": 23, "machine_name": "Formadora e Cortadora de Massas", "location": "Cozinha"},
    {"machine_id": 24, "machine_name": "Extrusora de Massas", "location": "Cozinha"},
    {"machine_id": 25, "machine_name": "Dosadora One Shot Pirog", "location": "Cozinha"},
    {"machine_id": 26, "machine_name": "Moedor/Triturador de Sólidos", "location": "Estoque"},
    {"machine_id": 27, "machine_name": "Guilhotina ENGEMAQ", "location": "Estoque"},
    {"machine_id": 28, "machine_name": "Forno Industrial a Gás", "location": "Cozinha"},
]

seed = pd.read_csv("seeds/seed_equipment_types.csv")
interval_lookup = seed.set_index('item_id')['service_interval_days'].to_dict()
records = []

for machine in machines:

        interval = interval_lookup[machine["machine_id"]]
        if interval == 30:
            offset = random.randint(10, 50)
        elif interval == 90:
            offset = random.randint(20, 160)
        else:
            offset = 0
        maintenance_date = date.today() - timedelta(days=offset)

        maintenance_type = random.choices(
            ["Preventiva", "Corretiva"],
            weights=[80, 20]
        )[0]

        technician = random.choice(
            ["Mauro", "Carlos", "Fernanda"]
        )

        records.append({
        "machine_id": machine["machine_id"],
        "machine_name": machine["machine_name"],
        "location": machine["location"],
        'maintenance_type': maintenance_type,
        "technician": technician,
        "maintenance_date": maintenance_date
        })

df = pd.DataFrame(records)

df.to_excel("./data/raw/bronze_maintenance_logs.xlsx", index=False)