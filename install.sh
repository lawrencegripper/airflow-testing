#!/bin/bash

virtualenv --python=python3 venv

source venv/bin/activate

# By default one of Airflow's dependencies installs a GPL dependency (unidecode).
# To avoid this dependency set SLUGIFY_USES_TEXT_UNIDECODE=yes in your environment when you install or upgrade Airflow. 
# To force installing the GPL version set AIRFLOW_GPL_UNIDECODE
export SLUGIFY_USES_TEXT_UNIDECODE=yes
python3 -m pip install apache-airflow[celery]

# initialize the database
airflow initdb