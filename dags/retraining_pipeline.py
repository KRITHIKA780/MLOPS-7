from datetime import datetime
import json
import os
from pathlib import Path
from urllib.request import Request, urlopen

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import BranchPythonOperator
from airflow.utils.trigger_rule import TriggerRule


THRESHOLD = 0.80
DATA_DIR = Path("/opt/airflow/data")


def notify(message):
    notification = f"{datetime.now().isoformat()} {message}"
    print(notification)
    with (DATA_DIR / "notifications.log").open("a", encoding="utf-8") as file:
        file.write(notification + "\n")

    webhook_url = os.environ.get("NOTIFICATION_WEBHOOK_URL")
    if webhook_url:
        payload = json.dumps({"text": message}).encode("utf-8")
        request = Request(
            webhook_url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=10):
            pass


def notify_failure(context):
    task = context.get("task_instance")
    notify(f"Airflow retraining failed: {task.task_id if task else 'unknown task'}")


def check_degradation():

    with open(
        DATA_DIR / "current_accuracy.txt", "r", encoding="utf-8"
    ) as f:

        accuracy = float(f.read())

    print("Current Accuracy:", accuracy)

    if accuracy < THRESHOLD:
        print("DEGRADATION DETECTED")
        return "retrain_model"

    print("Model performance is acceptable")
    return "model_ok"


def notify_retraining_complete():
    accuracy = (DATA_DIR / "new_accuracy.txt").read_text(encoding="utf-8").strip()
    notify(f"Model retrained and deployed successfully. New accuracy: {accuracy}")


with DAG(
    dag_id="automatic_model_retraining",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["mlops", "retraining"],
    on_failure_callback=notify_failure,
) as dag:

    degrade_data = BashOperator(
        task_id="simulate_degradation",
        bash_command="python /opt/airflow/scripts/degrade_data.py"
    )

    evaluate_model = BashOperator(
        task_id="evaluate_model",
        bash_command="python /opt/airflow/scripts/evaluate_model.py"
    )

    check_model = BranchPythonOperator(
        task_id="check_degradation",
        python_callable=check_degradation
    )

    retrain_model = BashOperator(
        task_id="retrain_model",
        bash_command="python /opt/airflow/scripts/retrain_model.py"
    )

    deploy_model = BashOperator(
        task_id="deploy_model",
        bash_command="python /opt/airflow/scripts/deploy_model.py"
    )

    model_ok = EmptyOperator(
        task_id="model_ok"
    )

    notify_complete = PythonOperator(
        task_id="notify_retraining_complete",
        python_callable=notify_retraining_complete,
        trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS,
    )

    degrade_data >> evaluate_model >> check_model

    check_model >> retrain_model
    check_model >> model_ok

    retrain_model >> deploy_model >> notify_complete
    model_ok >> notify_complete