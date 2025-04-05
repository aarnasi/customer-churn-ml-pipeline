from kfp.v2.dsl import component, Input, Output, Dataset, Model

@component(
    packages_to_install=["scikit-learn", "joblib", "pandas", "google-cloud-storage"]
)
def train_model(config: dict, data: Input[Dataset], output_model: Output[Model]):
    """
    Trains a Random Forest classifier on the input dataset and uploads the serialized model to GCS.

    Args:
        config (dict): Configuration dict containing GCS bucket info under 'gcs' -> 'bucket_name'.
        data (Input[Dataset]): Preprocessed training dataset.
        output_model (Output[Model]): Output model artifact path.
    """
    # Import required libraries inside the component
    from sklearn.ensemble import RandomForestClassifier
    from sklearn import preprocessing
    import joblib
    import pandas as pd
    import google.cloud.storage as storage
    import logging
    import os

    # Set up logging format and level
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    try:
        # Load the dataset from the path provided by the upstream component
        logging.info(f"Reading training data from: {data.path}")
        df = pd.read_csv(data.path)

        # Drop any rows with missing values to avoid errors during training
        df = df.dropna()
        logging.info(f"Data shape after dropping NA: {df.shape}")

        # Define the features and target column
        feature_cols = ['tenure', 'age', 'address', 'income', 'ed', 'employ', 'equip']
        target_col = 'churn'
        logging.info(f"Extracting features: {feature_cols} and target: {target_col}")

        X = df[feature_cols]
        y = df[target_col]

        # Standardize the feature set
        logging.info("Standardizing features using StandardScaler")
        X_scaled = preprocessing.StandardScaler().fit_transform(X)

        # Train the Random Forest classifier
        logging.info("Training Random Forest Classifier with 10 estimators")
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        model.fit(X_scaled, y)
        logging.info("Model training completed")

        # Save the trained model to a temporary local path
        MODEL_LOCAL_PATH = '/tmp/customer_churn_model.joblib'
        logging.info(f"Saving trained model locally at: {MODEL_LOCAL_PATH}")
        joblib.dump(model, MODEL_LOCAL_PATH)

        # Upload the model to Google Cloud Storage
        bucket_name = config['gcs']['bucket_name']
        model_blob_path = os.path.join("models", "customer_churn_model.joblib")
        logging.info(f"Preparing to upload model to: gs://{bucket_name}/{model_blob_path}")

        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(model_blob_path)
        blob.upload_from_filename(MODEL_LOCAL_PATH)
        logging.info("Model uploaded to GCS successfully")

        # Set the model URI as output for downstream components
        output_model.uri = f"gs://{bucket_name}/{model_blob_path}"
        logging.info(f"Output model URI set: {output_model.uri}")

    except Exception as e:
        # Log and raise errors to surface issues in pipeline runs
        logging.error("Error occurred during model training or upload", exc_info=True)
        raise RuntimeError(f"Model training failed: {e}")
