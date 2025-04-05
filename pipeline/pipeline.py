# Import Kubeflow Pipelines DSL for defining the pipeline structure
import kfp.dsl as dsl

# Import the KFP compiler to compile the pipeline
from kfp.v2 import compiler

# Import the custom pipeline components
from components.data_ingester import data_ingenstion

# Standard Python libraries
import yaml

# Load pipeline configuration from the YAML file
with open("pipeline/configs/config_local.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)

# Import other pipeline components
from components.data_preprocessor import data_preprocessing
from components.model_trainer import model_training
from components.model_deployer import deploy_model

# Define the Kubeflow pipeline using the loaded configuration
@dsl.pipeline(
    name=config['pipeline']['name'],                      # Name of the pipeline
    description=config['pipeline']['description'],        # Pipeline description
    pipeline_root=config['pipeline']['pipeline_root']     # Pipeline root path in GCS
)
def pipeline():
    # Step 1: Ingest data using a custom component
    ingestion_op = data_ingenstion.ingest_data(config=config)

    # Step 2: Preprocess the ingested data
    preprosessing_op = data_preprocessing.preprocess_data(input_data=ingestion_op.output)

    # Step 3: Train a model using the preprocessed data
    model_training_op = model_training.train_model(config=config, data=preprosessing_op.output)

    # Step 4: Deploy the trained model as a service on Cloud Run
    deploy_service_op = deploy_model.deploy_to_cloud_run(
        image_uri=config['service']['image_uri'],             # Container image URI
        service_name=config['service']['service_name'],       # Cloud Run service name
        region=config['service']['region'],                   # Region for deployment
        min_instances=config['service']['min_instances'],     # Minimum instances to keep warm
        project=config['service']['project_id']               # GCP project ID
    )

    # Ensure the model is deployed only after training is completed
    deploy_service_op.after(model_training_op)
