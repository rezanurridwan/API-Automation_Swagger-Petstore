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

def test_user_crud_sequential(api_client, user_data):

    create_user = user_data["create"]
    update_user = user_data["update"]

    username = create_user["username"]

    print("\nSTEP 1: CREATE USER")

    create_response = execute_step(
        test_case="TC01 - Create User",
        category="POSITIVE",

        api_request=lambda: api_client.post(
            "/user",
            create_user
        ),

        validator=lambda response: (
            assert_create_response(response)
        ),

        expected_result="HTTP 200 and response code 200"
    )

    get_response = execute_step(
        test_case="TC02 - Get User",
        category="POSITIVE",

        api_request=lambda: api_client.get(
            f"/user/{username}"
        ),

        validator=lambda response: (
            assert_get_response(response, create_user)
        ),

        expected_result="HTTP 200 and created user data matches"
    )
    update_response = execute_step(
        test_case="TC03 - Update User",
        category="POSITIVE",

        api_request=lambda: api_client.put(
            f"/user/{username}",
            update_user
        ),

        validator=lambda response: (
            assert_update_response(response)
        ),

        expected_result="HTTP 200 and updated user data matches"
    )

    print("Status Code:", update_response.status_code)
    print("Response:", update_response.text)

    assert update_response.status_code == 200

    update_result = update_response.json()

    assert update_result["code"] == 200

    print("\nSTEP 4: VERIFY UPDATED USER")

    verify_response = execute_step(
        test_case="TC04 - Verify Updated User",
        category="POSITIVE",

        api_request=lambda: api_client.get(
            f"/user/{username}"
        ),

        validator=lambda response: (
            assert_verify_response(response, update_user)
        ),

        expected_result="HTTP 200 and updated user data matches"
    )

