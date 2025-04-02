import kfp.dsl as dsl
from kfp.v2 import compiler
from components.data_ingester import data_ingenstion
import yaml
import os
import logging

project_root = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(project_root, "configs/config.yaml"), "r") as config_file:
    config = yaml.safe_load(config_file)
gcs_path = f'gcp path={config["gcs"]["bucket_name"]}'
logging.log(logging.INFO, msg=gcs_path)

from components.data_preprocessor import data_preprocessing
from components.model_trainer import model_training
from components.model_deployer import deploy_model
from kfp.components import load_component_from_file

#ingestion_op = load_component_from_file("components/data_ingester/Component.yaml")


@dsl.pipeline(
    name="customer-churn-automation-pipeline",
    description="A kubeflow pipeline from data ingestion to deployment",
    pipeline_root="gs://customer_churn-sinni12/pipeline"
)
def pipeline():
    ingestion_task = data_ingenstion.ingest_data(config=config)
    #preprosessing_task = data_preprocessing.preprocess_data(input_data=ingestion_task.output)
    #model_training_task = model_training.train_model(data=preprosessing_task.output)
    #deploy_model.deploy_model(model=model_training_task.output)


#compiler.Compiler().compile(pipeline_func=pipeline, package_path="pipeline/compiled_pipeline/customer_churn_pipeline.json")
