import os
from time import sleep

import subprocess

from models import DeviceType, Device
import config
from database import db


def is_raspi():
    if os.path.isfile("/proc/device-tree/model"):
        with open("/proc/device-tree/model") as f:
            text = f.read()
            return 'raspberry pi' in text.lower()
    return False

IS_RASPI = False

def get_all_pins_used():
    # devices = Device.query.all()
    # pins = set()
    # for device in devices:
    #     if device.device_type in [DeviceType.LIGHT, DeviceType.FAN]:
    #         pins.add(device.on_code)
    #         pins.add(device.off_code)
    # return pins

    return [20, 21, 16, 26, 19, 13, 6, 12, 5, 1]

if is_raspi():
    IS_RASPI = True
    import RPi.GPIO as GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    pins = get_all_pins_used()
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)

else:
    pins = get_all_pins_used()
    for pin in pins:
        print('Setting up pin: {}'.format(pin))

def turn_on(device):
    if os.environ.get('DEBUG') or not IS_RASPI:
        message = 'Turning on:\n Device: {}\n Type: {}\n Code:{}'.format(device.name, device.device_type, device.on_code)
        print(message)
    else:
        if device.device_type == DeviceType.RF:
            _send_pulse(device.on_code)
        elif device.device_type in [DeviceType.LIGHT, DeviceType.FAN]:
            _pin_flicker(device.on_code)
        else:
            print('Unknown device type')
    Device.query.filter_by(id=device.id).update({'state': True})
    db.session.commit()

def turn_off(device):
    if os.environ.get('DEBUG') or not IS_RASPI:
        message = 'Turning off:\n Device: {}\n Type: {}\n Code:{}'.format(device.name, device.device_type, device.off_code)
        print(message)
    else:
        if device.device_type == DeviceType.RF:
            _send_pulse(device.off_code)
        elif device.device_type in [DeviceType.FAN, DeviceType.LIGHT]:
            _pin_flicker(device.off_code)
        else:
            print('Unknown device type')
    Device.query.filter_by(id=device.id).update({'state': False})
    db.session.commit()

# Flickers outlet_id
def flicker(outlet_id, on_duration=1):
    turn_on(outlet_id)
    time.sleep(on_duration)
    turn_off(outlet_id)

# Uses codesend to send_pulse
def _send_pulse(pulse_id):
    args = [config.CODESEND_DIR, '-l', str(config.PULSE), str(pulse_id)]
    subprocess.call(args)

def _pin_flicker(outlet_id):
    GPIO.output(int(outlet_id), True)
    sleep(0.5)
    GPIO.output(int(outlet_id), False)

