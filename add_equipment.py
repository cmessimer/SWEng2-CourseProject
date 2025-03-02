from app import db, app
from models import Equipment

# List of equipment names
equipment_list = [
    "Laptop", "Desktop", "Monitor", "Keyboard", "Mouse",
    "Printer", "Projector", "Router", "Switch", "Tablet",
    "Headphones", "Microphone", "External Hard Drive", "USB Flash Drive",
    "Docking Station", "Smartphone", "Graphics Tablet", "VR Headset",
    "Camera", "Speaker"
]

with app.app_context():
    # Fetch existing equipment names (case insensitive)
    existing_equipment_names = {equip.name.lower() for equip in Equipment.query.all()}

    new_equipment = []
    for name in equipment_list:
        if name.lower() not in existing_equipment_names:  # Prevent duplicates
            new_equipment.append(Equipment(name=name, status="Available"))  # Ensure "Available"

    if new_equipment:
        db.session.bulk_save_objects(new_equipment)
        db.session.commit()
        print(f"{len(new_equipment)} new equipment items added successfully!")
    else:
        print("⚠ No new equipment added (duplicates detected).")
