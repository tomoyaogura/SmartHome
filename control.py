import os

import subprocess
import config

def turn_on(outlet_id):
    if os.environ.get('DEBUG'):
        print('ON!')
    else:
        _send_pulse(config.CODES[outlet_id][0])

def turn_off(outlet_id):
    if os.environ.get('DEBUG'):
        print('OFF!')
    else:
        _send_pulse(config.CODES[outlet_id][1])

# Flickers outlet_id
def flicker(outlet_id, on_duration=1):
    import time
    turn_on(outlet_id)
    time.sleep(on_duration)
    turn_off(outlet_id)

# Uses codesend to send_pulse
def _send_pulse(pulse_id):
    args = [config.CODESEND_DIR, '-l', str(config.PULSE), str(pulse_id)]
    subprocess.call(args)

