# Telco Churn Prediction Pipeline

This project is a complete, end-to-end machine learning pipeline for predicting customer churn using a Telco dataset. It transforms a manual, notebook-based process into a fully automated and reproducible workflow.

---

## Project Structure

telco_churn_etl/
├── README.md # Project description and usage instructions
├── .env.example # Example environment variables (DB config, secrets, etc.)
├── setup.sh # Script to bootstrap Python venv and launch Docker Postgres
├── Makefile # One-command orchestrator to run the whole pipeline
├── docker-compose.yml # Spins up PostgreSQL using Docker
├── requirements.txt # Python package dependencies

├── migrations/
│ └── migrate.sql # SQL script to set up the telco_customer_churn table

├── etl/
│ ├── load_raw.py # Step 2: Load raw CSV into PostgreSQL
│ └── export_parquet.py # Step 3: Export clean data from DB to Parquet

├── model/
│ └── train_model.py # Step 4: Train ML model and save model + metrics

├── api/
│ └── main.py # Step 5: FastAPI app to serve model predictions

├── dags/
│ └── churn_pipeline_dag.py # Step 6*: Optional Airflow DAG for orchestration

├── data/
│ ├── raw/
│ │ └── Telco-Customer-Churn.csv
│ └── processed/ # Optional: Intermediate/staging files

├── outputs/
│ ├── churn_data.parquet # Final analytics-ready Parquet export
│ ├── model.joblib # Trained model artifact
│ └── metrics.json # Model evaluation metrics

└── tests/
└── test_etl.py # Bonus: Simple tests for ETL functionality

---

## Assignment Task Mapping

| Step | Requirement Description                                  | Implementation Files                          |
|------|-----------------------------------------------------------|-----------------------------------------------|
| 0    | Bootstrap environment (venv + Docker Postgres)            | `setup.sh`, `.env.example`, `docker-compose.yml` |
| 1    | DB schema creation (automated)                            | `migrations/migrate.sql`                      |
| 2    | Load CSV into relational DB                               | `etl/load_raw.py`                             |
| 3    | Export DB table to Parquet with correct types             | `etl/export_parquet.py`                       |
| 4    | Train churn-prediction model & save model + metrics       | `model/train_model.py`                        |
| 5    | Serve predictions via REST API                            | `api/main.py`                                 |
| 6*   | Orchestrate steps with Makefile or Airflow (optional)     | `Makefile`, `dags/churn_pipeline_dag.py`      |

---

## Pipeline Flow Diagram

```text
+-----------------------------+
| Telco CSV (raw data)        |
| data/raw/*.csv              |
+-------------┬---------------+
              │
              ▼
+-----------------------------+
| Step 2: Load to Postgres    |
| etl/load_raw.py             |
+-------------┬---------------+
              │
              ▼
+-----------------------------+
| Step 3: Export to Parquet   |
| etl/export_parquet.py       |
+-------------┬---------------+
              │
              ▼
+-----------------------------+
| Step 4: Train Model         |
| model/train_model.py        |
+-------------┬---------------+
              │
              ▼
+-----------------------------+
| Step 5: Serve via API       |
| api/main.py (FastAPI)       |
+-------------▲---------------+
              │
+-----------------------------+
| Step 6*: Orchestrate All    |
| Makefile / Airflow DAG      |
+-----------------------------+