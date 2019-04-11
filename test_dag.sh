#!/bin/bash
set -e

# Setup env
source venv/bin/activate
source ./env_shared.sh
source ./env_setup.private.sh

# # Test it loads
python ./dags/$DAG_NAME.py

# # List tree
airflow list_tasks $DAG_NAME --tree

# # Test print file found
airflow test $DAG_NAME python_op_file_found 2015-06-01

