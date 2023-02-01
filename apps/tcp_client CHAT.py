# from tcp_funcs import *

import sys,os
os.system("CLS")
from socket import *
tcp_socket = socket(AF_INET, SOCK_STREAM)

host = '192.168.8.111'
port = 16969
BYTEORDER = "little"
addr = (host,port)

print("Connecting to server: ",host,":",port,"...")
tcp_socket = socket(AF_INET, SOCK_STREAM)
tcp_socket.connect(addr)
print("CONNECTED")

while 1:
    data = input("Отправить на сервер: ")
    if(data=='close'):
        print("STOP THE PROGRAM")
        tcp_socket.close()
        quit()
    data = str.encode(data)
    tcp_socket.send(data)

    data = tcp_socket.recv(1024)
    if(len(data)==0):
        print("ERROR! No data")
        tcp_socket.close()
        quit()

    data = bytes.decode(data)
    print("Server response: ",data,end='\n')


tcp_socket.close()








    