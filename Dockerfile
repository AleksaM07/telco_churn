FROM apache/airflow:2.9.1

USER root

# Copy requirements to somewhere readable
COPY requirements.txt /tmp/requirements.txt
# Install any OS packages you might need here (optional)
# RUN apt-get update && apt-get install -y ...

# Switch to airflow user (recommended by Airflow image)
USER airflow

# Install python packages as airflow user
RUN pip install --no-cache-dir -r /tmp/requirements.txt \
 && pip install --no-cache-dir dbt-core dbt-duckdb

# Switch back to airflow user if not already (safe)
USER airflow