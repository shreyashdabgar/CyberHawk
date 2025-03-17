from netwoksecurity.components.data_ingestion import Dataingestion
from netwoksecurity.entities.config_entity import dataingestionConfig, trainingpipelineconfig
from netwoksecurity.logging.logger import logging
from netwoksecurity.exception.exception import CustomException

if __name__ == '__main__':
    try:
        trainpipelineconfig = trainingpipelineconfig()
        dataingestionconfig = dataingestionConfig(trainpipelineconfig)
        data_ingestion = Dataingestion(dataingestionconfig)

        logging.info("Initiating data ingestion process...")
        dataingestionArtifact = data_ingestion.intiate_data_ingestion()
        print(dataingestionArtifact)

    except Exception as e:
        raise CustomException(e)
