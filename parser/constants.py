import os

from dotenv import load_dotenv

load_dotenv()

DB_URI = "mysql+mysqlconnector://{}:{}@{}:{}/{}".format(
    os.getenv('DB_USERNAME', 'root'),
    os.getenv('DB_PASSWORD', ''),
    os.getenv('DB_HOST', 'localhost'),
    os.getenv('DB_PORT', '3306'),
    os.getenv('DB_DATABASE', 'laravel')
)