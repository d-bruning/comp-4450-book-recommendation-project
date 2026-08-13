import mlflow

mlflow.set_experiment("test")

with mlflow.start_run(run_name="hello_world"):
    mlflow.log_param("model", "test")
    mlflow.log_metric("accuracy", 0.95)

print("done")
