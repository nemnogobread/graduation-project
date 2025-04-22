import wmi

def get_com_dev_list():
        dev_list = wmi.WMI()
        COM_list = []
        for item in dev_list.query("Select * From Win32_SerialPort"):
                print(item.Caption)
                COM_list.append(item.Caption[-5:-1])
        return COM_list
