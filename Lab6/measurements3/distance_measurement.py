import math
import os
import matplotlib.pyplot as plt
import numpy as np

import pandas as pd
from matplotlib.pyplot import title

def calculate_signal_amplitude(filename):
    data = pd.read_csv(PATH + filename)
    data = data['amp_steps_COM3'] / 4096 * 3.3

    return sum(data)/len(data)

def calculate_attenuation_rate(signal_amplitude_0, signal_amplitude_1, distance_0, distance_1):
    n = abs(signal_amplitude_0 - signal_amplitude_1) / (10 * h * math.log10(distance_1/distance_0))
    return n


if __name__ == "__main__":
    PATH = './'
    COLUMN = 'amp_steps_COM3'
    x_pos_COM5 = 5 # координата COM5 якоря
    x_pos_COM6 = 0 # координата COM6 якоря
    csv_files = [file for file in os.listdir(PATH) if file.endswith('.csv')] # находим все csv файлы в директории
    files_number = int(len(csv_files)/2)
    data_x = [0 for i in range(files_number)]
    data_y_COM5 = [0 for i in range(files_number)]
    data_y_COM6 = [0 for i in range(files_number)]
    temp_COM5 = [0 for i in range(files_number)]
    temp_COM6 = [0 for i in range(files_number)]
    result_distance = [0 for i in range(files_number)]
    h = 21 * 1e-3
    print(len(csv_files))

    for i in range (0, len(csv_files)):
        filename = str(csv_files[i])
        parts = filename.split('_')
        index = int(parts[0])
        port = parts[2]
        distance = float(parts[4])
        signal_amplitude = calculate_signal_amplitude(filename)

        data_x[index-1] = distance
        if port == "COM5":
            data_y_COM5[index-1] = signal_amplitude
        if port == "COM6":
            data_y_COM6[index-1] = signal_amplitude

    print(data_x)

    # data_x[6] = 2.0, data_x[6] = 3.0 - калибровочные расстояния
    n_COM5 = calculate_attenuation_rate(data_y_COM5[6], data_y_COM5[10], data_x[6], data_x[10])
    n_COM6 = calculate_attenuation_rate(data_y_COM6[6], data_y_COM6[10], data_x[6], data_x[10])
    print(n_COM5)
    print(n_COM6)

    base_amplitude_COM5 = data_y_COM5[6]
    base_amplitude_COM6 = data_y_COM6[10]

    for i in range(0, files_number):
        if i == 6 or i == 10:
            pass
        else:
            dist_COM5 = data_x[10] * pow(10, ( (base_amplitude_COM5 - data_y_COM5[i]) / (10 * h * n_COM5 )))
            dist_COM6 = data_x[10] * pow(10, ( (base_amplitude_COM6 - data_y_COM6[i]) / (10 * h * n_COM6 )))
            temp_COM5[i] = 5 - dist_COM5
            temp_COM6[i] = dist_COM6
            x_min = max(x_pos_COM5 - dist_COM5, x_pos_COM6 - dist_COM6)
            x_max = min(x_pos_COM5 + dist_COM5, x_pos_COM6 + dist_COM6)
            result_distance[i] =  (dist_COM6 + 5 - dist_COM5) / 2

    x = np.linspace(0.5, 4.5, 4)
    y = x
    plt.plot(x, y, label='y = x', color='blue', linestyle="--")

    data_x.pop(10)
    data_x.pop(6)
    result_distance.pop(10)
    result_distance.pop(6)

    temp_COM5.pop(10)
    temp_COM5.pop(6)
    temp_COM6.pop(10)
    temp_COM6.pop(6)

    error = 0
    for i in range(0, 15):
        error += abs(result_distance[i] - data_x[i])
    error/= 15
    print(error)
    #plt.plot(data_x, temp_COM6, label="COM6")
    #plt.plot(data_x, temp_COM5, label="COM5")
    plt.plot(data_x, result_distance, label="distance")
    plt.legend()
    plt.grid(True)
    plt.show()