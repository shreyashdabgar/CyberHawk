from netwoksecurity.exception.exception import CustomException
from netwoksecurity.logging.logger import logging
from netwoksecurity.utills.main_utils.utils import *
from netwoksecurity.constents.traning_pipeline import *
from netwoksecurity.entities.artifact_entity import data_transform_artifacat, datavalidationartifacts
from netwoksecurity.entities.config_entity import data_transformationconfig

import os 
import sys

#importing required liabraries for data transformation
import pandas as pd 
import numpy as np 
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline


'''1 step is to datataransformation class and it will take two input
2 step is to read the data
3 step is to drop the target column'''

class DataTransfromation():
    def __init__(self,data_validation_artifact : datavalidationartifacts,# input we have to put 
                 data_transformation_config : data_transformationconfig):
        try :
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        
        except Exception as e : 
            raise CustomException(e)
        
    @staticmethod
    def read(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(e)
        
    '''creating data transformation pipeline'''
    def transformation_pipeline(cls) -> Pipeline:
        try:
            logging.info("ceratinng the knn imputer pileine")
            # knn imputer 
            imputer = KNNImputer(
                **DATA_TRANSFORMED_IMPUTE_PARAMS # ** is used to unpack the dictionary
                ) 
            
            processer = Pipeline([("imputer", imputer)])
            return processer
        
        except Exception as e:
            raise CustomException(e)

        
    '''main works starts from here '''
    def intialize_data_transformation(self) -> data_transform_artifacat:# this is output 
        try: 
            logging.info("started the data transformation")

            '''1 step is to read the data '''
            train_df = self.read(self.data_validation_artifact.valid_train_file_path)
            test_df = self.read(self.data_validation_artifact.valid_test_file_path)

            '''2 step is to drop the target column '''
            input_feature_train_df = train_df.drop(columns = [TARGET_COLUM],axis = 1)
            output_train_df = train_df[TARGET_COLUM]
            output_train_df = output_train_df.replace(-1, 0)# replace the -1 with 0

            input_feature_test_df = test_df.drop(columns = [TARGET_COLUM],axis = 1)
            output_test_df = test_df[TARGET_COLUM]
            output_test_df = output_test_df.replace(-1, 0)# replace the -1 with 0

            '''3 impliment the transformation on data '''
            # for train data 
            processer = self.transformation_pipeline()
            tarnsformed_train_data= processer.fit_transform(input_feature_train_df)

            # for test data
            transformed_test_data = processer.transform(input_feature_test_df)

            '''combine both data(train and test)'''
            train_data = np.column_stack((tarnsformed_train_data, np.array(output_train_df)))
            test_data = np.column_stack((transformed_test_data, np.array(output_test_df)))


            # saving data 

            save_numpy_array(file_path= self.data_transformation_config.trasnformed_train_file_path , array=train_data)
            save_numpy_array(file_path = self.data_transformation_config.transformed_test_file_path, array=test_data)
            save_obj(self.data_transformation_config.transformed_object_file_path , obj=processer)

            #saving the proprocesser object in final dir
            save_obj("final_model/preprocesser.pkl", obj=processer)
            
            # preparing artifact (it is creating a path for output storage)
            data_transnformation_artifact = data_transform_artifacat(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.trasnformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )

            return data_transnformation_artifact

        except Exception as e :
            raise CustomException(e)
