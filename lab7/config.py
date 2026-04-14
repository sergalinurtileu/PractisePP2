import os
from configparser import ConfigParser

def load_config(filename='database.ini', section='postgresql'):
  
    script_dir = os.path.dirname(os.path.abspath(__file__))
    path_to_ini = os.path.join(script_dir, filename)
    
    parser = ConfigParser()
    

    if not os.path.exists(path_to_ini):
        raise FileNotFoundError(f"The file {path_to_ini} was not found.")

    parser.read(path_to_ini)

    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, path_to_ini))
    return config

if __name__ == '__main__':
    try:
        config = load_config()
        print("Success! Config loaded:", config)
    except Exception as e:
        print("Error:", e)