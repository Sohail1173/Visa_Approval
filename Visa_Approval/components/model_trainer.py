import sys
from typing import Tuple
import pandas as pd
import numpy as np
from pandas import DataFrame
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score,f1_score,precision_score,recall_score
from neuro_mf import ModelFactory

from Visa_Approval.Exception import USvisaException
from Visa_Approval.logger import logging
from Visa_Approval.utils.main_utils import load_numpy_array_data,read_yaml_file,load_object,save_object
from Visa_Approval.entity.config import ModelTrainerConfig
from Visa_Approval.entity.artifacts import DataTransformationArtifact,ModelTrainerArtifact,ClassificationMetricsArtifact
from Visa_Approval.entity.estimator import USvisaModel


class ModelTrainer:
    def __init__(self,data_transformation_artifact:DataTransformationArtifact,
                 model_trainer_config:ModelTrainerConfig):
        self.data_transformation_artifact=data_transformation_artifact
        self.model_trainer_config=model_trainer_config


    def get_model_object_and_report(self,train:np.array,test:np.array)-> Tuple[object,object]:


        try:
            logging.info("Using neuro_mf to get best model object and report")
            model_factors = ModelFactory(model_config_path=self.model_trainer_config.model_config_file_path)
            x_train,y_train,x_test,y_test=train[:,:-1],train[:,-1],test[:,:-1],test[:,-1]
            best_model_details=model_factors.get_best_model(
                X=x_train,y=y_train,base_accuracy=self.model_trainer_config.expected_accuracy
            )
            model_obj=best_model_details.best_model
            y_pred=model_obj.predict(x_test)
            accuracy=accuracy_score(y_test,y_pred)
            f1=f1_score(y_test,y_pred)
            precision=precision_score(y_test,y_pred)
            recall=recall_score(y_test,y_pred)
            metric_artifact=ClassificationMetricsArtifact(f1_score=f1,precision_score=precision,recall_score=recall)
            return best_model_details,metric_artifact
        except Exception as e:
            raise USvisaException(e,sys)
        




    def initiate_model_trainer(self,)->ModelTrainerArtifact:

        logging.info("Entered initiate_model_trainer method of ModelTrainer class")

        try:
            train_arr=load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_file_path)
            test_arr=load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_file_path)

            best_model_details,metric_artifact=self.get_model_object_and_report(train=train_arr,test=test_arr)
            preprocessing_obj=load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)

            if best_model_details.best_score<self.model_trainer_config.expected_accuracy:
                logging.info("No best model found with score more than base score")
                raise Exception("No best model found with score more than base score")
            
            usvisa_model=USvisaModel(preprocessing_object=preprocessing_obj,
                                     trained_model_object=best_model_details.best_model)
            
            logging.info("created usvisa model object with preprocessor and model")
            logging.info("created best model file path")
            save_object(self.model_trainer_config.trained_model_file_path,usvisa_model)

            model_trainer_artifact =ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                metric_artifact=metric_artifact,
            )

            logging.info(f"Model trainer artifact:{model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise USvisaException(e,sys)