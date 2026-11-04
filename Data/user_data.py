import uuid

def generate_user_data():

    unique_id = uuid.uuid4().hex[:8]

    create_user = {
        "id": int(unique_id, 16),
        "username": f"automation_{unique_id}",
        "firstName": "Muhammad",
        "lastName": "Reza",
        "email": "muhrez@test.com",
        "password": "Test12345",
        "phone": "08123456789",
        "userStatus": 1
    }

    update_user = {
        "id": create_user["id"],
        "username": create_user["username"],
        "firstName": "Kurniawan",
        "lastName": "Santana",
        "email": "updated@test.com",
        "password": "Updated12345",
        "phone": "08987654321",
        "userStatus": 1
    }

    invalid_username = f"invalid_{uuid.uuid4().hex}"

    return {
        "create": create_user,
        "update": update_user,
        "invalid_username": invalid_username
    }