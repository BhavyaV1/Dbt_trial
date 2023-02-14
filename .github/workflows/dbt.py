import enum
import os
import time

# Be sure to `pip install requests` in your python environment
import requests

ACCOUNT_ID = 82119
JOB_ID = 210238

# Store your dbt Cloud API token securely in your workflow tool
API_KEY = os.getenv('DBT_CLOUD_API_TOKEN')

# These are documented on the dbt Cloud API docs


class DbtJobRunStatus(enum.IntEnum):
    QUEUED = 1
    STARTING = 2
    RUNNING = 3
    SUCCESS = 10
    ERROR = 20
    CANCELLED = 30


def _trigger_job() -> int:
    res = requests.post(
        url=f"https://cloud.getdbt.com/api/v2/accounts/{ACCOUNT_ID}/jobs/{JOB_ID}/run/",
        headers={'Authorization': f"Token {API_KEY}"},
        json={
            # Optionally pass a description that can be viewed within the dbt Cloud API.
            # See the API docs for additional parameters that can be passed in,
            # including `schema_override`
            'cause': f"Triggered by bhavya's workflow!",
        }
    )

    try:
        res.raise_for_status()
    except:
        print(f"API token (last four): ...{API_KEY[-4:]}")
        raise
    response_payload = res.json()
    return response_payload['data']['id']


def _get_job_run_status(job_run_id):
    res = requests.get(
        url=f"https://cloud.getdbt.com/api/v2/accounts/{ACCOUNT_ID}/runs/{job_run_id}/",
        headers={'Authorization': f"Token {API_KEY}"},
    )
    res.raise_for_status()
    response_payload = res.json()
    return response_payload['data']['status']


def run():
    job_run_id = _trigger_job()
    print(f"job_run_id = {job_run_id}")
    while True:
        time.sleep(5)
        status = _get_job_run_status(job_run_id)
        print(f"status = {status}")
        if status == DbtJobRunStatus.SUCCESS:
            break
        elif status == DbtJobRunStatus.ERROR or status == DbtJobRunStatus.CANCELLED:
            raise Exception("Failure!")


if __name__ == '__main__':
    run()
