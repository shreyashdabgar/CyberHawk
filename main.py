from netwoksecurity.components.data_ingestion import Dataingestion
from netwoksecurity.components.data_validation import datavalidation
from netwoksecurity.entities.config_entity import dataingestionConfig, trainingpipelineconfig , datavalidationconfig
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

        logging.info("intiating data validation ")
        data_validationconfig = datavalidationconfig(trainpipelineconfig)
        data_validation= datavalidation(dataingestionArtifact , data_validationconfig)
        datavalidationartifact = data_validation.intiate_datavalidation()
        print(datavalidationartifact)
        

    except Exception as e:
        raise CustomException(e)
