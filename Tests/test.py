def test_user_crud_sequential(api_client, user_data):

    create_user = user_data["create"]
    update_user = user_data["update"]

    username = create_user["username"]

    print("\nSTEP 1: CREATE USER")

    create_response = api_client.post(
        "/user",
        create_user
    )

    print("Status Code:", create_response.status_code)
    print("Response:", create_response.text)

    assert create_response.status_code == 200

    create_result = create_response.json()

    assert create_result["code"] == 200

    print("\nSTEP 2: GET USER")

    get_response = api_client.get(
        f"/user/{username}"
    )

    print("Status Code:", get_response.status_code)
    print("Response:", get_response.text)

    assert get_response.status_code == 200

    get_result = get_response.json()

    assert get_result["username"] == username
    assert get_result["firstName"] == create_user["firstName"]
    assert get_result["lastName"] == create_user["lastName"]
    assert get_result["email"] == create_user["email"]

    print("\nSTEP 3: UPDATE USER")

    update_response = api_client.put(
        f"/user/{username}",
        update_user
    )

    print("Status Code:", update_response.status_code)
    print("Response:", update_response.text)

    assert update_response.status_code == 200

    update_result = update_response.json()

    assert update_result["code"] == 200

    print("\nSTEP 4: VERIFY UPDATED USER")

    verify_response = api_client.get(
        f"/user/{username}"
    )

    print("Status Code:", verify_response.status_code)
    print("Response:", verify_response.text)

    assert verify_response.status_code == 200

    verify_result = verify_response.json()

    assert verify_result["username"] == username
    assert verify_result["firstName"] == update_user["firstName"]
    assert verify_result["lastName"] == update_user["lastName"]
    assert verify_result["email"] == update_user["email"]
    assert verify_result["phone"] == update_user["phone"]

    print("\nALL USER API TESTS PASSED!")
