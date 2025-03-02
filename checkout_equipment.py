import requests

# Set API endpoints
login_url = "http://127.0.0.1:5000/login"
checkout_url = "http://127.0.0.1:5000/checkout"

# Step 1: Log in and get JWT token
login_data = {"username": "chad", "password": "newpassword456"}
login_response = requests.post(login_url, json=login_data)

if login_response.status_code == 200:
    token = login_response.json().get("access_token")
    print(f"Login successful! Token: {token}")

    # Step 2: Fetch Available Equipment
    headers = {"Authorization": f"Bearer {token}"}
    equipment_list_response = requests.get("http://127.0.0.1:5000/equipment", headers=headers)

    if equipment_list_response.status_code == 200:
        equipment_list = equipment_list_response.json()
        available_equipment = [e for e in equipment_list if e["status"] == "Available"]

        if not available_equipment:
            print("No available equipment to check out.")
        else:
            # Display available equipment
            print("\nAvailable Equipment:")
            for equip in available_equipment:
                print(f"ID: {equip['id']}, Name: {equip['name']}")

            # Ask user which equipment to check out
            equipment_id = input("\nEnter Equipment ID to check out: ").strip()

            # Step 3: Checkout Equipment
            try:
                equipment_id = int(equipment_id)
                checkout_data = {"equipment_id": equipment_id}
                checkout_response = requests.post(checkout_url, json=checkout_data, headers=headers)

                if checkout_response.status_code == 200:
                    print(f"Checkout Successful: {checkout_response.json()}")
                    #print equipment_id and name checked out successfully
                    for equip in available_equipment:
                        if equip['id'] == equipment_id:
                            print(f"Equipment ID {equipment_id} checked out successfully: {equip['name']}")
                            break
                    
                else:
                    print(f"Error: {checkout_response.status_code}, {checkout_response.text}")

            except ValueError:
                print("Invalid input. Please enter a numeric Equipment ID.")

    else:
        print(f"Error fetching equipment list: {equipment_list_response.status_code}, {equipment_list_response.text}")

else:
    print(f"Login Failed: {login_response.status_code}, {login_response.text}")
print("Checkout process completed.")
