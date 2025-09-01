import sys
import time
from pathlib import Path

import requests

API_URL = "http://localhost:8000"


def upload_document(file_path: Path) -> str:
    """Upload the document and return the job ID."""
    with file_path.open("rb") as f:
        response = requests.post(f"{API_URL}/api/review", files={"file": f})
    response.raise_for_status()
    return response.json()["job_id"]


def wait_for_completion(job_id: str, interval: int = 2) -> str:
    """Poll the job status until completed and return the analysis URL."""
    while True:
        response = requests.get(f"{API_URL}/api/job/{job_id}")
        response.raise_for_status()
        data = response.json()
        if data.get("status") == "completed":
            return data["result"]["analysis_url"]
        time.sleep(interval)


def fetch_results(analysis_url: str) -> dict:
    """Fetch the analysis results."""
    response = requests.get(f"{API_URL}{analysis_url}")
    response.raise_for_status()
    return response.json()


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python upload_and_review.py path/to/contract.pdf")
        sys.exit(1)

    file_path = Path(sys.argv[1])
    job_id = upload_document(file_path)
    print(f"Uploaded. Job ID: {job_id}")
    analysis_url = wait_for_completion(job_id)
    result = fetch_results(analysis_url)
    summary = result.get("analysis", {}).get("summary", "No summary available")
    print("Summary:\n", summary)


if __name__ == "__main__":
    main()
