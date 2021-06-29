from datetime import datetime, timedelta
from functools import partial

from airflow import DAG
from airflow.operators.python import PythonOperator

from lib import email, presto

DAG_OWNER = 'sumanth.psv@razorpay.com'

default_args = {
    'owner': DAG_OWNER,
    'start_date': datetime(2021, 6, 2, 9, 30, 0),
    'provide_context': True,
    'on_failure_callback': partial(email.send_mail_slack,
                                   ['shiva.vippa@razorpay.com', 'product.analytics@razorpay.com'], ["datahub"]),
    'retries': 2,
    'retry_delay': timedelta(seconds=300)
}

dag = DAG(
    'Auto_kyc_tat',
    tags=['presto'],
    default_args=default_args,
    schedule_interval='30 9 * * *',
    catchup=False
)

sql1 = """
drop table if exists hive.test.test123;
"""

presto_task1 = PythonOperator(
    task_id='ExecutePrestoQuery1',
    provide_context=True,
    python_callable=presto.execute_presto_query_cli,
    op_kwargs={'query': sql1, 'user': DAG_OWNER},
    dag=dag)

presto_task1