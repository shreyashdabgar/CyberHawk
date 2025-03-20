from netwoksecurity.logging.logger import logging
from netwoksecurity.exception.exception import CustomException
import os 
import sys 
from dataclasses import dataclass

@dataclass
class dataingestionArtifacts():
    trained_file_path :str
    test_file_path : str 

@dataclass
class datavalidationartifacts():
    validation_status : bool # becuase it gives true and false  
    valid_train_file_path : str
    valid_test_file_path : str 
    invalid_train_file_path : str 
    invalid_test_file_path : str 
    drift_report_file_path : str
