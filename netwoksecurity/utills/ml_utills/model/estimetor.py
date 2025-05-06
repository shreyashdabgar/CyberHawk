from netwoksecurity.constents.traning_pipeline import *

import os 
import sys 

from netwoksecurity.exception.exception import CustomException
from netwoksecurity.logging.logger import logging

class networkmodel():
    def __init__(self,preprocesser ,model):
        try :
            self.preprocesser = preprocesser
            self.model = model 
        except CustomException as e :
            raise CustomException(e)

    def predict(self, x):
        try :
            x_transformed = self.preprocesser.transform(x)
            y_hat = self.model.predict(x_transformed)
            return y_hat
        except CustomException as e :
            raise CustomException(e)