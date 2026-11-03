import requests, urllib3
import json
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class users:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.verify = False
    
    def test_post_request(self, endpoint, headers, data):
        """Test POST request"""
        url = f"{self.base_url}{endpoint}"
        headers = headers
        
        try:
            response = self.session.post(url, headers=headers, json=data)
            return response
        except Exception as e:
            print(f"Error: {str(e)}")
            return None
        
    def test_get_request(self, endpoint, headers):
        """Test GET request"""
        url = f"{self.base_url}{endpoint}"
        headers = headers
        
        try:
            response = self.session.get(url, headers=headers)
            return response
        except Exception as e:
            print(f"Error: {str(e)}")
            return None
    
    def validate_status_code(self, response, expected_code):
        """Validasi status code"""
        if response and response.status_code == expected_code:
            print(f"Status code valid: {expected_code}")
            return True
        else:
            print(f"Status code tidak sesuai. Expected: {expected_code}, Got: {response.status_code if response else 'None'}")
            return False
    def get_random_id(self):
        return int
    
    
if __name__ == "__main__":
    api = users("https://petstore.swagger.io/v2")
    
    headers = {
        "Content-Type": "application/json",
        "accept": "application/json"
    }

    body_post = {
        "id": 1,
        "username": "facia123",
        "firstName": "Facia",
        "lastName": "Puspa",
        "email": "facia@mail.com",
        "password": "password123",
        "phone": "+8251716666",
        "userStatus": 0
        }
   
    response = api.test_post_request("/user", headers, body_post)
    if response is None:
        print("No response received")
    else:
        if response.status_code == 200:
            try:
                result = response.json()
            except Exception:
                print("Invalid JSON response")
                result = response.text
                code = result.get("code")
                message = result.get("message")
                
        else:
            print(f"Status Code: {response.status_code}")
            print(f"Response Body: {response.text}")
            try:
                print(response.json())
            except:
                print(response.text)
        print(f"Status Code: {status_code}")