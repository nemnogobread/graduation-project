# Измерение уровня мошности сигнала.
# Осуществляет последовательный опрос нескольких приемников, подключенных к ПК.
# Результаты считываются короткими пакетами.

import COM
import pandas as pd
import time
from main_2_nodes_request import make_measurements

def calculate_distance(anchor1, anchor2, mobile_device, pos_anchor1, pos_anchor2,
                       base_distance_to_anchor1, base_amplitude_to_anchor1, n_anchor_1,
                       base_distance_to_anchor2, base_amplitude_to_anchor2, n_anchor_2):
    start_signal_for_anchor1 = 120
    start_signal_for_anchor2 = 140
    h = 21 * 1e-3
    print(anchor1, ": ", end='')
    amplitude_to_anchor1 = make_measurements(mobile_device, anchor1, start_signal_for_anchor1)
    print('waiting 10 seconds', end='')
    for i in range(10):
        time.sleep(1)
        print('.', end='')
    print('\n', anchor2, ": ", end='')
    amplitude_to_anchor2 = make_measurements(mobile_device, anchor2, start_signal_for_anchor2)

    dist_to_anchor1 = base_distance_to_anchor1 * pow(10, ((base_amplitude_to_anchor1 - amplitude_to_anchor1) / (10 * h * n_anchor_1)))
    dist_to_anchor2 = base_distance_to_anchor2 * pow(10, ((base_amplitude_to_anchor2 - amplitude_to_anchor2) / (10 * h * n_anchor_2)))

    pos_mobile_device =  (dist_to_anchor1 + (pos_anchor2 - pos_anchor1) - dist_to_anchor2) / 2

    return pos_mobile_device

