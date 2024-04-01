import numpy as np
import pandas as pd
import os,sys
from imblearn.combine import SMOTEENN
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler,OneHotEncoder,OrdinalEncoder,PowerTransformer
from sklearn.compose import ColumnTransformer

from Visa_Approval.constants import TARGET_COLUMN,SCHEMA_FILE_PATH,CURRENT_YEAR
from Visa_Approval.entity.config import DataTransformationConfig,DataIngestionConfig,DataValidationConfig
from Visa_Approval.entity.artifacts import DataTransformationArtifact,DataIngestionArtifact,DataValidationArtifact
from Visa_Approval.logger import logging
from Visa_Approval.utils.main_utils import save_object,save_numpy_array_data,read_yaml_file,drop_columns
from Visa_Approval.Exception import USvisaException
from Visa_Approval.entity.estimator import TargetValueMapping

class DataTransformation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                 data_transformation_config:DataTransformationConfig,
                 data_validation_artifact:DataValidationArtifact):
        
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_transformation_config=data_transformation_config
            self.data_validation_artifact=data_validation_artifact
            self._schema_config=read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise USvisaException(e,sys)
        


    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise USvisaException(e,sys)
            


    def get_data_transformer_object(self)->Pipeline:


        logging.info("Entered get_data_transformer_object method of DataTransformation class" )
        try:
            logging.info("Got numerical cols from schema config")
            numeric_transformer=StandardScaler()
            oh_transformer=OneHotEncoder()
            Ordina_encoder=OrdinalEncoder()
            logging.info("Initialized StandardScaler,OneHotEncoder,OrdinaEncoder")
            oh_columns=self._schema_config["oh_columns"]
            or_columns=self._schema_config["or_columns"]
            transform_columns =self._schema_config["transform_columns"]
            num_features=self._schema_config["num_features"]
            logging.info("Initialize PoerTransformer")

            transform_pipe=Pipeline(steps=[
            ("transform",PowerTransformer(method="yeo-johnson"))
            ])
            preprocessor=ColumnTransformer(
                [
                    ("OneHotEncode",oh_transformer,oh_columns),
                    ("Ordinal_Encoder",Ordina_encoder,or_columns),
                    ("StandardScaler",numeric_transformer,num_features)

                    ]
                )

            logging.info("Created preprocessor object form Column Transformer")
            logging.info("Exited get_data_transformer_object method of DataTransformation class")
            return preprocessor
        except Exception as e:
            raise USvisaException(e,sys)
            

    def initiate_data_transformation(self,)->DataIngestionArtifact:

        try:
            if self.data_validation_artifact.validation_status:
                logging.info("Starting data transformation")
                preprocessor=self.get_data_transformer_object()
                logging.info("Got the preprocessor object")
                
                train_df=DataTransformation.read_data(file_path=self.data_ingestion_artifact.trained_file_path)
                test_df=DataTransformation.read_data(file_path=self.data_ingestion_artifact.test_file_path)

                input_features_train_df=train_df.drop(columns=[TARGET_COLUMN],axis=1)
                target_features_train_df=train_df[TARGET_COLUMN]
                logging.info("Got the train features and test features of training dataset")

                input_features_train_df["company_age"]=CURRENT_YEAR-input_features_train_df["yr_of_estab"]

                logging.info("Added company_age column to the training dataset")

                drop_cols=self._schema_config["drop_columns"]

                logging.info("drop the columns in drop_cols of training dataset")
                input_features_train_df=drop_columns(df=input_features_train_df,cols=drop_cols)
                target_features_train_df=target_features_train_df.replace(
                    TargetValueMapping()._asdict()
                )


                input_features_test_df=test_df.drop(columns=[TARGET_COLUMN],axis=1)
                target_features_test_df=test_df[TARGET_COLUMN]
                input_features_test_df["company_age"]=CURRENT_YEAR-input_features_test_df["yr_of_estab"]
                logging.info("drop the column in drop_cols of Test dataset")
                input_features_test_df=drop_columns(df=input_features_test_df,cols=drop_cols)
                logging.info("drop the column in drop_cols of Test dataset")

                target_features_test_df =target_features_test_df.replace(
                    TargetValueMapping()._asdict()
                )

                logging.info("Got train features and test features of Testing dataset")
                logging.info("Applying prerocessing object on training dataframe and testing dataframe")
                 


                input_feature_train_arr=preprocessor.fit_transform(input_features_train_df)
                
                logging.info("Used the preprocessor object to fit transform the train features")

                input_feature_test_arr=preprocessor.transform(input_features_test_df)

                logging.info("Used the preprocessor object to fit transform the test features")
                logging.info("Applying the SMOTEEENN onn Training dataset")

                smt=SMOTEENN(sampling_strategy="minority")
                input_feature_train_final,target_features_train_final=smt.fit_resample(
                    input_feature_train_arr,target_features_train_df)

                logging.info("Applied SMOTEEN on training  dataset")
                logging.info("Applying the SMOTEEENN onn testing dataset")

                input_feature_test_final,target_features_test_final=smt.fit_resample(input_feature_test_arr,
                                            target_features_test_df)
                
                logging.info("Applied SMOTEEN on testing  dataset")
                logging.info("Created train array and test array")


                train_arr=np.c_[
                    input_feature_train_final,np.array(target_features_train_final)
                ]

                test_arr=np.c_[
                    input_feature_test_final,np.array(target_features_test_final)
                ]
                

                save_object(self.data_transformation_config.transformed_object_file_path,
                            preprocessor)
                save_numpy_array_data(self.data_transformation_config.
                                      transformed_train_file_path,array=train_arr)
                save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,array=test_arr)
                

                logging.info("saved the preprocessor object")

                logging.info("Exited initiate_data_transformation method of Data_Transformation class")

                data_transformation_artifact =DataTransformationArtifact(
                    transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                    transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                    transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
                )
                             

                return data_transformation_artifact
            else:
                raise USvisaException(self.data_validation_artifact.message)

        except Exception as e:
            raise USvisaException(e,sys)
