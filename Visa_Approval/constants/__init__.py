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
SCHEMA_FILE_PATH=os.path.join("config","schema.yaml")
DATA_DOWNLOAD_URL:str="https://drive.google.com/file/d/1nsUnwZqMV2K-eP7WoQUGH9j2WkufOx9i/view?usp=sharing"
# DATA_DOWNLOAD_URL:str="https://drive.google.com/file/d/1lijGILl9xcaXkkYiIka45zh8kukeiwp1/view?usp=sharing"

LOCAL_DATA_FILE="data.zip"


DATA_INGESTION_COLLECTION_NAME:str="visa_data"
DATA_INGESTION_DIR_NAME:str="data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR:str="feature_store"
DATA_INGESTION_INGESTED_DIR:str="ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float=0.2





DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml"


DATA_TRANSFORMATIONN_DIR_NAME:str="data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR:str="transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT__DIR:str="transformed_object"





MODEL_TRAINER_DIR_NAME: str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR: str ="trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME: str ="model.pkl"
MODEL_TRAINER_EXPECTED_SCORE:float=0.6
MODEL_TRAINER_MODEL_CONFIG_FILE_PATH:str=os.path.join("config","model.yaml")



MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE:float=0.02