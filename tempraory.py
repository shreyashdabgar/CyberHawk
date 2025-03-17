import os
import sys
import pandas as pd
import numpy as np
import pymongo
from typing import List
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv

from netwoksecurity.exception.exception import CustomException
from netwoksecurity.logging.logger import logging
from netwoksecurity.constents.traning_pipeline import *
from netwoksecurity.entities.config_entity import dataingestionConfig
from netwoksecurity.entities.artifact_entity import dataingestionArtifacts

# Load environment variables
load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self, data_ingestion_config: dataingestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config

            # MongoDB Connection Check
            if not MONGO_DB_URL:
                raise CustomException("MongoDB URL is missing in environment variables.")
            
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            logging.info("Connected to MongoDB successfully.")
        except Exception as e:
            raise CustomException(f"Error during DataIngestion initialization: {e}")
    
    def convert_database_collection_as_dataframe(self):
        """Read data from MongoDB and convert it to a DataFrame"""
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)

            print(f"✅ Connecting to MongoDB: {MONGO_DB_URL}")  # Debugging
            collection = self.mongo_client[database_name][collection_name]

        # Fetch data
            data = list(collection.find())
            print(f"📊 Total Documents Retrieved: {len(data)}")  # Debugging

            if not data:
                raise ValueError("🚨 No data found in MongoDB collection!")

            df = pd.DataFrame(data)

            if "_id" in df.columns:
                df = df.drop(columns=["_id"], axis=1)

            df.replace({"na": np.nan}, inplace=True)
            return df

        except Exception as e:
            raise CustomException(f"Error fetching data from MongoDB: {e}")


            
    
    def export_data_into_feature_store(self, dataframe: pd.DataFrame):
        """Save the dataframe to the feature store."""
        try:
            feature_store_file_path = self.data_ingestion_config.fetaure_store_file_path

            # Ensure directory exists
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)

            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            logging.info(f"Data successfully saved to feature store at: {feature_store_file_path}")

            return dataframe
        except Exception as e:
            raise CustomException(f"Error saving data to feature store: {e}")
    
    def split_train_test(self, dataframe: pd.DataFrame):
        """Split data into training and testing sets and save them."""
        try:
            if dataframe.empty:
                raise CustomException("Dataset is empty. Cannot perform train-test split.")

            train_set, test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio, random_state=42
            )
            logging.info(f"Train-Test split successful. Train shape: {train_set.shape}, Test shape: {test_set.shape}")

            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)

            # Save train and test sets
            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.test_file_path, index=False, header=True)
            logging.info("Train and test data saved successfully.")

        except ValueError as ve:
            raise CustomException(f"Train-Test split error: {ve}")
        except Exception as e:
            raise CustomException(f"Error in split_train_test: {e}")

    def initiate_data_ingestion(self):
        """Main function to run data ingestion steps."""
        try:
            logging.info("Starting Data Ingestion process...")

            dataframe = self.convert_database_collection_as_dataframe()
            dataframe = self.export_data_into_feature_store(dataframe)
            self.split_train_test(dataframe)

            data_ingestion_artifact = dataingestionArtifacts(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.test_file_path,
            )
            logging.info("Data Ingestion process completed successfully.")

            return data_ingestion_artifact
        except Exception as e:
            raise CustomException(f"Error during data ingestion: {e}")
