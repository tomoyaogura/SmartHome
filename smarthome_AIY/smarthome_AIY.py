#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Run a recognizer using the Google Assistant Library.

The Google Assistant Library has direct access to the audio API, so this Python
code doesn't need to record audio. Hot word detection "OK, Google" is supported.

The Google Assistant Library can be installed with:
    env/bin/pip install google-assistant-library==0.0.2

It is available for Raspberry Pi 2/3 only; Pi Zero is not supported.
"""

import logging
import sys

import aiy.assistant.auth_helpers
import aiy.voicehat
import requests
from google.assistant.library import Assistant
from google.assistant.library.event import EventType

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
)

ALL = [1, 2, 3, 4, 5, 6]
LIVING_ROOM = [4, 6]
POT = [1]
HEATER = [2]
LED = [3]
LAMP = [4]
BEDROOM = [5]
KITCHEN = [6]
KITCHEN_FAN_LOW = [7]
KITCHEN_FAN_MEDIUM = [8]
KITCHEN_FAN_HIGH = [9]
BEDROOM_FAN_LOW = [10]
BEDROOM_FAN_MEDIUM = [11]
BEDROOM_FAN_HIGH = [12]

ALLOWED_COMMANDS = {
    'all on': {'pins': ALL, 'state': True},
    'all off': {'pins': ALL, 'state': False},
    'living room on': {'pins': LIVING_ROOM, 'state': True},
    'living room off': {'pins': LIVING_ROOM, 'state': False},
    'bedroom on': {'pins': BEDROOM, 'state': True},
    'bedroom off': {'pins': BEDROOM, 'state': False},
    'heater on': {'pins': HEATER, 'state': True},
    'heater off': {'pins': HEATER, 'state': False},    
    'led on': {'pins': LED, 'state': True},
    'led off': {'pins': LED, 'state': False},   
    'lamp on': {'pins': LAMP, 'state': True},
    'lamp off': {'pins': LAMP, 'state': False},   
    'kitchen on': {'pins': KITCHEN, 'state': True},
    'kitchen off': {'pins': KITCHEN, 'state': False},   
    'water on': {'pins': POT, 'state': True},
    'water off': {'pins': POT, 'state': False},   
    'kitchen fan low': {'pins': KITCHEN_FAN_LOW, 'state': True},
    'kitchen fan medium': {'pins': KITCHEN_FAN_MEDIUM, 'state': True},
    'kitchen fan high': {'pins': KITCHEN_FAN_HIGH, 'state': True},
    'kitchen fan off': {'pins': KITCHEN_FAN_MEDIUM, 'state': False},    
    'bedroom fan low': {'pins': BEDROOM_FAN_LOW, 'state': True},
    'bedroom fan medium': {'pins': BEDROOM_FAN_MEDIUM, 'state': True},
    'bedroom fan high': {'pins': BEDROOM_FAN_HIGH, 'state': True},
    'bedroom fan off': {'pins': BEDROOM_FAN_MEDIUM, 'state': False},    
}

RASPI_HOST = 'http://192.168.1.74:5000'


def process_event(assisstant, event):
    status_ui = aiy.voicehat.get_status_ui()
    if event.type == EventType.ON_START_FINISHED:
        status_ui.status('ready')
        if sys.stdout.isatty():
            print('Say "OK, Google" then speak, or press Ctrl+C to quit...')

    elif event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        status_ui.status('listening')

    elif event.type == EventType.ON_END_OF_UTTERANCE:
        status_ui.status('thinking')

    elif event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED and event.args:
        print('You said:', event.args['text'])
        text = event.args['text'].lower()

        if text in ALLOWED_COMMANDS:
            assisstant.stop_conversation()
            for device in ALLOWED_COMMANDS[text]['pins']:
                url = "{}/api/v1/devices/{}".format(RASPI_HOST, device)
                requests.post(url, json={"state": ALLOWED_COMMANDS[text]['state']})

    elif event.type == EventType.ON_CONVERSATION_TURN_FINISHED:
        status_ui.status('ready')

    elif event.type == EventType.ON_ASSISTANT_ERROR and event.args and event.args['is_fatal']:
        sys.exit(1)


def main():
    credentials = aiy.assistant.auth_helpers.get_assistant_credentials()
    with Assistant(credentials) as assistant:
        for event in assistant.start():
            process_event(assistant, event)


if __name__ == '__main__':
    main()
