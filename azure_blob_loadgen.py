from datetime import timedelta, datetime
import airflow
from airflow import DAG
from airflow.operators.dagrun_operator import TriggerDagRunOperator
from airflow.contrib.sensors.wasb_sensor import WasbPrefixSensor
from airflow.contrib.hooks.wasb_hook import WasbHook
from azure.storage.blob.models import BlobPermissions
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.subdag_operator import SubDagOperator

args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(2),
}

dag = DAG(
    dag_id="azure_blob_loadgen",
    default_args=args,
    schedule_interval="@once",
)

start = DummyOperator(
    task_id='start',
    default_args=args,
    dag=dag,
)


def trigger_processing_dag(context, dag_run_obj):
    # Trigger with test image
    dag_run_obj.payload = {
        "image_url": "https://lgairflowinput.blob.core.windows.net/222/json.png?st=2019-04-12T10%3A22%3A00Z&se=2019-04-15T15%3A22%3A00Z&sp=rl&sv=2018-03-28&sr=b&sig=N3MJg%2Fge9S8sxgaDH962Jnqcffd%2BYWVvgY7vGZmAwGw%3D",
    }
    return dag_run_obj


for x in range(0, 10):
    trigger_processing = TriggerDagRunOperator(
        task_id="trigger_processing_{}".format(x),
        trigger_dag_id="image_processing",
        python_callable=trigger_processing_dag,
        dag=dag
    )
    start.set_downstream(trigger_processing)
