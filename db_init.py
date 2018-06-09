from app import db
from runserver import app
from models import Device, DeviceType


DEFAULT_DEVICES = [ {'name': 'Water Heater', 'device_type': DeviceType.RF, 'on_code': 4543795, 'off_code': 4543804},
                    {'name': 'Kotatsu', 'device_type': DeviceType.RF, 'on_code': 4543939, 'off_code': 4543948}, 
                    {'name': 'LEDs', 'device_type': DeviceType.RF, 'on_code' :4545795, 'off_code': 4545804},
                    {'name': 'Living Room', 'device_type': DeviceType.RF, 'on_code' :4551939, 'off_code': 4551948},
                    {'name': 'Bedroom Light', 'device_type': DeviceType.LIGHT, 'on_code': 20, 'off_code': 20},
                    {'name': 'Kitchen Light', 'device_type': DeviceType.LIGHT, 'on_code': 21, 'off_code': 21},
                    {'name': 'Kitchen Fan: Low', 'device_type': DeviceType.FAN, 'on_code': 16, 'off_code': 26},
                    {'name': 'Kitchen Fan: Medium', 'device_type': DeviceType.FAN, 'on_code': 19, 'off_code': 26},
                    {'name': 'Kitchen Fan: High', 'device_type': DeviceType.FAN, 'on_code': 13, 'off_code': 26},  
                    {'name': 'Bedroom Fan: Low', 'device_type': DeviceType.FAN, 'on_code': 6, 'off_code': 12},
                    {'name': 'Bedroom Fan: Medium', 'device_type': DeviceType.FAN, 'on_code': 5, 'off_code': 12},
                    {'name': 'Bedroom Fan: High', 'device_type': DeviceType.FAN, 'on_code': 1, 'off_code': 12} ]

with app.app_context():
    db.create_all()
    for device in DEFAULT_DEVICES:
        db.session.add(Device(name=device['name'], on_code=device['on_code'], off_code=device['off_code'], device_type=device['device_type']))
    db.session.commit()
