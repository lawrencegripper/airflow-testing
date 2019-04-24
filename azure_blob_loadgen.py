from datetime import timedelta, datetime
import airflow
from airflow import DAG
from airflow.operators.dagrun_operator import TriggerDagRunOperator
from airflow.operators.python_operator import PythonOperator

args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(2),
}

dag = DAG(
    dag_id="azure_blob_loadgen",
    default_args=args,
    schedule_interval="@once",
)

image_url = "https://proxy.duckduckgo.com/iu/?u=http%3A%2F%2Fwww.gpwebsolutions-host.co.uk%2F1400%2Ffiles%2F2014%2F02%2Fprescription1.jpg&f=1"

def start_image_processing(**context):
    print("Start load gen")
    for x in range (0, 100):
        def trigger_processing_dag(context, dag_run_obj):
                dag_run_obj.payload = {
                    "image_url": image_url,
                }
                return dag_run_obj

        TriggerDagRunOperator(
            task_id="trigger_processing",
            trigger_dag_id="image_processing",
            python_callable=trigger_processing_dag,
            dag=dag
        ).execute(context)
    print("Finish load gen")
    

python_task = PythonOperator(
    task_id='start',
    python_callable=start_image_processing,
    dag=dag,
)