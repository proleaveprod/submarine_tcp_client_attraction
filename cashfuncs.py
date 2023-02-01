import keyboard
from socket import *
tcp_socket = socket(AF_INET, SOCK_STREAM)

# print("\n\n\n ~~~~~~TCP-клиент Притяжение~~~~~~")
# connectToServer(host,port)
# test_send()

# #     data = str.encode(data)
# #     tcp_socket.send(data)




# print("        МЕНЮ        ")
# print("     1 - Получить данные с КТВ ГЗ")
# print("     2 - Получить данные с КТВ РТНПА")
# print("     3 - Управление ОП на КТВ ГЗ")
# print("     4 - Управление ОП на КТВ РТНПА")
# print("     5 - Управление ПУ на КТВ ГЗ")
# print("     6 - Управление НПУ на КТВ РТНПА")

# while 1:
#     keyboard_func()



def test_send():
    data = "DataTest12345678!@#$%^&*_-_-()}{"
    data = str.encode(data)
    tcp_socket.send(data)

def connectToServer(host,port):
    print("Connecting to server: ",host,":",port,"...")
    
    
    try:
        tcp_socket.connect((host,port))

    except Exception as err:
        print("Error:")
        print(err)
        quit()
    print("Connected!!!")

# def keyboard_func():
    
#     if keyboard.is_pressed('1'):
#         print("Запрос данных с КТВ ГЗ")
#         request_gz()

#     if keyboard.is_pressed('2'):
#         print("Запрос данных с КТВ РТНПА")

#     if keyboard.is_pressed('3'):
#         print("Управление лампами на КТВ ГЗ")

#     if keyboard.is_pressed('1'):
#         print("Управление лампами на КТВ РТНПА")

#     if keyboard.is_pressed('1'):
#         print("Управление двигателями на КТВ РТНПА")
    
#     if keyboard.is_pressed('1'):
#         print("Управление лампами на КТВ РТНПА")


def request_gz():
    print("Отправка запроса...")

    header = 0x55aa77cc
    lenght = 0x04
    id = 0x0001

    message = [header,0x00,lenght,id]


    
