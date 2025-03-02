from app import db, app
from models import Equipment

with app.app_context():
    equipment_seen = set()
    duplicates = []

    for equip in Equipment.query.all():
        if equip.name in equipment_seen:
            duplicates.append(equip)
        else:
            equipment_seen.add(equip.name)

    if duplicates:
        for equip in duplicates:
            db.session.delete(equip)
        db.session.commit()
        print(f"Removed {len(duplicates)} duplicate equipment items.")
    else:
        print("No duplicates found.")
    print("Database cleanup complete.")
    print("All equipment items are now unique in the database.")
