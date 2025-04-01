import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statistics
import math
import seaborn as sns

data_size = 10000000
periods = []
durations = []
is_signal = False
begin_signal_time = 0
previos_begin_signal_time = 0
end_signal_time = 0
np.append(periods, 0)

PATH = './'
filename = 'data_025'
channels = ['CH2']
params = pd.read_csv(PATH + filename + '_params' + '.csv')
dt = pd.read_csv(PATH + filename + '.csv')
data = pd.DataFrame(columns = dt.columns)
threshold = 1.28
point_signal_starts = 4900000
sum = 0
num = 0

CHNL, NR_pt, XUNit, XZEro, XINcr, YUNit, YZEro, YOFf, YMUlt, BYT_nr = params.iloc[0]
data['time'] = [(XZEro + XINcr * (x - 1))*10e8 for x in range(len(dt['time']))] #X = XZEro + XINcr * (i - 1)

for ii in range(len(channels)):
    # print(ii)
    CHNL, NR_pt, XUNit, XZEro, XINcr, YUNit, YZEro, YOFf, YMUlt, BYT_nr = params.iloc[ii]
    data[channels[ii]] = [(YZEro + YMUlt*(y - YOFf)) for y in dt[channels[ii]]]  #Value in YUNit units = ((curve_in_dl - YOFf) * YMUlt) + YZEro

for i in range(int(point_signal_starts), data_size):
    if (abs(data['CH2'][i]) >= threshold):
        sum += data['CH2'][i]
        num += 1

#periods.pop(0)
#print(durations)
# print('Среднее значение периода: ', round(statistics.mean(periods)), ' нс.'
#         ' Среднеквадратичное отклонение: ', round(math.sqrt(statistics.variance(periods))), ' нс', sep='')
# print('Среднее значение длительности: ', round(statistics.mean(durations)), ' нс.'
#         ' Среднеквадратичное отклонение: ', round(math.sqrt(statistics.variance(durations))), ' нс', sep='')

print(sum/num)
plt.plot(data['time'], data['CH2'])
plt.axvline(data['time'][point_signal_starts])
#plt.hist(periods, color = 'blue', edgecolor = 'black', bins = len(periods))
plt.show()
