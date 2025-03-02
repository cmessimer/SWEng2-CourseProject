import tkinter as tk
from tkinter import messagebox
import requests

# API Endpoint
LOGIN_URL = "http://127.0.0.1:5000/login"

def attempt_login():
    username = entry_username.get()
    password = entry_password.get()
    print(f"Sending: Username={username}, Password={password}")  # Debugging line

    if not username or not password:
        messagebox.showerror("Error", "Please enter both username and password")
        return

    login_data = {"username": username, "password": password}
    response = requests.post(LOGIN_URL, json=login_data)
    print(f"Response: {response.status_code}, {response.text}")  # Debugging line

    if response.status_code == 200:
        token = response.json().get("access_token")
        messagebox.showinfo("Login Successful", "You are now logged into the Equipment Management System!")
        root.destroy()  # Close window on success
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

# Create GUI window
root = tk.Tk()
root.title("Inventory Login")
root.geometry("300x200")

# Username Label & Entry
tk.Label(root, text="Username:").pack(pady=5)
entry_username = tk.Entry(root)
entry_username.pack(pady=5)

# Password Label & Entry
tk.Label(root, text="Password:").pack(pady=5)
entry_password = tk.Entry(root, show="*")  # Hide password input
entry_password.pack(pady=5)

# Login Button
login_button = tk.Button(root, text="Login", command=attempt_login)
login_button.pack(pady=10)

# Run GUI
root.mainloop()
# print("Login process completed.")
# Note: This script assumes the Flask server is running and accessible at the specified URL.
# Ensure the server is running before executing this script.
