from pathlib import Path
import subprocess

import mlflow


def get_git_commit() -> str:
    """
    Returns the current git commit hash.
    """

    try:
        return (
            subprocess.check_output(
                ["git", "rev-parse", "HEAD"]
            )
            .decode("utf-8")
            .strip()
        )

    except Exception:
        return "unknown"


def initialize_experiment(
    experiment_name: str,
    run_name: str,
    params: dict
):
    """
    Configure MLflow experiment and start a run.
    """

    mlflow.set_experiment(experiment_name)

    mlflow.start_run(run_name=run_name)

    params = dict(params)

    params["git_commit"] = get_git_commit()

    mlflow.log_params(params)


def log_metrics(metrics: dict):
    """
    Log metrics to MLflow.
    """

    for key, value in metrics.items():

        if isinstance(value, (int, float)):
            mlflow.log_metric(key, value)


def log_artifacts(files):
    """
    Log one or more files as artifacts.
    """

    for file in files:
        mlflow.log_artifact(str(file))


def finish_run():
    """
    End the active MLflow run.
    """

    mlflow.end_run()
