# Измерение уровня мошности сигнала.
# Осуществляет последовательный опрос нескольких приемников, подключенных к ПК.
# Результаты считываются короткими пакетами.


import COM
from   win_dev_list import get_com_dev_list
import pandas as pd
import numpy as np
import time

start_signal_for_COM5 = 120
start_signal_for_COM6 = 140
distance_COM3_COM5 = 0.3
distance_COM3_COM6 = 4.5
measure_number = 0

def make_measurements(receiver, transmitter, distance, start_signal):

    start = time.time() ## точка отсчета времени

    baudrate = 2000000  # 115200 #1200 #115200 #1000000 # Скорость COM - порта
    num_points_to_read = 4000  # Число измерений в серии
    req_len = 100  # Программа запрашивает у приемника измерения короткими сериями (пакетами). Это длина такого пакета
    HOST_DEV = 0

    PATH = 'C:/Users/infor/OneDrive/Рабочий стол/GlebMarat/Gleb/Lab7/baudrate-test-measurements/'  # Директория, в которой будет храниться файл с результатами измерений
    filename = str(measure_number) + '_measurements_' + transmitter + '_on_' + str(distance) + '_meters'   # Файл с результатами измерений
    num_cycles = int(num_points_to_read/req_len)  # Число считываний пакетов

    result = pd.DataFrame(columns = ['amp_steps_' + receiver])
    COM.serial_port_init_config(HOST_DEV, receiver, baudrate) # Задаем параметры COM-порта и открываем порт
    COM.send_request(start_signal, HOST_DEV)
    while COM.get_answer(HOST_DEV) != (str(req_len) + '\n').encode():  # Шлем запросы, пока не получим подтверждение
        COM.reset_serial(HOST_DEV)
        COM.send_request(req_len, HOST_DEV)
    COM.close_serial(HOST_DEV)

    for ii in range(num_cycles):
        res_list = []
        COM.serial_port_init_config(HOST_DEV, receiver, baudrate) # Задаем параметры COM-порта и открываем порт
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
        res_tmp.columns = ['amp_steps_' + receiver]
        result = (res_tmp.copy() if result.empty
                  else pd.concat([result, res_tmp], axis=0, ignore_index=True))

    result.to_csv(PATH + filename + '.csv', index=False) # Пишем результаты в файл
    print("\n", time.time() - start)

    print('Done')


if __name__ == "__main__":

    print('COM5: ', end='')
    make_measurements('COM3', 'COM5', distance_COM3_COM5, start_signal_for_COM5)
    # print('waiting 10 seconds', end='')
    # for i in range(10):
    #     time.sleep(1)
    #     print('.', end='')
    # print('\nCOM6: ', end='')
    # make_measurements('COM3', 'COM6', distance_COM3_COM6, start_signal_for_COM6)

