import math
import os
import matplotlib.pyplot as plt

import pandas as pd


def calculate_signal_amplitude(filename):
    data = pd.read_csv(PATH + filename)
    data_size = data.size
    data = data['amp_steps_COM3'] / 4096 * 3.3

    return sum(data)/len(data)

def calculate_attenuation_rate(filename_0, filename_1, distance_0, distance_1):
    signal_amplitude_0 = calculate_signal_amplitude(filename_0)
    signal_amplitude_1 = calculate_signal_amplitude(filename_1)
    n = (signal_amplitude_0 - signal_amplitude_1) / (10 * h * math.log10(distance_1/distance_0))
    return n

PATH = './'
COLUMN = 'amp_steps_COM3'
data = []
distance = [0.25, 0.50, 0.75, 1.00]
h = 21 * 1e-3
csv_files = [file for file in os.listdir(PATH) if file.endswith('.csv')] # находим все csv файлы в директории
n = calculate_attenuation_rate(csv_files[0], csv_files[1], distance[0], distance[1]) # считаем коэф. затухания сигнала по двум измерениям
print(csv_files)

print("\nattenuation_rate: ", round(n, 2))

base_amplitude = calculate_signal_amplitude(csv_files[0])
data.append(base_amplitude)
data.append(calculate_signal_amplitude(csv_files[1]))

for i in range (2, len(csv_files)):
    signal_amplitude = calculate_signal_amplitude(csv_files[i])
    data.append(signal_amplitude)
    result_distance = distance[0] * pow(10, ( (base_amplitude - signal_amplitude) / (10 * h * n )))
    print("for", csv_files[i], "distance is", round(result_distance, 2))

plt.plot(distance, data)
plt.show()