FROM quay.io/astronomer/astro-runtime:6.0.4
ENV AIRFLOW__CORE__ENABLE_XCOM_PICKLING=true

# Set a default root directory for dbt projects
ARG DBT_DIR_DEFAULT="/usr/local/airflow/dbt"
ENV DBT_DIR=$DBT_DIR_DEFAULT
ENV DBT_PROFILES_DIR=$DBT_DIR_DEFAULT

# Create a venv for DBT and generate manifest.json files for each model
USER root
WORKDIR ${DBT_DIR}
RUN python -m virtualenv dbt_venv && source dbt_venv/bin/activate && \
    pip install --no-cache-dir dbt-core==1.3.1 && \
    pip install --no-cache-dir dbt-postgres==1.3.1 && \
    dbt ls --project-dir ./jaffle_shop && \
    dbt ls --project-dir ./attribution-playbook && \
    dbt deps --project-dir ./mrr-playbook && \
    dbt ls --project-dir ./mrr-playbook && deactivate

# Grant access to the dbt project directory for everyone
RUN chmod -R 777 ${DBT_DIR}

# Create an alias for dbt commands so we don't have to activate every time
RUN echo -e '#!/bin/bash' > /usr/bin/dbt && \
    echo -e "source $DBT_DIR/dbt_venv/bin/activate && dbt \$@" >> /usr/bin/dbt && \
    chmod +x /usr/bin/dbt

# reset working directory
WORKDIR "/usr/local/airflow"
USER astro