from sys import argv

import pyvisa
import pandas as pd
import numpy as np
import time

#params = argv
#script, PATH, filename, data_start, data_stop, channels = params[0], params[1], params[2], int(params[3]), int(params[4]), params[5:]

#print(PATH, filename, data_start, data_stop, channels)
#PATH, filename, channels, data_start, data_stop = argv
channels = ['CH2']
data_start = 1
data_stop = 10000000
PATH = './'
filename = 'data_100'

rm = pyvisa.ResourceManager()
rm.list_resources()
scope = rm.open_resource('USB0::0x0699::0x0401::C010802::INSTR')
print(scope.query('*IDN?'))

start = time.time() ## точка отсчета времени

scope.write('ACQuire:STOPAfter SEQuence') # Снимает данные кусками, чтоб на всех каналах одновременно
scope.write('ACQuire:MODe SAMple') # Режим оцифровки
scope.write(':DATa:STARt ' + str(data_start)) # Номер первого отсчета
scope.write(':DATa:STOP ' + str(data_stop)) # Номер последнего отсчета
scope.write(':DATa:ENCdg SRIbinary') # Формат передаваемых данных
#scope.write(':DATa:WFMOutpre:BN_Fmt RI')
#scope.write(':DATa:WFMOutpre:BYT_Or MSB')
scope.write(':DATa:WIDth 1') # Разраядность передаваемых данных
scope.write(':HEADer 0') # Отключить справочную информацию при передаче данных

values_list = []
params_list = []
columns = ['time'] + [chnl for chnl in channels]
tm = [x for x in range(data_stop - data_start + 1)]
values_list.append(tm)

for chnl in channels:
    print(chnl)
    scope.write(':DATa:SOUrce ' + chnl) # Номер канала, с которого снимаются данные
    scope.query(':WFMOutpre?') # Получение справочных данных
    NR_pt = int(scope.query(':WFMOutpre:NR_pt?')) # Число точек
    XUNit = str(scope.query(':WFMOutpre:XUNit?'))[1:-2] # Единица измерения по оси X
    XZEro = float(scope.query(':WFMOutpre:XZEro?')) # 
    XINcr = float(scope.query(':WFMOutpre:XINcr?')) # 
    YUNit = str(scope.query(':WFMOutpre:YUNit?'))[1:-2] # Единица измерения по оси Y
    YZEro = float(scope.query(':WFMOutpre:YZEro?')) #
    YMUlt = float(scope.query(':WFMOutpre:YMUlt?')) # 
    YOFf = float(scope.query('WFMOutpre:YOFf?'))
    BYT_nr = int(scope.query(':WFMOutpre:BYT_nr?')) # Число байт
    print('Number of data points:', NR_pt)
    print('XUNit:', XUNit, 'XZEro:', XZEro, 'XINcr:', XINcr)
    print('YUNit:', YUNit, 'YZEro:', YZEro, 'YOFf:', YOFf, 'YMUlt:', YMUlt)
    print('BYT_nr:', BYT_nr)
    params_list.append([chnl, NR_pt, XUNit, XZEro, XINcr, YUNit, YZEro, YOFf, YMUlt, BYT_nr])

    values = scope.query_binary_values('CURV?', datatype='b', is_big_endian=True)
    values_list.append(values)
    
#scope.write('*TRG')
params = pd.DataFrame(params_list, columns = ['CHNL', 'NR_pt', 'XUNit', 'XZEro', 'XINcr', 'YUNit', 'YZEro', 'YOFf', 'YMUlt', 'BYT_nr'])
params.to_csv(PATH + filename + '_params' + '.csv', index=False)

res = pd.DataFrame(data = np.array(values_list).T, columns = columns)
res.to_csv(PATH + filename + '.csv', index=False)

end = time.time() - start ## собственно время работы программы
print(end) ## вывод времени
print('Done')

scope.write('FPAnel:PRESS RUnstop')
#scope.write('*DDT ACQuire:STOPAfter SEQuence') # Снимает данные кусками, чтоб на всех каналах одновременно
#scope.write('*TRG')
