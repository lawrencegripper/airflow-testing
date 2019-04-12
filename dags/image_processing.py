from datetime import timedelta

import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from cognitive_services_hook import CognitiveServicesHook

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
    'retry_delay': timedelta(minutes=5),
    'sla': timedelta(minutes=1),
}

dag = DAG(
    dag_id='image_processing',
    default_args=default_args,
    description='Process images',
)

cog_hook = CognitiveServicesHook(conn_id="cog_services_ocr")


def cognitive_text_lookup(ds, **kwargs):
    image_sas_url = kwargs['dag_run'].conf['image_url']
    print("Submitting image image {}".format(image_sas_url))

    result = cog_hook.recognize_printed_text(image_sas_url)

    print("Found {} regions".format(len(result.regions)))
    print("Found lines in region 0")

    for region in result.regions:
        print("Recognized:\n")
        for line in region.lines:
            line_text = " ".join([word.text for word in line.words])
            print(line_text)


cognitive_text = PythonOperator(
    task_id='start',
    provide_context=True,
    python_callable=cognitive_text_lookup,
    dag=dag,
)
