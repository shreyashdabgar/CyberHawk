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

SAVED_MODEL_DIR = os.path.join("saved_model")


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

'''data transformation dir'''
DATA_TRANASFORMATION_DIR :str = "data_transfromation"
DATA_TRANASFROMATION_TRANSFORMED_DIR :str = "transformed"
DATA_TRANASFROMATION_OBJECT_DIR :str = "transformed_object"
DATA_TRANSFORMATION_OBBJECT_FILE_NAME :str = "preprocesser.pkl"
DATA_TRANSFORMATION_TRAIN_FILE_PATH :str = "train.npy"
DATA_TRANSFORMATION_TEST_FILE_PATH :str = "test.npy"

## this hard coded value is used for knn model imputer 
DATA_TRANSFORMED_IMPUTE_PARAMS :dict = {
    "missing_values":np.nan,
    "n_neighbors":3,
    "weights":"uniform",
}
'''data processing '''
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float = 0.2


'''model trainer dir'''
MODEL_TRAINER_DIR :str = "model_trainer"
MODEL_DIR :str = "model"
MODEL_FILE_NAME= "model.pkl"
EXPECTED_ACCURECY:float = 0.7
MODEL_CONFIG_FILE_PATH = "model_config.yaml"
OVERFITTING_UNDERFITTING_THRESHOLD:float = 0.05
