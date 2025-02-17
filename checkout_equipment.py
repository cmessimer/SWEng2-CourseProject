import requests

# Set API endpoints
login_url = "http://127.0.0.1:5000/login"
checkout_url = "http://127.0.0.1:5000/checkout"

# Step 1: Login and get JWT token
login_data = {"username": "chad", "password": "password123"}
login_response = requests.post(login_url, json=login_data)

if login_response.status_code == 200:
    token = login_response.json().get("access_token")
    print(f"Login successful! Token: {token}")

    # Step 2: Fetch Equipment List
    headers = {"Authorization": f"Bearer {token}"}
    equipment_list_response = requests.get("http://127.0.0.1:5000/equipment", headers=headers)

    if equipment_list_response.status_code == 200:
        equipment_list = equipment_list_response.json()
        if not equipment_list:
            print("No equipment found in the database.")
        else:
            # Pick the first available equipment
            equipment_id = equipment_list[0]["id"]
            print(f"Checking out Equipment ID: {equipment_id}")

            # Step 3: Checkout Equipment
            checkout_data = {"equipment_id": equipment_id}
            checkout_response = requests.post(checkout_url, json=checkout_data, headers=headers)

            if checkout_response.status_code == 200:
                print(f"Checkout Successful: {checkout_response.json()}")
            else:
                print(f"Error: {checkout_response.status_code}, {checkout_response.text}")

    else:
        print(f"Error fetching equipment list: {equipment_list_response.status_code}, {equipment_list_response.text}")

else:
    print(f"Login Failed: {login_response.status_code}, {login_response.text}")
