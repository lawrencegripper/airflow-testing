# Airflow Azure Sample

## Azure Blob Sensor `wasb`

[azure_blob_reader.py](./dags/azure_blob_reader.py) demonstrates a simple DAG which will wait on new files to be put in blob with the prefix `new_`. 

### Running

Create a file called `env_setup_private.sh` and use [this utils script](./utils/azblob_connection) to generate a `uri` based connection string for a blob storage account. 

Your `env.setup_private.sh` script should look something like this... 

```
#!/bin/bash
set -e

export AIRFLOW_CONN_WASB_FILE_UPLOAD="wasb://storageaccountname:escapedkeyusingurlencoding@azure"
```

Now you can run `install.sh` to create a virtual env for python and install then initialize an `airflow` server locally.

Running `start.sh` will now run an instance or Airflow, you can [navigate to it's admin console](http://localhost:8080) and enable the DAG `azure_blob_reader`. 

Now drop a file into the container `uploaded` in the blob storage and see the workflow run. 

### Developing 

When editing the `DAG` you can use `DAG_NAME=azure_blob_reader ./test_dag.sh` to check for any python language issues before running in Airflow 