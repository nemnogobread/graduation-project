import serial

fsp = [serial.Serial() for i in range(0,2)]
# 0 - host   id

# Инициализация COM-порта
def serial_port_init_config(dev_id, com_port_num, baudrate):
    fsp[dev_id].baudrate = baudrate
    fsp[dev_id].port = com_port_num
    fsp[dev_id].open()

# Отправка запроса приемнику
def send_request(req, dev_id):
    fsp[dev_id].write((str(req)+'\n').encode())
    
# Получение ответа от приемника
def get_answer(dev_id):
    line_in = fsp[dev_id].readline()
    return line_in

# Перезапуск порта
def reset_serial(dev_id):
    fsp[dev_id].reset_input_buffer()
    fsp[dev_id].reset_output_buffer()

# Проверка буфера
def check_buf(dev_id):
    return fsp[dev_id].in_waiting

# Считывание пакета
def read_packet(packet_size, dev_id):
    serialStream = []
    num_n = 0
    while num_n < packet_size: # Считывает данные, пока не получит полный ракет
        line_in = fsp[dev_id].readline()
        ls = len(str(line_in))
        if ls == 12 or ls == 13: # Это костыль. Отсекает битые данные
            serialStream.append(float(line_in)) # осторожно с readline!
                                                # Может блокировать порт если ничего нет на входе.
            num_n += 1
        else:
            print('not in range', line_in)
    return serialStream

# Закрываем COM-порт
def close_serial(dev_id):
    fsp[dev_id].close() #we don't need serial port anymore




# Хвосты от старой программы. Не используются    
def test_read():
    print(fsp[0])

def read_ln():
    print(fsp[0].readline())
    print(fsp[0].readline())
    print(fsp[0].readline())
    print(fsp[0].readline())

def write_to_dest(t_bytes, dev_id):
        fsp[dev_id].write(t_bytes)



    

    



