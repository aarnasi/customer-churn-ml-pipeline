from kfp.v2.dsl import component


@component(base_image="us-central1-docker.pkg.dev/customer-churn-453414/customer-churn-ml-pipeline/deployer-comp", packages_to_install=["kfp"])
def deploy_to_cloud_run(
    image_uri: str,
    service_name: str,
    region: str,
    min_instances: int,
    project: str
):
    """
    Deploys a container image to Google Cloud Run with customizable settings.

    Args:
        image_uri: The URI of the container image in a container registry.
        service_name: The desired name for the Cloud Run service.
        region: The Google Cloud region for deployment.
        min_instances: Minimum number of container instances to keep running.
        project: Project ID
    """
    import subprocess
    import json
    import logging

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    try:
        # Build the gcloud command
        command = [
            "gcloud", "run", "deploy", service_name,
            f"--image={image_uri}",
            f"--region={region}",
        ]
        if project is not None:
           command.append(f"--project={project}")
        if min_instances is not None:
            command.append(f"--min-instances={min_instances}")

        logging.info("Preparing Cloud Run deployment command")

        # Log final command
        logging.info("Executing Cloud Run deployment command")
        logging.debug("Command: %s", " ".join(command))

        # Run the deployment command
        process = subprocess.run(command, capture_output=True, text=True, check=True)

        logging.info("Cloud Run deployment successful")
        logging.debug("gcloud output: %s", process.stdout)

    except subprocess.CalledProcessError as e:
        logging.error("Cloud Run deployment failed")
        logging.error("Command stdout: %s", e.stdout)
        logging.error("Command stderr: %s", e.stderr)
        raise RuntimeError("Deployment failed, see logs above for details.")
    except Exception as ex:
        logging.error("Unexpected error during deployment", exc_info=True)
        raise
