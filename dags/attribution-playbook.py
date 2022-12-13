"""
## Attribution Playbook DAG
[Attribution Playbook](https://github.com/dbt-labs/attribution-playbook) is a working dbt project demonstrating how to
model customer attribution. This dbt project originates from dbt labs as an example project with dummy data to
demonstrate a working dbt core project. This DAG uses the dbt parser stored in `/include/utils/dbt_dag_parser.py` to
parse this project (from dbt's [manifest.json](https://docs.getdbt.com/reference/artifacts/manifest-json) file) and
dynamically create Airflow tasks and dependencies.

"""

from pendulum import datetime

from airflow import DAG
from airflow.datasets import Dataset
from airflow.utils.task_group import TaskGroup
from cosmos.providers.dbt.core.operators import DBTSeedOperator, DBTRunOperator, DBTTestOperator


with DAG(
    dag_id="attribution-playbook",
    start_date=datetime(2022, 11, 27),
    schedule=[Dataset("DAG://EXTRACT_DAG")],
    doc_md=__doc__,
    catchup=False,
    default_args={
        "owner": "02-TRANSFORM"
    }
) as dag:

    # We're using the dbt seed command here to populate the database for the purpose of this demo
    seed = DBTSeedOperator(
        task_id="dbt_seed",
        project_dir=f"/usr/local/airflow/dbt/attribution-playbook",
        schema="public",
        conn_id="airflow_db"
    )

    run = DBTRunOperator(
        task_id="dbt_run",
        project_dir="/usr/local/airflow/dbt/attribution-playbook",
        schema="public",
        conn_id="airflow_db"
    )

    test = DBTTestOperator(
        task_id="dbt_test",
        project_dir="/usr/local/airflow/dbt/attribution-playbook",
        schema="public",
        conn_id="airflow_db"
    )

    # with TaskGroup(group_id="dbt") as dbt:
    #     dag_parser = DbtProjectParser(
    #         dbt_project="attribution-playbook",
    #         schema="public",
    #         conn_id="airflow_db"
    #     )

    seed >> run >> test
