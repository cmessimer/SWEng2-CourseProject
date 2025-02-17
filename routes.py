from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User, Equipment, Checkout
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from config import Config
from werkzeug.security import generate_password_hash, check_password_hash

# Create Blueprint
api_routes = Blueprint('api_routes', __name__)

# User Registration Route (Optional, for testing)
@api_routes.route('/register', methods=['POST'])
def register():
    data = request.json

    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 400

    # Ensure 'position' is provided, or set a default value
    position = data.get("position", "Employee")  # Default to 'Employee' if not provided

    hashed_password = generate_password_hash(data['password'])
    new_user = User(username=data['username'], password=hashed_password, position=position, role=data.get("role", "Employee"))

    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'})

# Login Route (Get JWT Token)
@api_routes.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()

    if user and check_password_hash(user.password, data['password']):  
        access_token = create_access_token(identity=str(user.id))  # ✅ Convert ID to a string
        return jsonify(access_token=access_token)

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
    current_user_id = int(get_jwt_identity())  # ✅ Convert back to an integer
    data = request.json
    equipment = Equipment.query.get(data['equipment_id'])
    
    if not equipment:
        return jsonify({'message': 'Equipment ID not found'}), 404
    if equipment.status != 'Available':
        return jsonify({'message': 'Equipment is not available'}), 400

    new_checkout = Checkout(user_id=current_user_id, equipment_id=equipment.id)
    equipment.status = 'Checked Out'
    
    db.session.add(new_checkout)
    db.session.commit()
    
    return jsonify({'message': 'Equipment checked out successfully'})

# Return Equipment
@api_routes.route('/return', methods=['POST'])
@jwt_required()
def return_equipment():
    current_user = get_jwt_identity()
    data = request.json
    checkout = Checkout.query.filter_by(equipment_id=data['equipment_id'], returned=False).first()
    
    if not checkout:
        return jsonify({'message': 'Invalid return request'}), 400
    if checkout.user_id != current_user['id']:  # Prevents unauthorized returns
        return jsonify({'message': 'You can only return equipment you checked out'}), 403

    checkout.returned = True
    equipment = Equipment.query.get(checkout.equipment_id)
    equipment.status = 'Available'

    db.session.commit()
    return jsonify({'message': 'Equipment returned successfully'})

# Email Notification Function (Fixed Line Break Issue)
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
