"""1 step of data ingestion is define dataset from mongodb(database)
2. step of data ingestion is save data into feature store 
3. step of split data into train test split 
4. step is to save train test split """


import os 
import sys 
import pandas as pd 
from netwoksecurity.exception.exception import CustomException
from netwoksecurity.logging.logger import logging

# config of dataingestion config 
from netwoksecurity.constents.traning_pipeline import *
from netwoksecurity.entities.config_entity import dataingestionConfig
from netwoksecurity.entities.artifact_entity import dataingestionArtifacts

import pymongo
from typing import List
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

class Dataingestion():
    def __init__(self,data_ingestion_config : dataingestionConfig):
        try :
            # we take (dataingestionConfig)class in dataingestion_config varaible
            self.dataingestion_config = data_ingestion_config
        except Exception as e :
            raise CustomException(e)
    
    def convert_database_collection_as_dataframe(self):
        """ read data from database(MongoDB)"""

        try :
            database_name = self.dataingestion_config.database_name
            collection_name = self.dataingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection = self.mongo_client[database_name][collection_name]

            # covert database to dataframe
            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis = 1)
                df.replace({"na": np.nan}, inplace=True)
            return df

        except Exception as e :
            raise CustomException(e)
        

    def export_data_into_feture_store(self, dataframe: pd.DataFrame):
        try :
            feture_store_file_path = self.dataingestion_config.fetaure_store_file_path
            '''cretaing folder '''
            dir_path = os.path.dirname(feture_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feture_store_file_path, index = False , header= True )
            return dataframe

        except Exception as e:
            raise CustomException(e)
        
    def split_train_test(self, dataframe:pd.DataFrame):
        try :
            train_set, test_set = train_test_split(
                dataframe, test_size= self.dataingestion_config.train_test_split_ratio
                )
            logging.info("split data into train_test split")
            dir_path = os.path.dirname(self.dataingestion_config.training_file_path)
            os.makedirs(dir_path ,exist_ok= True)

            logging.info("completed train test split function")

            # saving train test split into ingested folder
            train_set.to_csv(self.dataingestion_config.training_file_path,index = False, header = True)
            test_set.to_csv(self.dataingestion_config.test_file_path, index = False, header = True)
            logging.info("succesfully saved tran and test data csv into ingested(training_file_path, test_file_path) folder ")

        except Exception as e :
            raise CustomException(e)

    def intiate_data_ingestion(self):
        try :
            dataframe = self.convert_database_collection_as_dataframe()
            dataframe = self.export_data_into_feture_store(dataframe)
            self.split_train_test(dataframe)
            '''here we define that what we want to ake as output according to (main.py)'''
            dataingestionArtifact = dataingestionArtifacts(trained_file_path=self.dataingestion_config.training_file_path,
                                                           test_file_path=self.dataingestion_config.test_file_path)
            
            logging.info("data ingestion task is succesfully done")
            return dataingestionArtifact
            
        except Exception as e:
            raise CustomException(e)
        
    