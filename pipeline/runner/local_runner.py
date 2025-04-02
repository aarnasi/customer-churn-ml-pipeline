import kfp.local
from kfp.local import SubprocessRunner
import pipeline.pipeline

kfp.local.init(runner=SubprocessRunner(use_venv=False))

pipeline.pipeline.pipeline()
