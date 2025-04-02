from google.cloud import aiplatform
from kfp.v2 import compiler
from pipeline import pipeline

compiler.Compiler().compile(pipeline_func=pipeline,
                            package_path="pipeline/customer_churn_pipeline/compiled_pipeline/customer_churn_pipeline.json")

aiplatform.init(project="customer-churn-453414", location="us-central1")

pipeline_job = aiplatform.PipelineJob(
    display_name="customer-churn-pipeline",
    template_path="../compiled_pipeline/customer_churn_pipeline.json",
    enable_caching=True
)
pipeline_job.run()
