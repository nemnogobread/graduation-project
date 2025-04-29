import COM
import pandas as pd
import time
from main_2_nodes_request import make_measurements

def calculate_distance(anchor, mobile_device,
                       base_distance_to_anchor, base_amplitude_to_anchor, n_anchor):
    start_signal_for_anchors = {"COM5": 120, "COM6": 140}
    h = 21 * 1e-3
    print(anchor, ": ", end='')
    amplitude_to_anchor = make_measurements(mobile_device, anchor, start_signal_for_anchors[anchor])
    print('waiting 5 seconds', end='')
    for i in range(5):
        time.sleep(1)
        print('.', end='')

    dist_to_anchor = base_distance_to_anchor * pow(10, ((base_amplitude_to_anchor - amplitude_to_anchor) / (10 * h * n_anchor)))

    # pos_mobile_device =  (dist_to_anchor1 + (pos_anchor2 - pos_anchor1) - dist_to_anchor2) / 2

    return dist_to_anchor

