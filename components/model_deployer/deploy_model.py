from kfp.v2.dsl import component, Input, Model


@component(packages_to_install=["google-cloud-aiplatform"])
def deploy_model(model: Input[Model]):
    import os
    from google.cloud import aiplatform
    aiplatform.init(project="customer-churn-453414", location="us-central1")
    model = aiplatform.Model.upload(
        display_name="customer-churn-ml-model",
        artifact_uri=os.path.dirname(model.uri),
        serving_container_image_uri="us-docker.pkg.dev/vertex-ai/prediction/sklearn-cpu.0-24:latest"
    )
    endpoint = model.deploy(machine_type="n1-standard-4")
