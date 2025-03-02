import requests

# API Endpoints
login_url = "http://127.0.0.1:5000/login"
return_url = "http://127.0.0.1:5000/return"
equipment_url = "http://127.0.0.1:5000/equipment"

# Step 1: Log in and get JWT token (UPDATED PASSWORD)
login_data = {"username": "chad", "password": "newpassword456"}
login_response = requests.post(login_url, json=login_data)

if login_response.status_code == 200:
    token = login_response.json().get("access_token")
    print(f"Login successful! Token: {token}")

    # Step 2: Fetch Checked-Out Equipment
    headers = {"Authorization": f"Bearer {token}"}
    equipment_list_response = requests.get(equipment_url, headers=headers)

    if equipment_list_response.status_code == 200:
        equipment_list = equipment_list_response.json()
        checked_out_equipment = [e for e in equipment_list if e["status"] == "Checked Out"]

        if not checked_out_equipment:
            print("No checked-out equipment to return.")
        else:
            print("\nChecked-Out Equipment:")
            for equip in checked_out_equipment:
                print(f"ID: {equip['id']}, Name: {equip['name']}")

            # Ask user which equipment to return
            equipment_id = input("\nEnter Equipment ID to return: ").strip()

            # Step 3: Return Equipment
            return_data = {"equipment_id": equipment_id}
            return_response = requests.post(return_url, json=return_data, headers=headers)
            if return_response.status_code == 200:
                print(f"Return Successful: {return_response.json()}")
                print(f"Equipment ID {equipment_id} returned successfully.")
            else:
                print(f"Error: {return_response.status_code}, {return_response.text}")
