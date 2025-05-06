from netwoksecurity.logging.logger import logging
from netwoksecurity.exception.exception import CustomException
from netwoksecurity.constents.traning_pipeline import *
from netwoksecurity.entities.artifact_entity import *
from netwoksecurity.entities.config_entity import ModelTrainercondfig
from netwoksecurity.utills.main_utils.utils import *
from netwoksecurity.utills.ml_utills.model.estimetor import networkmodel
from netwoksecurity.utills.ml_utills.metric.classification_metric import get_classfiaction_score

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier,AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier


import os 
import sys

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

class ModelTrainer():
    def __init__(self,model_trainer_cofig : ModelTrainercondfig,
            data_transformation_artifact : data_transform_artifacat):
        try :
            self.model_trainer_cofig = model_trainer_cofig
            self.data_transformation_artifact = data_transformation_artifact

        except CustomException as e:
            raise CustomException(e)


    def train_model(self,x_train, y_train, x_test, y_test ) -> object:
        try:
            ml_models_algo = {
                "random_forest" : RandomForestClassifier(),
                "logistic_regression" : LogisticRegression(),
                "decision_tree" : DecisionTreeClassifier(),
                "knn" : KNeighborsClassifier(),
                "gradient_boosting" : GradientBoostingClassifier(),
                "adaboost" : AdaBoostClassifier()
            }

            model_report : dict = eveluate_model(x_train=x_train, y_train=y_train, x_test=x_test, y_test=y_test, models=ml_models_algo)
            
            '''getting the best model as well as its name and score'''
            best_model_score = max(list(model_report.values()))
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
                ] # serch for the best model keys of best model values(which model have best value pick that model acording to index and give the key of the model(name))
            best_model = ml_models_algo[best_model_name]


            best_model.fit(x_train, y_train)
            Y_train_pred = best_model.predict(x_train)
            y_test_pred = best_model.predict(x_test)


            train_score = get_classfiaction_score(y_true=y_train, y_pred=Y_train_pred)
            test_score = get_classfiaction_score(y_true=y_test, y_pred=y_test_pred)
            logging.info(f"train score : {train_score}, test score : {test_score}")
            logging.info(f"best model name : {best_model_name} and best model score : {best_model_score}")

            logging.info(f"model report : {model_report}")


            '''loading exsiting preprocesser object and saving the model'''
            preprocesser = load_obj(self.data_transformation_artifact.transformed_object_file_path)

            model_dir_path = os.path.dirname(self.model_trainer_cofig.model_file_path)
            os.makedirs(model_dir_path, exist_ok=True)

            '''combining both model and preprocessor object and saving them'''
            network_security_model = networkmodel(preprocesser=preprocesser, model=best_model)
            save_obj(file_path = self.model_trainer_cofig.model_file_path, obj=network_security_model)

            model_trainer_artifact = modeltrainingartifacts(trained_model_file_path=self.model_trainer_cofig.model_file_path,
                                   trained_metric_artifact=train_score,
                                   test_metric_artifact=test_score)
            

            return model_trainer_artifact
        
        except Exception as e :
            raise CustomException(e)
        

        
    def intiate_model_trainer(self) -> modeltrainingartifacts : # here wed check that out function return modeltrainingartifacts or not 
        try :

            '''first step is to load the data '''
            train_file = self.data_transformation_artifact.transformed_train_file_path
            test_file = self.data_transformation_artifact.transformed_test_file_path

            #load train and testv pickle file
            train_arr = load_numpy_array(train_file)
            test_arr = load_numpy_array(test_file)

            '''second step is to split data into x and y'''

            x_train = train_arr[: , :-1]
            y_train = train_arr[: , -1]
            x_test = test_arr[: , :-1]
            y_test = test_arr[: , -1]
        
            '''thired step is to put x_train and test and y train and test into teh model trainer'''
            model  = self.train_model(x_train, y_train, x_test, y_test)
            return model 

        except CustomException as e :
            raise CustomException(e)