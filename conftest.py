
import copy
import uuid

import pytest

from utils import report_generator
from utils.api_client import APIClient
from data.user_data import CREATE_USER, UPDATE_USER


def pytest_sessionstart(session):
    """Reset test results before execution"""
    report_generator.test_results.clear()


def pytest_sessionfinish(session, exitstatus):
    """Generate HTML report after all tests finish"""

    report_generator.generate_html_report()

@pytest.fixture
def api_client():
    client = APIClient()
    yield client
    client.close()


@pytest.fixture
def user_data():
    create_data = copy.deepcopy(CREATE_USER)
    update_data = copy.deepcopy(UPDATE_USER)

    unique_id = uuid.uuid4().hex[:8]

    create_data["id"] = int(unique_id, 16)
    create_data["username"] = f"automation_{unique_id}"

    update_data["id"] = create_data["id"]
    update_data["username"] = create_data["username"]

    return {
        "create": create_data,
        "update": update_data
    }

