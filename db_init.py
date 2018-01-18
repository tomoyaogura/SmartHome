from app import app, db
from models import Device

DEFAULT_DEVICES = [ {'name': 'Water Heater', 'device_id': '302-1'},
                    {'name': 'Kotatsu', 'device_id': '302-2'},
                    {'name': 'LEDs', 'device_id': '302-4'},
                    {'name': 'Living Room', 'device_id': '302-5'}]

with app.app_context(): 
    db.create_all()
    for device in DEFAULT_DEVICES:
        db.session.add(Device(name=device['name'], device_id=device['device_id']))
    db.session.commit()
