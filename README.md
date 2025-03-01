# CEIS 400 SWENG Equipment Management How-to Guide

## Overview
The Equipment Management System is a Flask-based web application that enables users to log in, check out equipment, return equipment, and prevent duplicate entries in the database. The system utilizes Flask, Flask-JWT-Extended for authentication, Flask-SQLAlchemy for database management, and Flask-Migrate for handling database migrations.

## Local Setup
Clone the repository from:  
[GitHub Repository](https://github.com/cmessimer/SWEng2-CourseProject)

## Setup Virtual Environment
Create the virtual environment (If already created, skip to activation step):
`python -m venv venv`

### Activate the virtual environment
Windows: 
`venv\Scripts\activate
`

macOS/Linux:
`source venv/bin/activate
`

To exit the virtual environment:
`deactivate
`

## Package Management
Update the requirements.txt file if changes are made:
`pip freeze > requirements.txt
`

Install dependencies from requirements.txt:
`pip install -r requirements.txt
`

To exit the virtual environment:
Command:
`deactivate
`

## Generate a JWT Secret
Generate a secret key:
`python -c "import secrets; print(secrets.token_hex(32))"
`

Store the key (Windows):
`$env:JWT_SECRET="insertYourSecret"
`

## Initialize Database
Command:
`python setup_db.py
`

## Run Inventory Management
Command: 
`python inventory_management.py
`

## Test the API
`curl -X POST http://127.0.0.1:5000/checkout \
     -H "Authorization: Bearer insertTokenName" \
     -H "Content-Type: application/json" \
     -d '{"equipment_id": 1}'
`

`curl -X POST "http://127.0.0.1:5000/checkout" -H "Authorization: Bearer insertYourToken application/json" -d "{\"equipment_id\":1}" -v`

## Start the Flask App
Command: 
`python app.py
`

Initialize Flask-Migrate:
`python -m flask db init
python -m flask db migrate -m "Initial migration"
python -m flask db upgrade
`

## Debugging Commands
Check if flask-migrate is installed (PowerShell):
`pip list | Select-String Flask-Migrate
`

## Equipment Checkout
Equipment checkout is handled via checkout_equipment.py. The script currently checks out equipment with ID: 1 (a laptop).

Ensure the Flask app is running or restart it:
`python app.py
`

Run the checkout script:
`python checkout_equipment.py
`

## Successful Checkout
A successful checkout should return confirmation of the transaction:
![image](https://github.com/user-attachments/assets/12034118-07ff-497a-825f-290ecf39db20)

## General Notes
Based on the Flask-Migrate documentation, the following configuration was needed:
`app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
`

## Resources
For more details, refer to the following documents:
- https://flask-migrate.readthedocs.io/en/latest/
- https://docs.python.org/3/library/tkinter.html
- https://flask.palletsprojects.com/en/stable/
- https://flask-migrate.readthedocs.io/en/latest/
- https://pub.dev/documentation/libsimple_flutter/latest/sqlite_web/SqliteImpl-class.html
- https://www.sqlalchemy.org/
