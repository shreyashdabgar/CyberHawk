import os 
import sys 
import json

from dotenv import load_dotenv
import certifi
import numpy as np
import pandas as pd 
import pymongo
import pymongo.mongo_client
from netwoksecurity.logging.logger import logging
from netwoksecurity.exception.exception import CustomException

MONGO_DB_URL = "mongodb+srv://dabgarshreyash199:shreyash123@cluster0.djd1n.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

load_dotenv()

ca = certifi.where()


class networkdataextrect():
    def __init__(self):
        try :
            pass
        except Exception as e :
            raise CustomException (e)
        
    def dataconverter(self,file_path):
        try :
            '''this function is basically read data from csv 
            drop by defualt index and convert csv to json format and save into variable and return it'''

            data = pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        
        except Exception as e :
            raise CustomException(e)
    
    def insert_data_mongodb(self, records , database, collection):
        try:
            self.records = records
            self.database = database
            self.collection = collection

            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[self.database]

            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)

            return (len(self.records))
        
        except Exception as e :
            raise CustomException(e)
        
if __name__ == '__main__':
    FILE_PATH = "network_data\phisingData.csv"
    DATABASE = "DATBASE_AI"
    collection = "networkdata"

    obj = networkdataextrect()
    records = obj.dataconverter(file_path = FILE_PATH)
    nunmber_of_records = obj.insert_data_mongodb(records, DATABASE, collection)

    print(nunmber_of_records)
