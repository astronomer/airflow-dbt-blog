FROM quay.io/astronomer/astro-runtime:7.0.0
ENV AIRFLOW__CORE__ENABLE_XCOM_PICKLING=true

# Set a default root directory for dbt projects
ARG DBT_DIR_DEFAULT="/usr/local/airflow/dbt"
ENV DBT_DIR=$DBT_DIR_DEFAULT
ENV DBT_PROFILES_DIR=$DBT_DIR_DEFAULT

# Create a venv for DBT and generate manifest.json files for each model
USER root
RUN python -m virtualenv dbt_venv && source dbt_venv/bin/activate && \
    pip install --no-cache-dir dbt-core==1.3.1 && \
    pip install --no-cache-dir dbt-postgres==1.3.1 && \
    dbt ls --project-dir ${DBT_DIR}/jaffle_shop && \
    dbt ls --project-dir ${DBT_DIR}/attribution-playbook && \
    dbt deps --project-dir ${DBT_DIR}/mrr-playbook && \
    dbt ls --project-dir ${DBT_DIR}/mrr-playbook && deactivate

# Create an alias for dbt commands so we don't have to activate every time
RUN echo -e '#!/bin/bash' > /usr/bin/dbt && \
    echo -e "source /usr/local/airflow/dbt_venv/bin/activate && dbt \$@" >> /usr/bin/dbt

# Copy dbt dir and access grants
COPY dbt ${DBT_DIR}
RUN chmod -R 777 ${DBT_DIR}
RUN chmod -R 777 /usr/bin/dbt

# reset working directory
USER astro