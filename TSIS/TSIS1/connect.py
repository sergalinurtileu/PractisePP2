import psycopg2
from config import load_config

def connect(config=None): # Добавили =None
    """ Connect to the PostgreSQL database server """
    if config is None:
        config = load_config() # Если конфиг не пришел, загружаем сами
        
    try:
        # connecting to the PostgreSQL server
        conn = psycopg2.connect(**config)
        print('Connected to the PostgreSQL server.')
        return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)