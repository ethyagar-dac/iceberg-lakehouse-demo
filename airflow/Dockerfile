# Official Airflow image + the pipeline's Python dependencies.
FROM apache/airflow:3.1.0
COPY requirements.txt /requirements.txt
# Re-pin apache-airflow so installing our packages can't up- or downgrade Airflow itself.
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt