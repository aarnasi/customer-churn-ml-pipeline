from kfp.v2.dsl import Input, Output, Dataset, component


@component(
    packages_to_install=["scikit-learn", "pandas"]
)
def preprocess_data(input_data: Input[Dataset], output_data: Output[Dataset]):
    """
    Preprocesses the input dataset by selecting relevant columns,
    handling missing values, and converting target variable.

    Args:
        input_data (Input[Dataset]): Input dataset from the previous step.
        output_data (Output[Dataset]): Output path to save the preprocessed dataset.
    """
    import pandas as pd
    import logging

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    try:
        logging.info(f"Reading input dataset from: {input_data.path}")
        df = pd.read_csv(input_data.path)

        # Define columns to retain
        selected_columns = ['tenure', 'age', 'address', 'income', 'ed',
                            'employ', 'equip', 'callcard', 'wireless', 'churn']

        logging.info(f"Selecting relevant columns: {selected_columns}")
        df = df[selected_columns]

        logging.info("Dropping rows with missing values")
        df = df.dropna()

        logging.info("Converting 'churn' column to integer type")
        df['churn'] = df['churn'].astype(int)

        logging.info(f"Saving preprocessed dataset to: {output_data.path}")
        df.to_csv(output_data.path, index=False)

        logging.info("Preprocessing completed successfully")

    except Exception as e:
        logging.error("Error during data preprocessing", exc_info=True)
        raise RuntimeError(f"Data preprocessing failed: {e}")
