
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

    submit_spark_client = KubernetesPodOperator(
        namespace='default',
        image='apache/spark:3.5.6_s3',
        cmds=['/bin/bash', '-c'],
        service_account_name="airflow",
        arguments=[
            '/opt/spark/bin/spark-submit '
            '--master k8s://https://kubernetes.default.svc '
            '--deploy-mode client '
            '--name spark-pi '
            '--class org.apache.spark.examples.SparkPi '
            '--conf spark.eventLog.enabled=true '
            '--conf spark.eventLog.dir=s3a://airflow-logs/logs/ '
            '--conf spark.hadoop.fs.s3a.access.key=minio '
            '--conf spark.hadoop.fs.s3a.secret.key=minio123 '
            '--conf spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem '
            '--conf spark.hadoop.fs.s3a.endpoint=http://192.168.80.241:9000 '
            '--conf spark.hadoop.fs.s3a.path.style.access=true '
            '--conf spark.kubernetes.container.image=apache/spark:3.5.6_s3 '
            '--conf spark.driver.host=$(hostname -i) '
            '--conf spark.kubernetes.namespace=default '
            '--conf spark.kubernetes.driver.deleteOnTermination=false '
            '--conf spark.kubernetes.driver.service.deleteOnTermination=false ' 
            '--conf spark.kubernetes.executor.deleteOnTermination=false '
            '--conf spark.kubernetes.authenticate.driver.serviceAccountName=airflow '
            'local:///opt/spark/examples/jars/spark-examples_2.12-3.5.6.jar 1000'
        ],
        name="spark-submit-client",
        task_id="spark_submit_client",
        on_finish_action="keep_pod",
        get_logs=True,
        is_delete_operator_pod=False,
        in_cluster=True,
        env_vars=[
            k8s.V1EnvVar(
                name="POD_IP",
                value_from=k8s.V1EnvVarSource(
                    field_ref=k8s.V1ObjectFieldSelector(field_path="status.podIP")
                ),
            )
        ],
        executor_config={
            "executor": "KubernetesExecutor"  # Explicitly choose CeleryExecutor, KubernetesExecutor
        }
        
    )


    submit_spark_cluster = KubernetesPodOperator(
        namespace='default',
        image='apache/spark:3.5.6',
        cmds=['/bin/bash', '-c'],
        service_account_name="airflow",
        arguments=[
            '/opt/spark/bin/spark-submit '
            '--master k8s://https://kubernetes.default.svc '
            '--deploy-mode cluster '
            '--name spark-pi '
            '--class org.apache.spark.examples.SparkPi '
            '--conf spark.eventLog.enabled=true '
            '--conf spark.eventLog.dir=s3a://airflow-logs/logs/ '
            '--conf spark.hadoop.fs.s3a.access.key=minio '
            '--conf spark.hadoop.fs.s3a.secret.key=minio123 '
            '--conf spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem '
            '--conf spark.hadoop.fs.s3a.endpoint=http://192.168.80.241:9000 '
            '--conf spark.hadoop.fs.s3a.path.style.access=true '
            '--conf spark.kubernetes.container.image=apache/spark:3.5.6_s3 '
            '--conf spark.kubernetes.namespace=default '
            '--conf spark.kubernetes.driver.deleteOnTermination=false '
            '--conf spark.kubernetes.driver.service.deleteOnTermination=false '
            '--conf spark.kubernetes.executor.deleteOnTermination=false '
            '--conf spark.kubernetes.authenticate.driver.serviceAccountName=airflow '
            'local:///opt/spark/examples/jars/spark-examples_2.12-3.5.6.jar '
            '1000' 
        ],
        name="spark-submit-cluster",
        task_id="spark_submit_cluster",
        on_finish_action="keep_pod",
        get_logs=True,
        is_delete_operator_pod=False,
        in_cluster=True
    )


    submit_spark_clustet_job = KubernetesJobOperator(
        namespace='default',
        image='apache/spark:3.5.6',
        cmds=['/bin/bash', '-c'],
        service_account_name="airflow",
        arguments=[
            '/opt/spark/bin/spark-submit '
            '--master k8s://https://kubernetes.default.svc '
            '--deploy-mode cluster '
            '--name spark-pi '
            '--class org.apache.spark.examples.SparkPi '
            '--conf spark.eventLog.enabled=true '
            '--conf spark.eventLog.dir=s3a://airflow-logs '
            '--conf spark.hadoop.fs.s3a.access.key=minio '
            '--conf spark.hadoop.fs.s3a.secret.key=minio123 '
            '--conf spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem '
            '--conf spark.hadoop.fs.s3a.endpoint=http://192.168.80.241:9000 '
            '--conf spark.hadoop.fs.s3a.path.style.access=true '
            '--conf spark.kubernetes.container.image=apache/spark:3.5.6_s3 '
            '--conf spark.kubernetes.namespace=default '
            '--conf spark.kubernetes.driver.deleteOnTermination=false '
            '--conf spark.kubernetes.driver.service.deleteOnTermination=false '
            '--conf spark.kubernetes.executor.deleteOnTermination=false '
            '--conf spark.kubernetes.authenticate.driver.serviceAccountName=airflow '
            'local:///opt/spark/examples/jars/spark-examples_2.12-3.5.6.jar '
            '1000'
        ],
        backoff_limit=0,
        startup_timeout_seconds=300,
        name="spark-submit-cluster-job",
        task_id="submit_spark_clustet_job",
        on_finish_action="keep_pod",
        get_logs=True,
    )

    submit_spark_client >> submit_spark_cluster >> submit_spark_clustet_job
