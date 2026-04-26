import os
from configparser import ConfigParser

def load_config(filename='database.ini', section='postgresql'):
    """
    Reads the database configuration from a .ini file and returns it as a dictionary.
    
    :param filename: Name of the configuration file (default: 'database.ini')
    :param section: The section within the .ini file to read (default: 'postgresql')
    :return: A dictionary containing database connection parameters
    """
    
    # Get the absolute path to the directory where this script is located
    # This ensures the .ini file can be found even if the script is run from another folder
    script_dir = os.path.dirname(os.path.abspath(__file__))
    path_to_ini = os.path.join(script_dir, filename)
    
    # Initialize the parser to handle the .ini file structure
    parser = ConfigParser()
    
    # Verify if the configuration file exists at the specified path
    if not os.path.exists(path_to_ini):
        raise FileNotFoundError(f"The file {path_to_ini} was not found.")

    # Load the configuration file
    parser.read(path_to_ini)

    config = {}
    # Check if the requested section (e.g., [postgresql]) exists in the file
    if parser.has_section(section):
        # Retrieve all key-value pairs from the section
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        # Raise an error if the section is missing
        raise Exception('Section {0} not found in the {1} file'.format(section, path_to_ini))
    
    return config

if __name__ == '__main__':
    # Test block to verify if the config loads correctly when running this file directly
    try:
        config = load_config()
        print("Success! Config loaded:", config)
    except Exception as e:
        print("Error:", e)