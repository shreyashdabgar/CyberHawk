"""we write every genral code here like()"""

import os,sys
from netwoksecurity.logging.logger import logging
from netwoksecurity.exception.exception import CustomException
import pickle 
import yaml
import pandas as pd 

"""yaml.safe_load() reads a YAML file or string and converts
 it into a Python dictionary (or list, depending on the YAML structure)."""

'''in our data_schema(schma.yaml) file our schema store as dict thats why use this function yaml.safe_load()'''

def write_yaml_file(file_path : str, content : object , replace : bool = False)-> None:
    try :
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok = True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
            
    except Exception as e :
        raise CustomException(e)
       
def read_yaml_file(file_path : str) -> dict:
    try :
        with open(file_path , "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
        
    except Exception as e :
        raise CustomException(e) 
    
@staticmethod
def read(file_path)-> pd.DataFrame:
    try :
        pd.read_csv(file_path) 
    except Exception as e :
        raise CustomException(e)