import os
from datetime import datetime
import logging
from  pathlib import Path
logging.basicConfig(level=logging.INFO,format='%(asctime)s:%(message)s')

project_name="Visa_Approval"


list_of_folders=[
    f"{project_name}/__init__.py",  
    f"{project_name}/components/__init__.py",
    f"{project_name}/components/data_ingestion.py",
    f"{project_name}/components/data_validation.py",
    f"{project_name}/components/data_transformation.py",
    f"{project_name}/components/model_trainer.py",
    f"{project_name}/constants/__init__.py",
    f"{project_name}/logger/__init__.py",
    f"{project_name}/Exception/__init__.py",
    f"{project_name}/pipelines/__init__.py",
    f"{project_name}/pipelines/training_pipelines.py",
    f"{project_name}/pipelines/predictions_pipelines.py",
    f"{project_name}/entity/__init__.py",
    f"{project_name}/entity/config.py",
    f"{project_name}/entity/artifacts.py",
    f"{project_name}/utils/__init__.py",
    f"{project_name}/utils/main_utils.py",
    "templates/index.html",
    "research/EDA.ipynb",
    "research/FEATURE_ENG.ipynb",
    "app.py",
    "requirements.txt",
    "Dockerfile",
    ".dockerignore",
    "demo.py",
    "setup.py",
    "config/model.yaml",
    "config/schema.yaml",
]
for file in list_of_folders:
    file=Path(file)
    file_dir,file_name=os.path.split(file)
    if file_dir!="":
        os.makedirs(file_dir,exist_ok=True)
        logging.info(f"creating directory:{file_dir} for file {file_name}")
    if (not os.path.exists(file)) or (os.path.getsize(file))==0:
        with open(file,"w") as f:
            pass
        logging.info(f"creating file:{file}")
    else:
        logging.info(f"file {file} already present")