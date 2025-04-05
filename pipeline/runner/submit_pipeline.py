# Import the Vertex AI SDK
from google.cloud import aiplatform

# Import YAML modules for file handling and configuration loading
import yaml

# Load pipeline configuration from the local YAML file
with open("pipeline/configs/config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)

# Initialize the Vertex AI environment with the specified project and region
aiplatform.init(
    project=config["project"]["project_id"],  # GCP project ID
    location="us-central1"            # Region for Vertex AI services
)

# Create a PipelineJob object with the compiled pipeline JSON
pipeline_job = aiplatform.PipelineJob(
    display_name="customer-churn-pipeline",                             # Display name for the pipeline job
    template_path="pipeline/compiled_pipeline/customer_churn_pipeline.json",  # Path to compiled pipeline definition
    enable_caching=True                                                 # Enable caching to avoid recomputing steps
)

# Run the pipeline job
pipeline_job.run()
