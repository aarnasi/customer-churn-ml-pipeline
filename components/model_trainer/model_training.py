import os.path

from kfp.v2.dsl import component, Input, Output, Dataset, Model


@component(packages_to_install=["scikit-learn", "joblib", "pandas", "google-cloud-storage"], )
def train_model(data: Input[Dataset], output_model: Output[Model]):
    from sklearn.ensemble import RandomForestClassifier
    import joblib
    import google.cloud.storage as storage
    import pandas as pd
    import logging
    import os
    df = pd.read_csv(data.path)
    X, y = df.drop(columns=["churn"]), df["churn"]
    model = RandomForestClassifier(n_estimators=10)
    model.fit(X, y)

    # Save the model to a local file using joblib
    model_local_path = '/tmp/random_forest_model.pkl'
    joblib.dump(model, model_local_path)
    logging.log(level=logging.INFO, msg="Object serialized")

    # Upload the model to GCS
    bucket = storage.Client().bucket("customer_churn-sinni12")
    full_model_path = os.path.join("models", "model.pkl")
    bucket.blob(os.path.join(full_model_path)).upload_from_filename(model_local_path)
    output_model.uri = "gs://customer_churn-sinni12/" + full_model_path
