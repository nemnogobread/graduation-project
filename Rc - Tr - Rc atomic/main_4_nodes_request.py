# Измерение уровня мошности сигнала.
# Осуществляет последовательный опрос нескольких приемников, подключенных к ПК.
# Результаты считываются короткими пакетами.


import COM
from   win_dev_list import get_com_dev_list
import pandas as pd
import numpy as np
import time

start = time.time() ## точка отсчета времени


PATH = 'C:/Users/infor/OneDrive/Рабочий стол/GlebMarat/Lab5/' # Директория, в которой будет храниться файл с результатами измерений
filename = 'measurements_on_100_meters_with_4000_points' # Файл с результатами измерений
meas = 1 # Номер файла, если делаем несколько серий измерений в одной точке
#filename = 'test' # Название файла с измерениями фонового шума

HOST_DEV    = 0

start_signal = 120;
baudrate = 2000000 #115200 #1200 #115200 #1000000 # Скорость COM - порта
num_points_to_read = 4000 # Число измерений в серии
req_len = 100 # Программа запрашивает у приемника измерения
              # короткими сериями (пакетами). Это длина такого пакета

num_cycles = int(num_points_to_read/req_len)  # Число считываний пакетов
print('num_cycles:', num_cycles)

# Проверяем, какие устройства подключены к COM-порту
# Connecting to STM32F334R8 RxTx modules
print("Connected devices:")
com_list = get_com_dev_list()
print(com_list)

com_list = ['COM3']
# В это датафрейме хранятся результаты измерений
result = pd.DataFrame(columns = ['amp_steps_' + com_port for com_port in com_list])
COM.serial_port_init_config(HOST_DEV, 'COM3', baudrate) # Задаем параметры COM-порта и открываем порт
COM.send_request(start_signal, HOST_DEV)
while COM.get_answer(HOST_DEV) != (str(req_len) + '\n').encode():  # Шлем запросы, пока не получим подтверждение
    COM.reset_serial(HOST_DEV)
    COM.send_request(req_len, HOST_DEV)
COM.close_serial(HOST_DEV)


res_tmp = []
if com_list != []:
    for ii in range(num_cycles):
        res_list = []
        for  nn, com_port in enumerate(com_list): # Опрашиваем последовательно каждый из приемников
            COM.serial_port_init_config(HOST_DEV, com_port, baudrate) # Задаем параметры COM-порта и открываем порт
            COM.send_request(req_len, HOST_DEV) # Шлем запрос приемнику, указывая число измерений (длину пакета), которые он должен сделать
            while COM.get_answer(HOST_DEV) != (str(req_len)+'\n').encode(): # Шлем запросы, пока не получим подтверждение
                COM.reset_serial(HOST_DEV)
                COM.send_request(req_len, HOST_DEV)

            test_com_buf = COM.check_buf(HOST_DEV) # Ждем, пока в буфере не накопится весь пакет
            while test_com_buf < 8 * req_len: #while test_com_buf != 8 * req_len:
                test_com_buf = COM.check_buf(HOST_DEV)

            serialStream = COM.read_packet(req_len, HOST_DEV) # Считываем пакет
            print('.', end='')

            res_list.append(serialStream)  # Сохраняем результат
            COM.close_serial(HOST_DEV) # Закрываем порт, идем опрашивать следующий

        res_tmp = pd.DataFrame(res_list).T # Сохраняем результаты
        res_tmp.columns = ['amp_steps_' + com_port for com_port in com_list]
        result = pd.concat([result, res_tmp], axis=0, ignore_index=True)


    print("\n", time.time() - start)
    result.to_csv(PATH + filename + '.csv', index=False) # Пишем результаты в файл
    end = time.time() - start ## собственно время работы программы
    print(end) ## вывод времени
    print('Done')
else:
    print('no host')




