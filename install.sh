#!/bin/bash
set -e

# Setup env
source ./env_shared.sh
source ./env_setup.private.sh

# install ubuntu deps
sudo apt install default-libmysqlclient-dev

virtualenv --python=python3 venv
source venv/bin/activate

# By default one of Airflow's dependencies installs a GPL dependency (unidecode).
# To avoid this dependency set SLUGIFY_USES_TEXT_UNIDECODE=yes in your environment when you install or upgrade Airflow. 
# To force installing the GPL version set AIRFLOW_GPL_UNIDECODE
export SLUGIFY_USES_TEXT_UNIDECODE=yes
pip install apache-airflow[postgres]
# Add blob dependency 
pip install azure-storage-blob
pip install azure-cognitiveservices-vision-computervision

# initialize the database
airflow initdb