"""we write every genral code here like()"""

import os,sys
from netwoksecurity.logging.logger import logging
from netwoksecurity.exception.exception import CustomException
import pickle 
import yaml
import pandas as pd 
import numpy as np 
from sklearn.metrics import r2_score 

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
    
def save_numpy_array(file_path : str , array : np.array):
    try :
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open (file_path, "wb") as file :
            np.save(file , array)
    except Exception as e :
        raise CustomException(e) 
    
def save_obj(file_path : str , obj : object ) -> None : 
    try :
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok= True)
        with open(file_path, "wb") as file :
            pickle.dump(obj, file) 
    except Exception as e :
        raise CustomException(e)
    
def load_obj(file_path : str ) -> object :
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"file not found at {file_path}")
        with open(file_path, "rb")as file:
            return pickle.load(file) 
    except Exception as e :
        raise CustomException(e)
    
def load_numpy_array(file_path : str) -> np.array:
    try :
        if os.path.exists(file_path) == False:
            raise FileNotFoundError(f"file not found at{file_path }")
        with open(file_path, "rb") as file:
            return np.load(file)
    except Exception as e :
        raise CustomException(e)
    

def eveluate_model(x_train, y_train , x_test, y_test , models):
    try:
        report = {} 
        for model_name , model in models.items():
            model.fit(x_train, y_train)
            Y_train_pred = model.predict(x_train)
            y_test_pred = model.predict(x_test)
            train_model_score = r2_score(y_train, Y_train_pred)
            test_model_score = r2_score(y_test, y_test_pred)
            report[model_name] = test_model_score

            print(f"model name :{report}")
            print(f"train model score : {train_model_score}")
            print(f"test model score : {test_model_score}")
        return report 

    except Exception as e :
        raise CustomException(e)
    
    