from kfp.dsl import component, Output, Dataset


@component(packages_to_install=["pandas", "google-cloud-storage"],
           base_image="python:3.10-slim")
def ingest_data(config: dict, output_data: Output[Dataset]):
    import pandas as pd
    import google.cloud.storage as storage
    import logging
    client = storage.Client()
    bucket = client.bucket(config["gcs"]["bucket_name"])
    blob = bucket.blob(config["gcs"]["dataset_name"])
    blob.download_to_filename("/tmp/customer_churn_processed.csv")
    df = pd.read_csv("/tmp/customer_churn_processed.csv")
    logging.log(logging.INFO, df.columns.tolist())
    df.to_csv(output_data.path, index=False)
