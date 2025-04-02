from google.cloud import aiplatform

aiplatform.init(project="customer-churn-453414", location="us-central1")

pipeline_job = aiplatform.PipelineJob(
    display_name="customer-churn-pipeline",
    template_path="../compiled_pipeline/customer_churn_pipeline.json",
    enable_caching=True
)
pipeline_job.run()
