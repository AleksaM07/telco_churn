
# Telco Churn Prediction Pipeline  
  
This project provides an end-to-end pipeline for predicting customer churn using real-world-like Telco data. It integrates:  
  

 - ETL processing     
 - Model training    
 - Model serving via FastAPI  
 - Workflow orchestration with Apache Airflow  
 - Basic testing to ensure pipeline reliability

  
# Getting Started  
## Requirements  
-Docker & Docker Compose  
  
-Bash (for piperun.sh)  
## Setup & Run  
1. **Clone the repository**  

>     git clone https://github.com/AleksaM07/telco_churn.git  
>     cd telco_churn_etl

  

2. **Configure environment:**

  

    *Copy the example .env file:*    
> cp env.example .env`

  
3.**Run everything via script:**  
  

> `./run_pipeline.sh`

  

 - This script:

  

     - Builds containers
     - Runs ETL unit tests
     - Waits for the FastAPI app to start
     - Sends a test prediction request to confirm it’s working
     - Leaves the terminal open for review

  
**TestingUnit tests in tests/test_etl.py verify the data transformation logic to ensure that:**  
  
I

 - Input data is correctly cleaned and encoded
 - No unexpected values cause downstream issues
 - The pipeline runs as expected before the model is used
 - These tests run automatically inside the Docker container during the
   script.

  
**API AccessOnce the pipeline is running, you can explore and test the API directly from your browser:**  
  
📍 http://127.0.0.1:8000/docs#/default/predict_predict_post  
The /predict endpoint expects Telco customer attributes and returns a prediction on whether the customer is likely to churn.  
  
**Airflow DAGWorkflow orchestration is handled using Apache Airflow. Visit the Airflow UI to monitor or trigger DAG runs manually:**  
  
🌐 http://localhost:8080/dags/churn_pipeline/grid  
*The DAG includes:*  
  

 - Ingesting raw data
 - Running transformation logic
 - Storing the processed dataset
 - Triggering model inference (optional extension)

  
ModelThe model is trained using LightGBMClassifier, serialized with pickle, and served via FastAPI. The saved model is successfully loaded and used in the container environment, with all preprocessing steps applied consistently.  
  
Notesenv.example: Provided for environment variable structure, though .env is not strictly needed in this version.  
  
Makefile: Included for completeness, even though the project uses Airflow for orchestration instead of make.  
 

## ResultWhen you run the pipeline via ./piperun.sh, you'll get:

**  
  
Test results from the ETL unit tests  
  
A sample churn prediction request sent to the API  
  
Visibility into the pipeline through the Airflow web UI  
  
A working FastAPI service that you can interact with or extend  
  
*Done!You're ready to build on this or deploy it in production.  
Churn insights = unlocked.* 
  
  
  
  
## Pipeline Flow Diagram  
  
```text  
+-----------------------------+  
| Telco CSV (raw data)        |  
| data/raw/*.csv              |  
+-------------┬---------------+  
 │ ▼+-----------------------------+  
| Step 2: Load to Postgres    |  
| etl/load_raw.py             |  
+-------------┬---------------+  
 │ ▼+-----------------------------+  
| Step 3: Export to Parquet   |  
| etl/export_parquet.py       |  
+-------------┬---------------+  
 │ ▼+-----------------------------+  
| Step 4: Train Model         |  
| model/train_model.py        |  
+-------------┬---------------+  
 │ ▼+-----------------------------+  
| Step 5: Serve via API       |  
| api/main.py (FastAPI)       |  
+-------------▲---------------+  
 │+-----------------------------+  
| Step 6: Orchestrate All     |  
| Airflow DAG+run_pipeline.sh |  
+-----------------------------+