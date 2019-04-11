#!/bin/bash
set -e

# Setup env
source venv/bin/activate
source ./env_shared.sh
source ./env_setup.private.sh

# # Test it loads
python ./dags/$DAG.py

# # List tree
airflow list_tasks $DAG --tree

# # Test print file found
airflow test $DAG $TASK 2015-06-01

