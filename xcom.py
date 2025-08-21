from datetime import datetime
from kubernetes.client import models as k8s
from datetime import datetime
from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from airflow.providers.cncf.kubernetes.operators.job import KubernetesJobOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 8, 1),
    'retries': 0
}

with DAG(
    'spark_submit_example',
    default_args=default_args,
    schedule_interval=None,
    tags=['spark', 'kubernetes']
) as dag:



    submit_spark_cluster = KubernetesPodOperator(
        namespace='default',
        image='apache/spark:3.5.6',
        cmds=['/bin/bash', '-c'],
        service_account_name="airflow",
        arguments=[
            '''echo '{"test_key":"test_value"}' > /airflow/xcom/return.json'''
        ],
        name="spark-submit-cluster",
        task_id="spark_submit_cluster",
        on_finish_action="keep_pod",
        get_logs=True,
        do_xcom_push=True,
        is_delete_operator_pod=False,
        in_cluster=True
    )

    submit_spark_cluster
