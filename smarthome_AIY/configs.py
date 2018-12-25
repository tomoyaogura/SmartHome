# Pin Mappings
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

# Mapping of commands and state
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
