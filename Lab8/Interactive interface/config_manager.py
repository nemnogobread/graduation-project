import json
import os

CONFIG_FILE = "app_config.json"

def save_config(data):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return None
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def get_default_config():
    return {
        "anchor1": 'COM8',
        "anchor2": 'COM6',
        "mobile_device": 'COM3',
        "start_signal": {"COM8": 180, "COM6": 160},
        "anchor_position": {"COM8": [2, 0], "COM6": [0, -2]},
        "base_distance": {"COM8": -1.0, "COM6": -1.0},
        "base_amplitude": {"COM8": -1.0, "COM6": -1.0},
        "calibration_amplitude": {"COM8": -1.0, "COM6": -1.0},
        "calibration_distance": {"COM8": -1.0, "COM6": -1.0},
        "distance": {"COM8": -1.0, "COM6": -1.0},
        "n_rate": {"COM8": -1.0, "COM6": -1.0}
    }