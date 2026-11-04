import subprocess
import sys
import time

import pytest
import requests
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="session")
def fastapi_server():
    """Start the FastAPI server before E2E tests and stop it afterward."""
    fastapi_process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "main:app",
            "--host",
            "127.0.0.1",
            "--port",
            "8000",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    server_url = "http://127.0.0.1:8000/"
    timeout = 30
    start_time = time.time()

    print("Starting FastAPI server...")

    while time.time() - start_time < timeout:
        if fastapi_process.poll() is not None:
            output = fastapi_process.stdout.read()
            raise RuntimeError(
                f"FastAPI server exited unexpectedly:\n{output}"
            )

        try:
            response = requests.get(server_url, timeout=2)
            if response.status_code == 200:
                print("FastAPI server is running.")
                break
        except requests.exceptions.RequestException:
            pass

        time.sleep(1)
    else:
        fastapi_process.terminate()
        output = fastapi_process.stdout.read()
        raise RuntimeError(
            f"FastAPI server failed to start within {timeout} seconds:\n{output}"
        )

    yield

    print("Shutting down FastAPI server...")
    fastapi_process.terminate()
    fastapi_process.wait(timeout=10)


@pytest.fixture(scope="session")
def playwright_instance_fixture():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright_instance_fixture):
    browser = playwright_instance_fixture.chromium.launch(headless=True)
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def page(browser):
    page = browser.new_page()
    yield page
    page.close()