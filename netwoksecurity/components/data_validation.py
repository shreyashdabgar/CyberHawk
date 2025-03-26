import os 
import sys 
from netwoksecurity.entities.config_entity import datavalidationconfig
from netwoksecurity.logging.logger import logging
from netwoksecurity.exception.exception import CustomException
from netwoksecurity.constents.traning_pipeline import *
from netwoksecurity.utills.main_utils.utils import read_yaml_file , write_yaml_file

''' input come from artifact entity.py'''
from netwoksecurity.entities.artifact_entity import dataingestionArtifacts, datavalidationartifacts

"""fro data drift we need to import library calle dscipy k2samp"""
from scipy.stats import ks_2samp


class datavalidation():
    def __init__(self, data_ingestion_artifact : dataingestionArtifacts,
                 data_validation_config : datavalidationconfig):
        
        try :
            logging.info(" started the datavalidation ")
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)

        except Exception as e :
            raise CustomException(e)
        
        '''create a static mathod becuse we define reading function and it use onle one and it genral use '''
    @staticmethod
    def read(file_path)-> pd.DataFrame:
        try :
           return pd.read_csv(file_path) 
        except Exception as e :
            raise CustomException(e)
    
    def validate_number_of_columns(self, dataframe : pd.DataFrame)-> bool:
        try :
            logging.info("checking the validate number of columns")
            number_of_columns = len(self.schema_config)

            '''check the num of columns between dataframe and number_of_columns '''
            if number_of_columns ==len(dataframe.columns):
                return True
            else:
                return False
            

        except Exception as e :
            raise CustomException(e)
        
    def data_drift(self, base_df , current_df, threshold = 0.05)-> bool:
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_sample_dist  = ks_2samp(d1,d2)
                if threshold <= is_sample_dist.pvalue:
                    is_found = False
                else :
                    is_found = True
                    status = False
                    report.update({
                        column : {"p_value" : float(is_sample_dist.pvalue),
                                  "drift_status": is_found}
                    })
               
            
            # creating directory for drift report
            
            drift_reoport_file_path  = self.data_validation_config.drift_report_file_path
            dir_path = os.path.dirname(drift_reoport_file_path)
            os.makedirs(dir_path, exist_ok=True)
            # write the report in yaml file
            write_yaml_file(file_path=drift_reoport_file_path , content=report)



        except Exception as e :
            raise CustomException (e)

    def intiate_datavalidation(self) -> datavalidationartifacts:
        '''the return type of these function is datavalidationartifacts'''
        try:
            '''take input from data_ingestion_artifact'''
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            # read the data from train and test 
            train_dataframe = datavalidation.read(train_file_path)
            test_dataframe = datavalidation.read(test_file_path)

            # validate columns 
            status  = self.validate_number_of_columns(dataframe=train_dataframe)
            if status == False:
                error_massage = f"train datafarme does not contain all columns"
            
            status = self.validate_number_of_columns(dataframe=test_dataframe)
            if status == False:
                error_massage= f"test datafarme does not contain all columns"
                
            # lets chck data drift 
            status  = self.data_drift(base_df  = train_dataframe, current_df = test_dataframe)
            '''if status is true then we have to valid_train_file_path, valid_test_file_path'''
            dir_path  = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path, exist_ok=True)

            train_dataframe.to_csv(
                self.data_validation_config.valid_train_file_path 
            )

            test_dataframe.to_csv(
                self.data_validation_config.valid_test_file_path 
            )

            #preparing the data validation artifact
            data_validation_artifact = datavalidationartifacts(
                validation_status  = status,  
                valid_train_file_path = self.data_validation_config.valid_train_file_path,
                valid_test_file_path = self.data_validation_config.valid_test_file_path,
                invalid_train_file_path = None,
                invalid_test_file_path = None,
                drift_report_file_path = self.data_validation_config.drift_report_file_path

            )
            return data_validation_artifact
            
            '''if you want ot print the data in the terminal so you have top return the data''' 
        except Exception as e:
            raise CustomException(e)
