from tcp_funcs import *


# Данные для подключения к БУ ГЗ
hostGZ = '192.168.8.111'
portGZ = 16969

# Данные для подключения к БУ РТНПА
hostRTNPA = '192.168.8.112'
portRTNPA = 16969


print("\n\n\n ~~~~~~TCP-клиент Притяжение~~~~~~")


connectToServer(tcp_socket1,hostGZ,portGZ)

mainMenu()
