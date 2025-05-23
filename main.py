from netwoksecurity.components.data_ingestion import Dataingestion
from netwoksecurity.components.data_validation import datavalidation
from netwoksecurity.components.data_transformation import DataTransfromation
from netwoksecurity.entities.config_entity import *
from netwoksecurity.logging.logger import logging
from netwoksecurity.exception.exception import CustomException
from netwoksecurity.components.model_trainer import ModelTrainer

if __name__ == '__main__':
    try:
        trainpipelineconfig = trainingpipelineconfig()
        dataingestionconfig = dataingestionConfig(trainpipelineconfig)
        data_ingestion = Dataingestion(dataingestionconfig)
        logging.info("Initiating data ingestion process...")
        dataingestionArtifact = data_ingestion.intiate_data_ingestion()
        print(dataingestionArtifact)

        logging.info("intiating data validation ")
        data_validationconfig = datavalidationconfig(trainpipelineconfig)
        data_validation= datavalidation(dataingestionArtifact , data_validationconfig)
        datavalidationartifact = data_validation.intiate_datavalidation()
        print(datavalidationartifact)

        logging.info("intiating data transformation")
        data_tarnsformationconfig = data_transformationconfig(trainpipelineconfig)
        data_tranformation = DataTransfromation(datavalidationartifact, data_tarnsformationconfig)
        data_transform_artifact = data_tranformation.intialize_data_transformation()
        print(data_transform_artifact)
        logging.info("data transformation is done")

        logging.info("intiating model trainer")
        model_trainer_config = ModelTrainercondfig(trainpipelineconfig)
        model_trainer = ModelTrainer(model_trainer_config, data_transform_artifact)
        model_trainer.intiate_model_trainer()
        logging.info("model trainer is done")
        



    except Exception as e:
        raise CustomException(e)
