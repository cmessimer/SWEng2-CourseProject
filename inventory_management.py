import os  # Add this import at the top
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ✅ Corrected JWT_SECRET_KEY Assignment
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET", "fallback_secret_if_not_set")

db = SQLAlchemy(app)
jwt = JWTManager(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # Employee, Supervisor, Admin

class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='Available')  # Available, Checked Out, Maintenance

class Checkout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    checkout_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, default=lambda: datetime.utcnow() + timedelta(days=7))
    returned = db.Column(db.Boolean, default=False)

# Authentication Route
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username'], password=data['password']).first()
    if user:
        access_token = create_access_token(identity={'id': user.id, 'role': user.role})
        return jsonify(access_token=access_token)
    return jsonify({'message': 'Invalid credentials'}), 401

# Equipment Checkout
@app.route('/checkout', methods=['POST'])
@jwt_required()
def checkout_equipment():
    current_user = get_jwt_identity()
    data = request.json
    equipment = Equipment.query.get(data['equipment_id'])
    if not equipment or equipment.status != 'Available':
        return jsonify({'message': 'Equipment not available'}), 400
    
    new_checkout = Checkout(user_id=current_user['id'], equipment_id=equipment.id)
    equipment.status = 'Checked Out'
    db.session.add(new_checkout)
    db.session.commit()
    return jsonify({'message': 'Equipment checked out successfully'})

# Equipment Return
@app.route('/return', methods=['POST'])
@jwt_required()
def return_equipment():
    data = request.json
    checkout = Checkout.query.filter_by(equipment_id=data['equipment_id'], returned=False).first()
    if not checkout:
        return jsonify({'message': 'Invalid return request'}), 400
    
    checkout.returned = True
    equipment = Equipment.query.get(checkout.equipment_id)
    equipment.status = 'Available'
    db.session.commit()
    return jsonify({'message': 'Equipment returned successfully'})

# Overdue Equipment Notification (Triggered by a Scheduler)
def send_overdue_notifications():
    overdue_checkouts = Checkout.query.filter(Checkout.due_date < datetime.utcnow(), Checkout.returned == False).all()
    for checkout in overdue_checkouts:
        user = User.query.get(checkout.user_id)
        send_email(user.username, 'Overdue Equipment Alert', f'Your checked-out equipment is overdue. Please return it immediately.')

def send_email(to_email, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = 'noreply@inventorysystem.com'
    msg['To'] = to_email
    
    try:
        with smtplib.SMTP('smtp.example.com', 587) as server:
            server.starttls()
            server.login('your_email@example.com', 'your_password')
            server.sendmail('noreply@inventorysystem.com', to_email, msg.as_string())
    except Exception as e:
        print(f'Error sending email: {e}')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Initialize the database
    app.run(debug=True)
