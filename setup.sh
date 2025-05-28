# Bootstrap environment (virtualenv, start Postgres)
./setup.sh

# Install Airflow (optional)
pip install apache-airflow

# Initialize Airflow DB & start scheduler & webserver (optional)
export AIRFLOW_HOME=$(pwd)/airflow_home
airflow db init
airflow scheduler &
airflow webserver &