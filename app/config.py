from dotenv import load_dotenv
import os

load_dotenv()

DB_NAME = os.getenv('POSTGRES_DB_NAME')
DB_PORT = os.getenv('POSTGRESS_DB_HOST_PORT')
DB_USER = os.getenv('POSTGRESS_DB_USER')
DB_PASSWORD = os.getenv('POSTGRESS_DB_PASSWORD')
DB_HOST = os.getenv('POSTGRES_DB_HOST')

main_logger_path = os.getenv('MAIN_LOG_FILE_PATH')
metric_logger_path = os.getenv('METRICS_LOG_FILE_PATH')

