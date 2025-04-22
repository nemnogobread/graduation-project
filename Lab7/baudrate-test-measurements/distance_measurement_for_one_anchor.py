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
    n = abs(signal_amplitude_0 - signal_amplitude_1) / (10 * h * math.log10(distance_0/distance_1))
    return n


if __name__ == "__main__":
    PATH = './'
    COLUMN = 'amp_steps_COM3'
    h = 21 * 1e-3
    csv_files = [file for file in os.listdir(PATH) if file.endswith('.csv')] # находим все csv файлы в директории
    files_number = int(len(csv_files))

    data_x_COM5 = [0 for i in range(files_number)]
    data_y_COM5 = [0 for i in range(files_number)]
    result_distance = [0 for i in range(files_number)]

    for i in range (0, len(csv_files)):
        filename = str(csv_files[i])
        parts = filename.split('_')
        index = int(parts[0]) - 1
        port = parts[2]
        distance = float(parts[4])
        signal_amplitude = calculate_signal_amplitude(filename)

        data_x_COM5[index] = distance
        data_y_COM5[index] = signal_amplitude

    base_distance_COM5 = data_x_COM5[3] # расстояние до COM5 3.0
    calibration_distance_COM5 = data_x_COM5[1] # расстояние до COM5 2.0

    base_amplitude_COM5 = data_y_COM5[3] # амлитуда COM5 на 3.0
    calibration_amplitude_COM5 = data_y_COM5[1] # амлитуда COM5 на 2.0

    n_COM5 = calculate_attenuation_rate(base_amplitude_COM5, calibration_amplitude_COM5, base_distance_COM5, calibration_distance_COM5)
    print(n_COM5)

    for i in range(0, files_number):
        if i == 1 or i == 3:
            pass
        else:
            dist_COM5 = base_distance_COM5 * pow(10, ( (base_amplitude_COM5 - data_y_COM5[i]) / (10 * h * n_COM5 )))
            result_distance[i] =  dist_COM5

    x = np.linspace(0.2, 1.0, 4)
    y = x
    plt.plot(x, y, label='y = x', color='blue', linestyle="--")

    data_x_COM5.pop(3)
    data_x_COM5.pop(1)
    result_distance.pop(3)
    result_distance.pop(1)

    error = 0
    for i in range(0, files_number - 2):
        error += abs(result_distance[i] - data_x_COM5[i])
    error/= files_number - 2
    print(error)
    plt.plot(data_x_COM5, result_distance, label="Расстояние")
    plt.xlabel("Реальное расстояние, м")
    plt.ylabel("Измеренное расстояние , м")
    plt.legend()
    plt.grid(True)
    plt.show()