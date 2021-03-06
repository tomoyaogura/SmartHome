from app import db
from runserver import app
from models import Device, DeviceType

DEFAULT_DEVICES = [ {'name': 'Water Heater', 'device_id': '302-1', 'device_type': DeviceType.RF},
                    {'name': 'Kotatsu', 'device_id': '302-2', 'device_type': DeviceType.RF},
                    {'name': 'LEDs', 'device_id': '302-4', 'device_type': DeviceType.RF},
                    {'name': 'Living Room', 'device_id': '302-5', 'device_type': DeviceType.RF},
                    {'name': 'Bedroom Light', 'device_id': 'L-20', 'device_type': DeviceType.FAN},
                    {'name': 'Kitchen Light', 'device_id': 'L-21', 'device_type': DeviceType.FAN}]

with app.app_context():
    db.create_all()
    for device in DEFAULT_DEVICES:
        db.session.add(Device(name=device['name'], device_id=device['device_id'], device_type=device['device_type']))
    db.session.commit()
