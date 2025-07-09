from kfp.dsl import component, Output, Dataset


@component(
    packages_to_install=["pandas", "google-cloud-storage"],
    base_image="python:3.10-slim"
)
def ingest_data(config: dict, output_data: Output[Dataset]):
    """
    Downloads a dataset from Google Cloud Storage and writes it to the pipeline's output path.

    Args:
        config (dict): A dictionary containing GCS configuration with keys:
                       - 'bucket_name': Name of the GCS bucket
                       - 'dataset_name': Name of the CSV file in the GCS bucket
        output_data (Output[Dataset]): Output artifact path to write the dataset to
    """
    import pandas as pd
    import google.cloud.storage as storage
    import logging
    import os

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    try:
        logging.info("Initializing Google Cloud Storage client...")
        client = storage.Client()

        bucket_name = config["gcs"]["bucket_name"]
        dataset_name = config["gcs"]["dataset_name"]

        logging.info(f"Accessing bucket: {bucket_name}")
        bucket = client.bucket(bucket_name)

        logging.info(f"Downloading blob: {dataset_name}")
        blob = bucket.blob(dataset_name)

        local_path = "/tmp/customer_churn_processed.csv"
        blob.download_to_filename(local_path)
        logging.info(f"File downloaded to: {local_path}")

        logging.info("Reading CSV file into pandas DataFrame...")
        df = pd.read_csv(local_path)

        logging.info(f"Writing dataset to pipeline output path: {output_data.path}")
        df.to_csv(output_data.path, index=False)

        logging.info("Data ingestion completed successfully.")

    except Exception as e:
        logging.error("Error during data ingestion", exc_info=True)
        raise RuntimeError(f"Failed to ingest data: {e}")
