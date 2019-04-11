from datetime import timedelta

import airflow
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.contrib.sensors.wasb_sensor import WasbPrefixSensor
from airflow.contrib.hooks.wasb_hook import WasbHook
from azure.storage.blob.models import Blob, BlobPermissions
from airflow.operators.subdag_operator import SubDagOperator
import datetime
from airflow.operators.python_operator import PythonOperator

from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import TextRecognitionMode
from azure.cognitiveservices.vision.computervision.models import TextOperationStatusCodes

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


def cognitive_text_lookup(ds, **kwargs):
    image_sas_url = kwargs['dag_run'].conf['image_url']
    print("Submitting image image {}".format(image_sas_url))

    client = ComputerVisionClient(endpoint="https://uksouth.api.cognitive.microsoft.com/", credentials=CognitiveServicesCredentials("__KEY_HERE__"))
    result = client.recognize_printed_text(image_sas_url, custom_headers=None)

    print("Found {} regions".format(len(result.regions)))
    print("Found lines in region 0")
        
    lines = result.regions[0].lines
    print("Recognized:\n")
    for line in lines:
        line_text = " ".join([word.text for word in line.words])
    print(line_text)

cognitive_text = PythonOperator(
    task_id='cognitive_text',
    provide_context=True,
    python_callable=cognitive_text_lookup,
    dag=dag,
)
