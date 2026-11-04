import pytest

from utils.api_client import APIClient
from data.user_data import generate_user_data
from utils import report_generator


@pytest.fixture
def api_client():
    client = APIClient()
    yield client
    client.close()


@pytest.fixture
def user_data():
    return generate_user_data()


@pytest.fixture
def created_user(api_client, user_data):

    create_user = user_data["create"]

    response = api_client.post(
        "/user",
        create_user
    )

    assert response.status_code == 200, (
        f"Failed to create user: {response.text}"
    )

    assert response.json()["code"] == 200

    return create_user


def pytest_sessionstart(session):
    report_generator.test_results.clear()


def pytest_sessionfinish(session, exitstatus):
    report_generator.generate_html_report()