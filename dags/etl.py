from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.decorators import task
import json
from airflow.utils.dates import days_ago



with DAG(
    dag_id='nasa_apod_postgres',
    start_date=days_ago(1),
    schedule_interval='@daily', 
    catchup=False
) as dag:
    @task
    def create_table():
        postgres_hook = PostgresHook(postgres_conn_id='my_postgres_connection')
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS apod_data (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255),
                explanation TEXT,
                url TEXT,
                date DATE,
                media_type VARCHAR(50)
                )
        '''
        postgres_hook.run(create_table_query)
        
    
   
        #url = ''
    extract_apod = SimpleHttpOperator(
        task_id='extract_apod',
        http_conn_id='nasa_api',
        method='GET',
        endpoint='planetary/apod',
        data={"api_key": "{{conn.nasa_api.extra_dejson.api_key}}"},
        response_filter=lambda response: response.json(),
        # headers={"Content-Type": "application/json"}
        )
       
    
    @task
    def transform_apod_data(response):
        apod_data={
            'title': response.get('title', ''),
            'explanation': response.get('explanation', ''),
            'url': response.get('url', ''),
            'date': response.get('date', ''),   
            'media_type': response.get('media_type', '')
        }
        
        return apod_data
    
    @task
    def load_data_to_postgres(data):
        postgres_hook = PostgresHook(postgres_conn_id='my_postgres_connection')
        insert_query = '''
        
        INSERT INTO apod_data (title, explanation, url, date, media_type)
        values (%s, %s, %s, %s, %s);
        '''
        postgres_hook.run(insert_query, parameters=(data['title'], data['explanation'], data['url'], data['date'], data['media_type']))
        
  
    create_table() >> extract_apod 
    
    api_response = extract_apod.output
    transformed_data = transform_apod_data(api_response)
    load_data_to_postgres(transformed_data)
    