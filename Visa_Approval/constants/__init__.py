import os
from datetime import date

ARTIFACT_DIR:str="usvisa"

PIPELINE_NAME:str="usvisa"
MODEL_FILE_NAME="model.pkl"
TARGET_COLUMN:str="case_status"
CURRENT_YEAR=date.today().year
PREPROCESSING_OBJECT_FILE_NAME="preprocessing.pkl"
FILE_NAME:str="Visadataset.csv"
TRAIN_FILE_NAME:str="train.csv"
TEST_FILE_NAME:str="test.csv"
SCHEMA_FILE_PATH:str=os.path.join("config","schema.yaml")
DATA_DOWNLOAD_URL:str="https://drive.google.com/file/d/1nsUnwZqMV2K-eP7WoQUGH9j2WkufOx9i/view?usp=sharing"
# DATA_DOWNLOAD_URL:str="https://drive.google.com/file/d/1lijGILl9xcaXkkYiIka45zh8kukeiwp1/view?usp=sharing"

LOCAL_DATA_FILE="data.zip"


DATA_INGESTION_COLLECTION_NAME:str="visa_data"
DATA_INGESTION_DIR_NAME:str="data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR:str="feature_store"
DATA_INGESTION_INGESTED_DIR:str="ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float=0.2




