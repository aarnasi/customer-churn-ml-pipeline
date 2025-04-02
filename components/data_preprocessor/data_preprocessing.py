from kfp.v2.dsl import Input, Output, Dataset, component


@component(packages_to_install=["scikit-learn", "pandas"])
def preprocess_data(input_data: Input[Dataset], output_data: Output[Dataset]):
    import pandas as pd
    df = pd.read_csv(input_data.path)
    df.fillna(0, inplace=True)
    df.to_csv(output_data.path, index=False)
