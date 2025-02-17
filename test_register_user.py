import requests

url = "http://127.0.0.1:5000/register"
data = {
    "username": "chad",
    "password": "password123",
    "position": "Software Engineer",  # ✅ Include a position value
    "role": "Employee"
}

response = requests.post(url, json=data)
print(response.json())  # Expected: {"message": "User registered successfully"}
