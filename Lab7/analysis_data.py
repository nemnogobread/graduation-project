import matplotlib.pyplot as plt
import pandas as pd

PATH = './baudrate-test-measurements/'
filename = '0_measurements_COM5_on_0.3_meters'
#filename = 'test'
data = pd.read_csv(PATH + filename + '.csv')
data_size = 4000
threshold = 1.28
high_signal = []
#print(data)
data = data['amp_steps_COM3'] / 4096 * 3.3
#
# for i in range(data_size):
#     if data[i] >= threshold:
#         high_signal.append(data[i])

print("среднее: ", sum(data)/len(data))
plt.plot(data)
plt.show()
