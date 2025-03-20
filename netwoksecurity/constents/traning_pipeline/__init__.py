import os 
import sys
import numpy as np 
import pandas as pd 


# Data Ingestion related constants

## common costant variable 

TARGET_COLUM = "Result"
PIPELINE_NAME:str = "Networksecurity"
ARTIFACT_DIR:str = "Artifacts"
FILE_NAME:str = "phisingData.csv"

TRAIN_FILE_NAME:str = "train.csv"
TEST_FILE_NAME:str = "test.csv"

SCHEMA_FILE_PATH = os.path.join("data_schema", "schema.yaml")



""" we write this becuase we doesn't have to spacify the path again and agian
we just apply this variable and our work done  """

'''database detail'''
DATA_INGESTION_COLLECTION_NAME:str = "networkdata"
DATA_INGESTION_DATABASE_NAME:str = "DATBASE_AI"

'''data_ingestion dir '''
DATA_INGESTION_DIR_NAME:str = "data_ingestion"
DATA_INGESTION_FETURE_STORE_DATA:str = "feature_store"
DATA_INGESTION_INGESTED_DIR:str = "ingested"

'''data validation dir '''
DATA_VALIDATION_DIR :str = "data_validation"
DATA_VALIDATION_VALID_DIR :str = "validated"
DATA_VALIDATION_INVALID_DIR :str = "invalidated"
DATA_VALIDATION_DRIFT_REPORT_DIR :str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME :str = "report.yml"


'''data processing '''
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float = 0.2
