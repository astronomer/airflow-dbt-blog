FROM quay.io/astronomer/astro-runtime:7.0.0
ENV AIRFLOW__CORE__ENABLE_XCOM_PICKLING=true

#Installs locally
USER root
COPY /cosmos/ /cosmos
WORKDIR "/usr/local/airflow/cosmos"
RUN pip install -e .

WORKDIR "/usr/local/airflow"

USER astro