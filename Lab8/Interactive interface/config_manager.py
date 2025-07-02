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
        "anchor1": 'COM5',
        "anchor2": 'COM4',
        "mobile_device": 'COM3',
        "start_signal": {"COM5": 120, "COM4": 140},
        "anchor_position": {"COM5": [0.75, 0.07], "COM4": [0.00, 0.56]},
        "base_distance": {"COM5": -1.0, "COM4": -1.0},
        "base_amplitude": {"COM5": -1.0, "COM4": -1.0},
        "calibration_amplitude": {"COM5": -1.0, "COM4": -1.0},
        "calibration_distance": {"COM5": -1.0, "COM4": -1.0},
        "distance": {"COM5": -1.0, "COM4": -1.0},
        "n_rate": {"COM5": -1.0, "COM4": -1.0}
    }