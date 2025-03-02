from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User, Equipment, Checkout
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from config import Config
from werkzeug.security import generate_password_hash, check_password_hash

# Create Blueprint
api_routes = Blueprint('api_routes', __name__)

# User Registration Route
@api_routes.route('/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 400

    position = data.get("position", "Employee")  # Default position
    hashed_password = generate_password_hash(data['password'])
    new_user = User(username=data['username'], password=hashed_password, position=position, role=data.get("role", "Employee"))

    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'})

# Login Route
@api_routes.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()

    if user:
        print(f"Debug: Hashed Password from DB: {user.password}")  # Shows stored hash
        print(f"Debug: Entered Password: {data['password']}")  # Shows entered password
        if check_password_hash(user.password, data['password']):
            print("Password verified!")  # Debugging line
        else:
            print("Password check failed!")  #  Debugging line

    if user and check_password_hash(user.password, data['password']):  # Compare hashed password
        access_token = create_access_token(identity={"id": user.id, "role": user.role})
        return jsonify(access_token=access_token)

    print("Returning 401 Unauthorized")  # Debugging line
    return jsonify({'message': 'Invalid credentials'}), 401

# List All Equipment
@api_routes.route('/equipment', methods=['GET'])
@jwt_required()
def get_equipment():
    equipment_list = Equipment.query.all()
    return jsonify([{"id": e.id, "name": e.name, "status": e.status} for e in equipment_list])

# Checkout Equipment
@api_routes.route('/checkout', methods=['POST'])
@jwt_required()
def checkout_equipment():
    current_user = get_jwt_identity()  # Extract user dictionary
    user_id = current_user["id"]
    
    data = request.json
    equipment = Equipment.query.get(data['equipment_id'])
    
    if not equipment:
        return jsonify({'message': 'Equipment ID not found'}), 404
    if equipment.status != 'Available':
        return jsonify({'message': 'Equipment is not available'}), 400

    new_checkout = Checkout(user_id=user_id, equipment_id=equipment.id, due_date=datetime.utcnow() + timedelta(days=7))
    equipment.status = 'Checked Out'
    
    db.session.add(new_checkout)
    db.session.commit()
    
    return jsonify({'message': f'Equipment ID {equipment.id} checked out successfully'})

# Return Equipment (Check-in)
@api_routes.route('/return', methods=['POST'])
@jwt_required()
def return_equipment():
    current_user = get_jwt_identity()  # Extract user dictionary
    user_id = current_user["id"]
    
    data = request.json
    equipment_id = data.get("equipment_id")

    # Find the active checkout entry for this equipment
    checkout = Checkout.query.filter_by(equipment_id=equipment_id, returned=False).first()

    if not checkout:
        return jsonify({'message': 'Equipment was not checked out or is already returned'}), 400

    if checkout.user_id != user_id:  # Check correct user
        return jsonify({'message': 'You can only return equipment you checked out'}), 403

    # Mark as returned
    checkout.returned = True
    equipment = Equipment.query.get(equipment_id)
    equipment.status = "Available"

    db.session.commit()
    return jsonify({'message': f'Equipment ID {equipment_id} has been returned successfully'})

# Email Notification Function
def send_email(to_email, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = Config.SMTP_EMAIL
    msg['To'] = to_email
    
    try:
        with smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT) as server:
            server.starttls()
            server.login(Config.SMTP_EMAIL, Config.SMTP_PASSWORD)
            server.sendmail(Config.SMTP_EMAIL, to_email, msg.as_string())
    except smtplib.SMTPException as e:
        print(f'Email sending failed: {e}')
