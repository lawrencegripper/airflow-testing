from datetime import timedelta

import airflow
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dagrun_operator import TriggerDagRunOperator
from airflow.contrib.sensors.wasb_sensor import WasbPrefixSensor
from airflow.contrib.hooks.wasb_hook import WasbHook
from azure.storage.blob.models import Blob, BlobPermissions
from airflow.operators.subdag_operator import SubDagOperator
import datetime


from airflow.operators.python_operator import PythonOperator

# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(2),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(days=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    'sla': timedelta(minutes=1),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'trigger_rule': u'all_success'
}

wasb_connection_id = 'wasb_file_upload'
input_container = '222'
output_container = '111'
processing_file_prefix = ''

blob_service = WasbHook(wasb_conn_id=wasb_connection_id)

dag = DAG(
    dag_id='azure_blob_reader',
    default_args=default_args,
    description='A dag to pull new images from blob and process them',
    schedule_interval=timedelta(days=1),
)

new_files = WasbPrefixSensor(
    task_id='new_files_sensor',
    container_name=input_container,
    prefix=processing_file_prefix,
    wasb_conn_id=wasb_connection_id,
    dag=dag,
)


def move_blobs_to_processing(**context):
    results = blob_service.connection.list_blobs(
        input_container, processing_file_prefix)
    blobs_moved = 0
    blob_urls = []
    for blob in results:
        print("\t Blob name: " + blob.name)
        # Generate a SAS token for blob access
        blob_input_url = blob_service.connection.make_blob_url(
            input_container,
            blob.name,
            sas_token=blob_service.connection.generate_blob_shared_access_signature(
                input_container,
                blob.name,
                permission=BlobPermissions(read=True),
                expiry=datetime.datetime.utcnow() + datetime.timedelta(days=5)))

        print("\t SAS URL:{}".format(blob_input_url))
        # Copy blob to processing bucket
        blob_service.connection.copy_blob(
            output_container, blob.name, blob_input_url, requires_sync=True)

        # Generate a SAS token the now moved blob for downstream dags
        blob_output_url = blob_service.connection.make_blob_url(
            input_container,
            blob.name,
            sas_token=blob_service.connection.generate_blob_shared_access_signature(
                input_container,
                blob.name,
                permission=BlobPermissions(read=True),
                expiry=datetime.datetime.utcnow() + datetime.timedelta(hours=1)))

        blobs_moved += 1
        blob_urls.append(blob_output_url)

        def trigger_processing_dag(context, dag_run_obj):
            urls = blob_urls
            dag_run_obj.payload = {
                "image_urls": urls,
            }
            return dag_run_obj

        TriggerDagRunOperator(
            task_id="trigger_processing",
            trigger_dag_id="image_processing",
            python_callable=trigger_processing_dag,
            dag=dag
        ).execute(context)

        # Remove existing blob
        blob_service.connection.delete_blob(input_container, blob.name)

    return blob_urls


python_task = PythonOperator(
    task_id='move_blobs',
    python_callable=move_blobs_to_processing,
    dag=dag,
)


new_files >> python_task
