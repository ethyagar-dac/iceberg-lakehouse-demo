"""Monthly NYC taxi pipeline: download -> load into Iceberg -> quality check."""

from datetime import datetime, timedelta

from airflow.sdk import dag, task


@dag(
    dag_id="taxi_monthly",
    schedule="@monthly",
    start_date=datetime(2024, 11, 1),
    end_date=datetime(2025, 1, 31),  # demo scope: 3 months
    catchup=True,  # create a run for each past month (Airflow 3 default is False)
    max_active_runs=1,  # run months in order: schema evolution is chronological
    default_args={"retries": 2, "retry_delay": timedelta(minutes=1)},
    tags=["iceberg", "portfolio"],
)
def taxi_monthly():
    # Imports are inside the tasks so the scheduler can parse this file quickly,
    # without loading pyiceberg/pyarrow every time it scans the dags folder.

    @task
    def download(month: str) -> str:
        from taxi.download import download as run

        run(month)
        return month

    @task
    def load(month: str) -> str:
        from taxi.load import load as run

        run(month)
        return month

    @task
    def quality_check(month: str) -> None:
        from taxi.quality import check

        check(month)

    # "{{ ds[:7] }}" is filled in per run: the run's date, e.g. 2024-11-01, trimmed to 2024-11.
    quality_check(load(download("{{ ds[:7] }}")))


taxi_monthly()
