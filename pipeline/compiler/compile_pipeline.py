from kfp.v2 import compiler

from pipeline.pipeline import pipeline

compiler.Compiler().compile(pipeline_func=pipeline,
                            package_path="pipeline/compiled_pipeline/customer_churn_pipeline.json")