import COM
import pandas as pd
import time
from main_2_nodes_request import make_signal_measurements

def calculate_distance(anchor, mobile_device, base_distance_to_anchor, base_amplitude_to_anchor, n_anchor, start_signal):
    h = 21 * 1e-3
    print(anchor, ": ", end='')
    amplitude_to_anchor = make_signal_measurements(mobile_device, start_signal)
    print('waiting 5 seconds', end='')
    for i in range(5):
        time.sleep(1)
        print('.', end='')
    print()

    dist_to_anchor = base_distance_to_anchor * pow(10, ((base_amplitude_to_anchor - amplitude_to_anchor) / (10 * h * n_anchor)))

    return dist_to_anchor

