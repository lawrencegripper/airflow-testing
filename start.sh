#!/bin/bash

# Setup connection strings for downstream services
source venv/bin/activate
source ./env_shared.sh
source ./env_setup.private.sh

# start the web server, default port is 8080
airflow webserver -p 8080 &
airflow scheduler 