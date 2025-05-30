FROM apache/airflow:2.9.1

USER root

# Copy requirements to somewhere readable
COPY requirements.txt /tmp/requirements.txt
# RUN apt-get update && apt-get install -y ...
RUN apt-get update && apt-get install -y libgomp1

USER airflow
# Install python packages as airflow user
RUN pip install --no-cache-dir -r /tmp/requirements.txt
USER airflow
