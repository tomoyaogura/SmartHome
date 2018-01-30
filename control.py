import os
from time import sleep

import subprocess

from models import DeviceType
import config


def is_raspi():
    if os.path.isfile("/proc/device-tree/model"):
        with open("/proc/device-tree/model") as f:
            text = f.read()
            return 'raspberry pi' in text.lower()
    return False

IS_RASPI = False

if is_raspi():
    IS_RASPI = True
    import RPi.GPIO as GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(21, GPIO.OUT)

def turn_on(outlet_id, device_type):
    if os.environ.get('DEBUG') or not IS_RASPI:
        print('ON!')
    else:
        if device_type == DeviceType.RF:
            _send_pulse(config.CODES[outlet_id][0])
        elif device_type == DeviceType.FAN:
            if outlet_id.split('-')[0] == 'L':
                _pin_flicker(int(outlet_id.split('-')[1]))
        else:
            print('Unknown device type')

def turn_off(outlet_id, device_type):
    if os.environ.get('DEBUG') or not IS_RASPI:
        print('OFF!')
    else:
        if device_type == DeviceType.RF:
            _send_pulse(config.CODES[outlet_id][1])
        elif device_type == DeviceType.FAN:
            if outlet_id.split('-')[0] == 'L':
                _pin_flicker(int(outlet_id.split('-')[1]))
        else:
            print('Unknown device type')

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
    GPIO.output(outlet_id, True)
    sleep(0.5)
    GPIO.output(outlet_id, False)

