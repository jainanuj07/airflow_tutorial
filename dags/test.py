from datetime import datetime, timedelta
from functools import partial

from airflow import DAG
from airflow.operators.python import PythonOperator

from lib import email, presto

DAG_OWNER = 'test123'

default_args = {
    'owner': DAG_OWNER,
    'start_date': datetime(2021, 6, 2, 9, 30, 0),
    'provide_context': True,
    'on_failure_callback': partial(email.send_mail_slack,
                                   ['test@gmail.com']),
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

