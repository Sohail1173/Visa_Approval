import sys,os
from Visa_Approval.components.data_ingestion import DataIngestion
from Visa_Approval.entity.config import DataIngestionConfig
from Visa_Approval.entity.artifacts import DataIngestionArtifact
from Visa_Approval.logger import logging
from Visa_Approval.Exception import USvisaException

class TrainPipeline:

    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
       

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
        

    def run_pipeline(self)->None:
        try:
            data_ingestion_artifact = self.start_data_ingestion()
        except Exception as e:
            raise USvisaException(e,sys)