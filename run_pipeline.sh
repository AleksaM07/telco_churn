#!/bin/bash

echo "Building and starting Docker containers..."
docker-compose up -d --build

echo "Waiting for FastAPI to start..."
sleep 20 #wait for everything to setle in
docker-compose exec fastapi bash -c "cd /opt/airflow && pytest tests/test_etl.py"

echo "Sending test prediction request to API..."
curl -X POST http://127.0.0.1:8000/predict -H "Content-Type: application/json" -d '{"gender": "Female","senior_citizen": 0,"partner": "Yes","dependents": "No","tenure": 12,"phone_service": "Yes","multiple_lines": "No","internet_service": "Fiber optic","online_security": "No","online_backup": "Yes","device_protection": "No","tech_support": "No","streaming_tv": "No","streaming_movies": "No","contract": "Month-to-month","paperless_billing": "Yes","payment_method": "Electronic check","monthly_charges": 75.3,"total_charges": 860.5}'

echo -e "\n Done!"
read -p "Press Enter to exit..."