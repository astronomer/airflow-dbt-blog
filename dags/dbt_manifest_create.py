"""
### dbt Manifest Create DAG
This DAG can be triggered as needed to re-create the manifest.json for the dbt projects embedded in this environment

### Notes
This DAG uses the `dbt ls` command to generate a manifest.json file to be parsed. You can read more about the dbt
command [here](https://docs.getdbt.com/reference/commands/list)
"""
import os
from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator
from include.utils.dbt_env import dbt_env_vars

with DAG(
    dag_id="dbt_manifest_create",
    start_date=datetime(2022, 7, 27),
    schedule=None,
    catchup=False,
    max_active_runs=1,
    doc_md=__doc__,
    default_args={
        "owner": "00-PREP"
    }
) as dag:

    for project in ["jaffle_shop", "mrr-playbook", "attribution-playbook"]:
        BashOperator(
            task_id=f"{project}_manifest",
            bash_command=(
                f"dbt deps --project-dir $DBT_DIR/{project} && \
                 dbt ls --project-dir $DBT_DIR/{project}"
            ),
            env=dbt_env_vars
        )