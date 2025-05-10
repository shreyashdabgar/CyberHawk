import os
import sys

from netwoksecurity.components.data_ingestion import Dataingestion
from netwoksecurity.components.data_validation import datavalidation
from netwoksecurity.components.data_transformation import DataTransfromation
from netwoksecurity.components.model_trainer import ModelTrainer

from netwoksecurity.exception.exception import CustomException
from netwoksecurity.logging.logger import logging

from netwoksecurity.entities.config_entity import *
from netwoksecurity.entities.artifact_entity import *


class TrainingPipeline:
    def __init__(self):
        self.traninng_pipeline_config = trainingpipelineconfig()

    def start_data_ingestion(self) -> dataingestionArtifacts:
        try :
            logging.info("Strat data ingedstion")
            self.data_ingetsion_config = dataingestionConfig(training_pipeline_config=self.traninng_pipeline_config)
            dataingestion = Dataingestion(data_ingestion_config=self.data_ingetsion_config)
            dataingestion_artifact = dataingestion.intiate_data_ingestion()
            logging.info("data ingestion is done")
            return dataingestion_artifact
        except Exception as e:
            raise CustomException(e)
        
    def start_data_validation(self , dataingestion_artifact: dataingestionArtifacts) -> datavalidationartifacts:
        try :
            logging.info("Start data validation")
            self.data_valiidation_config = datavalidationconfig(training_pipeline_config=self.traninng_pipeline_config)
            data_validation = datavalidation(data_validation_config=self.data_valiidation_config, data_ingestion_artifact=dataingestion_artifact)
            data_validation_artifact = data_validation.intiate_datavalidation()
            logging.info("data validation is done")
            return data_validation_artifact
        
        except Exception as e:
            raise CustomException(e)
        
    def stat_data_transformation(self, data_validation_artifact : datavalidationartifacts) -> data_transform_artifacat:
        try :
            logging.info("Start data tranasformation")
            self.data_transform_config = data_transformationconfig(training_pipeline_config=self.traninng_pipeline_config)
            data_transform = DataTransfromation(data_validation_artifact=data_validation_artifact, data_transformation_config=self.data_transform_config)
            data_transfrom_artifact = data_transform.intialize_data_transformation()
            logging.info("data transformation is done")
            return data_transfrom_artifact
        
        except Exception as e:
            raise CustomException(e)
    
    def start_modes_trainer(self , data_transfrom_artifact : data_transform_artifacat)-> modeltrainingartifacts:
        try :
            logging.info("Strat model trainer")
            self.model_trainer_config = ModelTrainercondfig(training_pipline_config=self.traninng_pipeline_config)
            model_trainer = ModelTrainer(model_trainer_cofig=self.model_trainer_config, data_transformation_artifact=data_transfrom_artifact)
            model_trainer_artifact = model_trainer.intiate_model_trainer()
            logging.info("model trainer is done")
            return model_trainer_artifact
        
        except Exception as e:
            raise CustomException(e)
        
    def run_pipeline(self):
        try :
            logging.info("Pipeline is started")
            data_ingetsion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(dataingestion_artifact=data_ingetsion_artifact)
            data_transfrom_artifact = self.stat_data_transformation(data_validation_artifact=data_validation_artifact)
            model_trainer_artifact = self.start_modes_trainer(data_transfrom_artifact=data_transfrom_artifact)
            logging.info("pipeline is completed")
            return model_trainer_artifact
        
        except Exception as e :
            raise CustomException(e)

