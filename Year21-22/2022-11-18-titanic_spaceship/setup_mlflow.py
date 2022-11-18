# set up mlflow
import os
import mlflow
import pandas as pd

os.environ["MLFLOW_TRACKING_URI"] = "https://mlflow.spencerlyon.com"
os.environ["MLFLOW_EXPERIMENT_NAME"] = "ucf-kaggle-titanic-spaceship"
os.environ["MLFLOW_TRACKING_USERNAME"] = "TODO"
os.environ["MLFLOW_TRACKING_PASSWORD"] = "TODO"

if "MLFLOW_TRACKING_PASSWORD" not in os.environ:
    raise ValueError("You need to properly configure the `.env` file")
else:
    print("good work! mlflow ready to go")

mlflow.set_experiment(os.environ.get("MLFLOW_EXPERIMENT_NAME", "Default"))