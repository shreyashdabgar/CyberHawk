from datetime import datetime
import os 
from netwoksecurity.constents.traning_pipeline import *

class trainingpipelineconfig():
    def __init__(self, timestamp = datetime.now()):
        timestamp = timestamp.strftime("%Y%m%d%H%M%S")
        self.pipeline_name = PIPELINE_NAME
        self.artifact_name = ARTIFACT_DIR
        self.artifact_dir = os.path.join(self.artifact_name, timestamp)
        self.timestamp:str = timestamp


## '''we write this code according to finalnetworksecurity.pdf(data ingestion structure)'''
class dataingestionConfig():
    def __init__(self, training_pipeline_config:trainingpipelineconfig):

        self.data_ingestion_dir:str = os.path.join(
            training_pipeline_config.artifact_dir , DATA_INGESTION_DIR_NAME
        )
        self.fetaure_store_file_path:str = os.path.join(
            self.data_ingestion_dir , DATA_INGESTION_FETURE_STORE_DATA , FILE_NAME
        )
        self.training_file_path = os.path.join(
            self.data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TRAIN_FILE_NAME
        )
        self.test_file_path = os.path.join(
            self.data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TEST_FILE_NAME
        )

        ## '''we doesnt have to declare path here becuase it is not file path'''
        self.train_test_split_ratio:float = DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        self.collection_name = DATA_INGESTION_COLLECTION_NAME   
        self.database_name = DATA_INGESTION_DATABASE_NAME


'''create data validation cofig '''
# every config is same but eith minor changes
# here we only join the path we make dir after in the main file components

class datavalidationconfig():
    def __init__(self, training_pipeline_config:trainingpipelineconfig):

        self.data_validation_dir: str = os.path.join(
            training_pipeline_config.artifact_dir , DATA_VALIDATION_DIR
        )

        self.valid_data_dir: str = os.path.join(
            self.data_validation_dir, DATA_VALIDATION_VALID_DIR
        )

        self.invalid_data_dir: str = os.path.join(
            self.data_validation_dir, DATA_VALIDATION_INVALID_DIR
        )

        self.valid_train_file_path: str = os.path.join(
            self.valid_data_dir, TRAIN_FILE_NAME
        )

        self.valid_test_file_path: str = os.path.join(
            self.valid_data_dir, TEST_FILE_NAME
        )

        self.invalid_train_file_path: str = os.path.join(
            self.invalid_data_dir, TRAIN_FILE_NAME
        )

        self.invalid_test_file_path: str = os.path.join(
            self.invalid_data_dir, TEST_FILE_NAME
        )
        self.drift_report_file_path :str = os.path.join(
            self.data_validation_dir, 
            DATA_VALIDATION_DRIFT_REPORT_DIR,
            DATA_VALIDATION_DRIFT_REPORT_FILE_NAME
        )

class data_transformationconfig():
    def __init__(self, training_pipeline_config: trainingpipelineconfig):
        self.data_transformation_dir = os.path.join(training_pipeline_config.artifact_dir,DATA_TRANASFORMATION_DIR
                                                     )
        self.trasnformed_train_file_path = os.path.join(self.data_transformation_dir, DATA_TRANASFROMATION_TRANSFORMED_DIR, DATA_TRANSFORMATION_TRAIN_FILE_PATH
                                                        )
        self.transformed_test_file_path = os.path.join(self.data_transformation_dir, DATA_TRANASFROMATION_TRANSFORMED_DIR, DATA_TRANSFORMATION_TEST_FILE_PATH
                                                       )
        self.transformed_object_file_path = os.path.join(self.data_transformation_dir, DATA_TRANASFROMATION_OBJECT_DIR, DATA_TRANSFORMATION_OBBJECT_FILE_NAME
                                                         )
        
class ModelTrainercondfig():
    def __init__(self, training_pipline_config : trainingpipelineconfig):
        self.model_trainer_dir = os.path.join(
            training_pipline_config.artifact_dir, MODEL_TRAINER_DIR
        )
        self.model_file_path = os.path.join(
            self.model_trainer_dir, MODEL_DIR, MODEL_FILE_NAME
        )
        self.expected_accurecy: float = EXPECTED_ACCURECY
        self.overfitting_underfitting_threshold = OVERFITTING_UNDERFITTING_THRESHOLD
