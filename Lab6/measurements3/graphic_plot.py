import math
import os
import matplotlib.pyplot as plt

import pandas as pd
from matplotlib.pyplot import title


def calculate_signal_amplitude(filename):
    data = pd.read_csv(PATH + filename)
    data = data['amp_steps_COM3'] / 4096 * 3.3

    return sum(data)/len(data)

def calculate_attenuation_rate(filename_0, filename_1, distance_0, distance_1):
    signal_amplitude_0 = calculate_signal_amplitude(filename_0)
    signal_amplitude_1 = calculate_signal_amplitude(filename_1)
    n = (signal_amplitude_0 - signal_amplitude_1) / (10 * h * math.log10(distance_1/distance_0))
    return n


if __name__ == "__main__":
    PATH = './'
    COLUMN = 'amp_steps_COM3'
    csv_files = [file for file in os.listdir(PATH) if file.endswith('.csv')] # находим все csv файлы в директории
    files_number = int(len(csv_files)/2)
    data_x = [0 for i in range(files_number)]
    data_y_COM5 = [0 for i in range(files_number)]
    data_y_COM6 = [0 for i in range(files_number)]
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

    plt.plot(data_x, data_y_COM5, label="Якорь 2")
    plt.plot(data_x, data_y_COM6, label="Якорь 1")
    plt.xlabel("x, м")
    plt.ylabel("A, В")
    plt.legend()
    plt.grid(True)
    plt.show()