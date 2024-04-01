import sys,os
from Visa_Approval.components.data_ingestion import DataIngestion
from Visa_Approval.components.data_validation import DataValidation
from Visa_Approval.components.model_trainer import ModelTrainer
from Visa_Approval.entity.config import (DataIngestionConfig,DataValidationConfig,
                                         DataTransformationConfig,
                                         ModelTrainerConfig)
from Visa_Approval.entity.artifacts import (DataIngestionArtifact,DataValidationArtifact,
                                            DataTransformationArtifact,
                                            ModelTrainerArtifact)
from Visa_Approval.components.data_transformation import DataTransformation
from Visa_Approval.logger import logging
from Visa_Approval.Exception import USvisaException

class TrainPipeline:

    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        self.data_transformation_config = DataTransformationConfig()
        self.model_trainer_config=ModelTrainerConfig()


    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            logging.info("Enter the start_data_ingestion method for training pipeline")
            logging.info("Getting data from gdrive")
            data_ingestion=DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
            logging.info("Exited the start_data_ingestion method of TrainPipeline class")
            return data_ingestion_artifact
        except Exception as e:
            raise USvisaException(e,sys)
        
    

    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact)->DataValidationArtifact:
        
        logging.info("Entered the start_data_validation method of TrainPipeline class")
        try:
            data_validation=DataValidation(data_ingestion_artifact=data_ingestion_artifact,
                                           data_validation_config=self.data_validation_config)
            
            data_validation_artifact=data_validation.initiate_data_validation()
            logging.info("Perfored data validation")
            logging.info("Exited the start_data_validation method of TrainPipeline class")
            return data_validation_artifact
        except Exception as e:
            raise USvisaException(e,sys)
        

    def start_data_transformation(self,data_ingestion_artifact:DataIngestionArtifact,
                                  data_validation_artifact:DataValidationArtifact)->DataTransformationArtifact:
        try:
            data_transformation=DataTransformation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_transformation_config=self.data_transformation_config,
                data_validation_artifact=data_validation_artifact,
            )

            data_transformation_artifact=data_transformation.initiate_data_transformation()
            return data_transformation_artifact
        except Exception as e:
            raise USvisaException(e,sys)
        


    def start_model_trainer(self,data_transformation_artifact:DataTransformationArtifact) ->ModelTrainerArtifact:

        try:
            model_trainer=ModelTrainer(data_transformation_artifact=data_transformation_artifact,
                                      model_trainer_config=self.model_trainer_config )

            model_trainer_artifact=model_trainer.initiate_model_trainer()
            return model_trainer_artifact
        except Exception as e:
            raise USvisaException(e,sys)
    def run_pipeline(self)->None:
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact=self.start_data_transformation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_artifact=data_validation_artifact
            )
            model_trainer_artifact=self.start_model_trainer(
                data_transformation_artifact=data_transformation_artifact
            )
        
        except Exception as e:
            raise USvisaException(e,sys)