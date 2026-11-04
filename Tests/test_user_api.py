from utils.report_generator import add_test_result

def execute_step(
    test_case,
    category,
    api_request,
    validator,
    expected_result
):
    """
    Execute API request, validate response,
    and save test result.
    """

    response = None

    try:
        response = api_request()

        validator(response)

        add_test_result(
            test_case=test_case,
            category=category,
            status="PASS",
            status_code=response.status_code,
            message="API validation successful",
            data=expected_result
        )

        print(f"\n{test_case}: PASS")

        return response

    except Exception as error:

        status_code = (
            response.status_code
            if response is not None
            else "N/A"
        )

        response_data = (
            response.text
            if response is not None
            else "No response received"
        )

        add_test_result(
            test_case=test_case,
            category=category,
            status="FAIL",
            status_code=status_code,
            message=f"{str(error)} | Response: {response_data}",
            data=expected_result
        )

        print(f"\n{test_case}: FAIL")

        raise

def test_create_user(api_client, user_data):

    create_user = user_data["create"]

    execute_step(
        test_case="TC01 - Create User",
        category="POSITIVE",

        api_request=lambda: api_client.post(
            "/user",
            create_user
        ),

        validator=assert_create_response,

        expected_result="HTTP 200 and response code 200"
    )

def test_get_user_data_valid(api_client, created_user):

    username = created_user["username"]

    execute_step(
        test_case="TC02 - Get Valid User",
        category="POSITIVE",

        api_request=lambda: api_client.get(
            f"/user/{username}"
        ),

        validator=lambda response: (
            assert_get_response(response, created_user)
        ),

        expected_result="HTTP 200 and user data matches"
    )

def test_get_user_data_invalid_username(
    api_client,
    user_data
):

    invalid_username = user_data["invalid_username"]

    execute_step(
        test_case="TC03 - Get Invalid User",
        category="NEGATIVE",

        api_request=lambda: api_client.get(
            f"/user/{invalid_username}"
        ),

        validator=assert_get_response_invalid,

        expected_result="HTTP 404 - User not found"
    )


def test_update_user(api_client, created_user, user_data):

    username = created_user["username"]

    update_user = user_data["update"]

    execute_step(
        test_case="TC04 - Update User",
        category="POSITIVE",

        api_request=lambda: api_client.put(
            f"/user/{username}",
            update_user
        ),

        validator=assert_update_response,

        expected_result="HTTP 200 and response code 200"
    )


def test_verify_updated_user(
    api_client,
    created_user,
    user_data
):

    username = created_user["username"]

    update_user = user_data["update"]

    # First update the user because this test
    # is designed to be independently executable.

    update_response = api_client.put(
        f"/user/{username}",
        update_user
    )

    assert update_response.status_code == 200

    execute_step(
        test_case="TC05 - Verify Updated User",
        category="POSITIVE",

        api_request=lambda: api_client.get(
            f"/user/{username}"
        ),

        validator=lambda response: (
            assert_get_response(response, update_user)
        ),

        expected_result="HTTP 200 and updated user data matches"
    )
# ASSERTION FUNCTIONS
def assert_create_response(response):

    assert response.status_code == 200, (
        f"Expected HTTP 200, got {response.status_code}"
    )

    result = response.json()

    assert result["code"] == 200, (
        f"Expected response code 200, got {result}"
    )


def assert_update_response(response):

    assert response.status_code == 200, (
        f"Expected HTTP 200, got {response.status_code}"
    )

    result = response.json()

    assert result["code"] == 200, (
        f"Expected response code 200, got {result}"
    )


def assert_get_response(response, expected_user):

    assert response.status_code == 200, (
        f"Expected HTTP 200, got {response.status_code}"
    )

    result = response.json()

    fields = [
        "username",
        "firstName",
        "lastName",
        "email",
        "phone"
    ]

    for field in fields:

        assert result.get(field) == expected_user[field], (
            f"{field} mismatch. "
            f"Expected: {expected_user[field]}, "
            f"Actual: {result.get(field)}"
        )


def assert_get_response_invalid(response):

    assert response.status_code == 404, (
        f"Expected HTTP 404, got {response.status_code}"
    )

    result = response.json()
    message = str(result.get("message", "")).lower()

    assert "not found" in message, (
        f"Expected user not found message, got {result}"
    )


def assert_verify_response(response, expected_user):
    assert_get_response(response, expected_user)