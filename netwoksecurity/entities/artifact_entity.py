from netwoksecurity.logging.logger import logging
from netwoksecurity.exception.exception import CustomException
import os 
import sys 
from dataclasses import dataclass

@dataclass
class dataingestionArtifacts():
    trained_file_path :str
    test_file_path : str 
