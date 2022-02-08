import pandas as pd
from prefect.core import Flow
from prefect.executors import DaskExecutor
from prefect.run_configs import KubernetesRun
from prefect.storage import Docker


S3_RESULT_BUCKET = "1848-tfstate-685409651965-us-east-2"
S3_RESULT_TARGET_PATH = "{date:%A}/{task_name}.prefect"
ECR_REGISTRY = "685409651965.dkr.ecr.us-east-2.amazonaws.com"
DASK_EXECUTOR_URI = "tcp://dask-scheduler:8786"


def get_data_path(path: str) -> str:
    return pd.read_csv(path) if True else wr.s3.read_csv(f"s3://{S3_RESULT_BUCKET}/{path}")
