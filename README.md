# Factory Lakehouse

A data lakehouse for a Brazilian confectionery manufacturer — bridging financial projections with operational reality using BigQuery, dbt, and Streamlit.

---

## Business Context

The client is a Brazilian confectionery company producing two product lines: **Pão de Mel** and **Trufa**. Operations span **28 machines** across production, packaging, logistics, and infrastructure categories.

Until this project, financial data lived in Excel spreadsheets (a DFC cash flow sheet and a DRE budget sheet), maintenance was tracked on paper, and there was no mechanism to compare planned costs against actual spending. Management had no visibility into which product line was more profitable, which machines were overdue for maintenance, or whether any cost center was consistently over budget.

This platform consolidates that fragmented data into a single analytics layer, making operational and financial intelligence accessible without spreadsheet gymnastics.

---

## Problem Solved

**The core gap**: the company had financial projections (budgets, planned unit costs) but no reliable way to compare them against what actually happened in the factory.

Specific problems addressed:

- **SKU economics**: no visibility into cost per unit or gross margin per product
- **Equipment risk**: no systematic tracking of which machines were due or overdue for maintenance
- **Budget adherence**: monthly budget by cost center existed, but actual spend was never mapped against it
- **Operational blindspot**: production volumes were estimated, not measured

This project closes those gaps by ingesting real financial data, enriching it with synthetic operational data where real data doesn't exist yet, and surfacing actionable metrics in a dashboard.

---

## Tech Stack

| Layer | Tool | Purpose |
|---|---|---|
| Storage & Compute | Google BigQuery | Cloud data warehouse hosting all three medallion layers |
| Transformation | dbt (Data Build Tool) | SQL-based models with testing and lineage |
| Orchestration | Apache Airflow | Daily pipeline scheduling and retry logic |
| Dashboard | Streamlit | Interactive analytics UI with Plotly charts |
| Data Generation | Python | Synthetic data to fill gaps in real source data |
| Auth | GCP Service Account | BigQuery authentication via JSON credentials |

---

## Architecture: Medallion Layers

```
Excel / CSV / Python generators
           │
           ▼
    ┌─────────────┐
    │   BRONZE    │  Raw ingestion — untouched source data loaded to BigQuery
    │  (9 tables) │  via Python ingestion scripts, WRITE_TRUNCATE on each run
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │   SILVER    │  Cleaned & enriched views — type casting, joins,
    │  (5 views)  │  deduplication, supplier name resolution
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │    GOLD     │  Analytics-ready tables — aggregated, business-logic
    │  (3 tables) │  applied, KPIs calculated, status flags assigned
    └──────┬──────┘
           │
           ▼
    Streamlit Dashboard
```

### Bronze Layer — Raw Ingestion

Nine tables loaded as-is from source files. No transformations applied; data fidelity is preserved for auditability.

| Table | Source |
|---|---|
| `bronze_transactions` | DFC sheet from Brumelli.xlsx (cash flow) |
| `bronze_budget` | DRE sheet from Brumelli.xlsx (budget by cost center) |
| `bronze_equipment` | Inventario.xlsx (machine inventory) |
| `bronze_production_plan` | Synthetic daily production records |
| `bronze_maintenance_logs` | Synthetic maintenance history |
| `bronze_r_produto` | R. Produto sheet (product cost baseline) |
| `bronze_synthetic_sales` | Synthetic monthly sales aggregates |
| `bronze_synthetic_budget` | Synthetic monthly budget by cost center |
| `bronze_synthetic_planned_cost` | Synthetic planned cost per SKU per month |

### Silver Layer — Cleaned Views

Five dbt views that clean, cast, and enrich bronze data. Materialized as views so they always reflect the latest bronze state.

| Model | What it does |
|---|---|
| `silver_transactions` | Converts Excel serial dates, joins supplier lookup to resolve cost centers, flags inflows vs outflows |
| `silver_equipment` | Pass-through of seed equipment master data; 28 machines with type, production line, and service interval |
| `silver_maintenance_logs` | Joins maintenance records with equipment types; adds service interval for predictive maintenance calculations |
| `silver_budget` | Standardizes monthly budget by cost center; normalizes month key to string format |
| `silver_production_plan` | Aggregates daily production to monthly totals; joins planned cost data for both SKUs |

### Gold Layer — Analytics Tables

Three dbt tables materialized with business logic and KPIs applied. These are the tables the dashboard queries directly.

| Model | What it does |
|---|---|
| `gold_budget_vs_actual` | Actual spend vs budget per cost center per month; variance in BRL and %; status flags (green/yellow/red/grey) |
| `gold_cost_per_unit` | Cost per unit, revenue per unit, and gross margin for Pão de Mel and Trufa over 16 months |
| `gold_equipment_status` | Latest maintenance date per machine, next due date, and status: OVERDUE / DUE_SOON / OK |

---

## Project Structure

```
Factory_Lakehouse/
├── dashboard/
│   ├── Home.py                      # Landing page with platform overview
│   ├── config.py                    # BigQuery client setup
│   ├── queries.py                   # Cached query functions (5-min TTL)
│   ├── requirements.txt             # Dashboard Python dependencies
│   └── pages/
│       ├── budget.py                # Budget vs actual page
│       ├── equipment.py             # Equipment maintenance status page
│       └── sku_economics.py         # SKU cost & margin page
├── ingestion/
│   ├── ingest.py                    # Main ingestion script (9 bronze tables)
│   ├── generate_synthetic_budget.py
│   ├── generate_synthetic_maintenance.py
│   ├── generate_synthetic_planned_cost.py
│   ├── generate_synthetic_production.py
│   └── generate_synthetic_sales.py
├── models/
│   ├── sources.yml                  # Bronze source declarations
│   ├── silver/
│   │   ├── schema.yml               # Silver layer tests
│   │   ├── silver_budget.sql
│   │   ├── silver_equipment.sql
│   │   ├── silver_maintenance_logs.sql
│   │   ├── silver_production_plan.sql
│   │   └── silver_transactions.sql
│   └── gold/
│       ├── schema.yml               # Gold layer tests
│       ├── gold_budget_vs_actual.sql
│       ├── gold_cost_per_unit.sql
│       └── gold_equipment_status.sql
├── seeds/
│   ├── seed_equipment_types.csv     # 28 machines with type, line, service interval
│   └── seed_supplier_lookup.csv     # 118 transaction description → supplier mappings
├── airflow/
│   └── factory_pipeline.py          # Daily DAG: ingest → silver → gold
├── dbt_project.yml
└── .env
```

---

## Dashboard Pages

### Home
Platform overview showing live metrics (product lines tracked, cost data points, equipment items, overdue maintenance alerts) and a radar chart of platform coverage. Tabs explain the data lakehouse concept and current data availability status.

### SKU Economics (`/sku_economics`)
Cost and revenue analysis for Pão de Mel and Trufa. Filters by product and month range. Shows:
- Planned units, total planned cost, average cost per unit
- Cost per unit trend line over 16 months
- Gross margin in BRL and percentage

### Equipment Status (`/equipment`)
Maintenance tracking for all 28 machines. Filters by machine type and production line. Shows:
- Status distribution: OVERDUE / DUE_SOON / OK
- Color-coded table with days until next maintenance
- Priority alert panel for overdue machines
- CSV export of full equipment status

### Budget Variance (`/budget`)
Monthly actual spend vs planned budget by cost center. Shows variance in BRL and percentage with status flags (green = under budget, yellow = within 10%, red = over budget).

> **Note**: This page is currently partially blocked — see Known Limitations below.

---

## How to Run Locally

### Prerequisites

- Python 3.10+
- A Google Cloud project with BigQuery enabled
- A GCP service account with BigQuery Data Editor and Job User roles
- dbt Core installed (`pip install dbt-bigquery`)

### Setup

**1. Clone the repository**
```bash
git clone <repo-url>
cd Factory_Lakehouse
```

**2. Create and activate a virtual environment**
```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows
.venv\Scripts\activate
```

**3. Install dashboard dependencies**
```bash
pip install -r dashboard/requirements.txt
```

**4. Configure credentials**

Place your GCP service account JSON file in the project root as `gcp-credentials.json`, then create a `.env` file:
```
GOOGLE_APPLICATION_CREDENTIALS=./gcp-credentials.json
```

**5. Configure dbt profile**

Create or update `~/.dbt/profiles.yml`:
```yaml
factory_lakehouse:
  target: dev
  outputs:
    dev:
      type: bigquery
      method: service-account
      project: your-gcp-project-id
      dataset: factory_lakehouse
      keyfile: /absolute/path/to/gcp-credentials.json
      location: US
      threads: 4
```

### Running the Pipeline

**Generate synthetic data** (if bronze tables are empty):
```bash
python ingestion/generate_synthetic_production.py
python ingestion/generate_synthetic_maintenance.py
python ingestion/generate_synthetic_budget.py
python ingestion/generate_synthetic_sales.py
python ingestion/generate_synthetic_planned_cost.py
```

**Ingest all sources to bronze**:
```bash
python ingestion/ingest.py
```

**Load dbt seeds** (equipment master + supplier lookup):
```bash
dbt seed
```

**Run dbt models** (silver + gold):
```bash
dbt run
```

**Run dbt tests**:
```bash
dbt test
```

**Launch the dashboard**:
```bash
streamlit run dashboard/Home.py
```

The dashboard will be available at `http://localhost:8501`.

### Automated Pipeline (Airflow)

The Airflow DAG at `airflow/factory_pipeline.py` runs the full pipeline daily at 6 AM. It executes ingestion tasks in parallel, then runs dbt silver models, then gold models. Configure with your Airflow instance and GCP connection ID.

---

## Known Limitations

### Budget Variance — Blocked by Source Data Quality

The `gold_budget_vs_actual` model and the Budget Variance dashboard page are partially non-functional. The root cause is in the source Excel transaction data: many transaction descriptions in the DFC sheet lack standardized supplier identifiers, which prevents the `silver_transactions` model from joining them against `seed_supplier_lookup` to assign a cost center.

Without a cost center assignment, those transactions cannot be bucketed into the eight budget categories (Producao, Materia_Prima, RH, etc.), so the actual vs budget comparison is incomplete for affected months.

**Resolution path**: enrich `seed_supplier_lookup.csv` with additional raw string patterns from the source Excel, or apply a fallback category to unmatched transactions. Waiting of future, better data.

### Synthetic Data Dependency

The SKU Economics and Equipment Status pages depend entirely on synthetic data (generated by the Python scripts in `ingestion/`). The underlying business logic is sound, but the absolute numbers are fabricated and should not be used for real financial decisions until replaced with actual production and sales records.

### No Incremental Loads

All bronze ingestion uses `WRITE_TRUNCATE` — every pipeline run reloads the full dataset. For the current data volume (16 months) this is fast and acceptable, but will not scale to multi-year history without switching to incremental load patterns.

---

## Data Coverage

| Dimension | Detail |
|---|---|
| Time range | January 2025 – April 2026 (16 months) |
| Machines | 28 (19 production, 4 packaging, 3 infrastructure, 1 logistics, 1 other) |
| Product lines | 2 (Pão de Mel, Trufa) |
| Cost centers | 8 (Producao, Materia_Prima, RH, Fixas, Marketing, Impostos, Logistica, Manutencao) |
| Supplier mappings | 118 entries in lookup seed |
| dbt models | 8 (5 silver views, 3 gold tables) |
| Dashboard pages | 4 (Home, SKU Economics, Equipment Status, Budget Variance) |

---

## License

See [LICENSE](LICENSE).
