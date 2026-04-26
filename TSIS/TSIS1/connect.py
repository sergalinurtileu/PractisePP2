import psycopg2
from config import load_config

def connect(config=None):
    """ 
    Establishes a connection to the PostgreSQL database server.
    
    :param config: A dictionary containing connection parameters. 
                   If None, it loads parameters using load_config().
    :return: A psycopg2 connection object if successful.
    """
    
    # If no configuration is provided, load it from the default source
    if config is None:
        config = load_config()
        
    try:
        # Establish a connection to the PostgreSQL server using unpacked dictionary parameters
        conn = psycopg2.connect(**config)
        print('Connected to the PostgreSQL server.')
        return conn
    
    except (psycopg2.DatabaseError, Exception) as error:
        # Log the error details if the connection fails
        print(f"Error while connecting to PostgreSQL: {error}")
        return None