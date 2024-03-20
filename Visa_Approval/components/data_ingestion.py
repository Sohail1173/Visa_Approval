import os
import sys
import pandas as pd
from pandas import  DataFrame
from sklearn.model_selection import train_test_split
from Visa_Approval.entity.config import DataIngestionConfig
from Visa_Approval.entity.artifacts import DataIngestionArtifact
from Visa_Approval.logger import logging
from Visa_Approval.Exception import USvisaException
import gdown
import zipfile
class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig=DataIngestionConfig()):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise USvisaException(e,sys) 
    def download_data(self)->str:

        try:
            dataset_url=self.data_ingestion_config.data_download_url
            print(dataset_url)
            zip_download_dir=self.data_ingestion_config.data_ingestion_dir
            zip_download=self.data_ingestion_config.data_ingestion_zip_dir
            os.makedirs(zip_download_dir,exist_ok=True)
            logging.info(f"downloading data from :{dataset_url} to {zip_download}")
            file_id=dataset_url.split('/')[-2]
            prefix = 'https://drive.google.com/uc?/export=download&id='
            gdown.download(prefix+file_id,zip_download)
            logging.info(f"downloading  zip file name :{zip_download}")
            return zip_download
        except Exception as e:
            raise USvisaException(e,sys)
        
    def extract_zip_file(self,zip_file_path:str)->str:
        try:
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path
            dir_path=os.path.dirname(feature_store_file_path)
            # print(dir_path)
            os.makedirs(dir_path,exist_ok=True)
            with zipfile.ZipFile(zip_file_path,"r") as  zip_ref:
                zip_ref.extractall(dir_path)
            logging.info(f"extracting zip file name :{zip_file_path}")
            dir=self.data_ingestion_config.file_name
            dir_path1=f"{dir_path}\{dir}"
            data_frame=pd.read_csv(dir_path1)
            print(data_frame.shape)
            return data_frame
        except Exception as e:
            raise USvisaException(e,sys)
        
    def split_data_as_train_test(self,csv_path):

        logging.info("Entered split_data_as_train_test method of Data_Ingestion class")
        try:
            train_set,test_set=train_test_split(csv_path,test_size=self.data_ingestion_config.train_test_split_ratio)
            print(train_set.shape)
            print(test_set.shape)
            logging.info("performed train test split on the csv data")
            logging.info("Exited split_data_as_train_test method of Data_ingestion class")
            dir_path=os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok=True)
            logging.info(f"Exporting train and test file path")
            train_set.to_csv(self.data_ingestion_config.training_file_path,index=False,header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path,index=False,header=True)
            logging.info(f"Exited train and test file path")
        except  Exception as e:
            raise USvisaException(e,sys)
        

    def initiate_data_ingestion(self)->DataIngestionArtifact:


        logging.info("Entered initiate_data_ingestion method of Data_ingestion class")

        try:
            zip_file_path=self.download_data()
            feature_store_path=self.extract_zip_file(zip_file_path)
            print(feature_store_path)
            logging.info("Got the data from google drive")
            self.split_data_as_train_test(feature_store_path)
            logging.info("performed train test split")
            logging.info("Exited initiate_data_ingestion method of Data_ingestion class")

            data_ingestion_artifact=DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
            test_file_path=self.data_ingestion_config.testing_file_path)
            logging.info(f"Data Ingestion artifact:{data_ingestion_artifact}")
            return data_ingestion_artifact
        


        except Exception as e:
            raise USvisaException(e,sys)
        




        
        
    
            


        