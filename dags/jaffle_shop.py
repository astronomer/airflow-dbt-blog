"""
## Jaffle Shop DAG
[Jaffle Shop](https://github.com/dbt-labs/jaffle_shop) is a fictional eCommerce store. This dbt project originates from
dbt labs as an example project with dummy data to demonstrate a working dbt core project. This DAG uses the dbt parser
stored in `/include/utils/dbt_dag_parser.py` to parse this project (from dbt's
[manifest.json](https://docs.getdbt.com/reference/artifacts/manifest-json) file) and dynamically create Airflow tasks
and dependencies.

"""
from pendulum import datetime

from airflow import DAG
from airflow.datasets import Dataset
from airflow.operators.bash import BashOperator
from include.utils.dbt_dag_parser import DbtDagParser
from include.utils.dbt_env import dbt_env_vars
from airflow.utils.task_group import TaskGroup


with DAG(
    dag_id="jaffle_shop",
    start_date=datetime(2022, 11, 27),
    schedule=[Dataset("DAG://EXTRACT_DAG")],
    doc_md=__doc__,
    catchup=False,
    default_args={
        "owner": "02-TRANSFORM"
    }
) as dag:

    # We're using the dbt seed command here to populate the database for the purpose of this demo
    seed = BashOperator(
        task_id="dbt_seed",
        bash_command=f"dbt seed --project-dir $DBT_DIR/jaffle_shop",
        env=dbt_env_vars
    )

    with TaskGroup(group_id="dbt") as dbt:
        dag_parser = DbtDagParser(
            dbt_project="jaffle_shop",
            dbt_global_cli_flags="--no-write-json"
        )

    seed >> dbt


