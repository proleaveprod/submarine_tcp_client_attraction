from socket import *
import sys,os
import keyboard
import colorama
from colorama import Fore
import time
import struct

colorama.init()
os.system("CLS")

tcp_socket1 = socket(AF_INET, SOCK_STREAM)
tcp_socket2 = socket(AF_INET, SOCK_STREAM)


ID_GETSTATES        = 0x0001
ID_SETMOTORS        = 0x0002
ID_SETOFFMOTORS     = 0x0003
ID_SETLAMPS         = 0x0004
ID_SETLASER         = 0x0005
ID_CALIBRATION      = 0x0006


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Служебные функции ~~~~~~~~~~~~~~~~~~~~~~~~~~~
BYTEORDER = "little"
def createPocket(id=0,lenght=4,data=0):
    if data==0:
        data = b''
    message = []
    header = 0x55AA77CC
    reserve = 0
    dataLenght = lenght-4
    zeroDataLenght = 56 - dataLenght
    message.append((header).to_bytes(4,byteorder=BYTEORDER,signed=False))
    message.append((lenght).to_bytes(1,byteorder=BYTEORDER,signed=False))
    message.append((reserve).to_bytes(1,byteorder=BYTEORDER,signed=False))
    message.append((id).to_bytes(2,byteorder=BYTEORDER,signed=False))
    message.append(data)
    message.append((0).to_bytes(zeroDataLenght,byteorder=BYTEORDER,signed=False))
    message = bytes(b'').join(message)
    return message

def connectToServer(sock,host,port):
    print(f'Подключение к : {host}:{port}...',end='')

    try:
        sock.connect((host,port))
        print(Fore.GREEN + '   Подключен')
        #print("\033[32m{}".format("   Подключен"))
            
    except Exception as err:
        print(Fore.RED + "   Не удалось выполнить соединение")
        print(err)
        quit()

def sendNrecv(sock,dataToSend):
    #print(Fore.GREEN + "\n\nОтправка данных на устройство...")
    try:
        sock.send(dataToSend)
    except Exception as err:
        print(Fore.RED + "ОШИБКА ОТПРАВКИ\n")
        print(err)
        time.sleep(1)
        quit()

    try: 
        dataRx = sock.recv(1024)
    except Exception as err:
        print(Fore.RED + "ОШИБКА ПРИЕМА\n")
        print(err)
        time.sleep(1)
        quit()

    if(len(dataRx)==0):
            print(Fore.RED+ "ОШИБКА!!! Нет данных")
            quit()
    print(Fore.CYAN+ "Ответ от сервера:"+ Fore.WHITE)
    for i in range(0,len(dataRx)):
        print(hex(dataRx[i]),end=' ')
        if(i==7):
            print((Fore.CYAN),end='')
    print('\n')

    return dataRx

def mainMenuList():
    print(Fore.BLUE+ ("-------------МЕНЮ-------------"))
    print(" 1 - Получить данные с КТВ ГЗ")
    print(" 2 - Получить данные с КТВ РТНПА\n")

    print(" 3 - Управление ОП на КТВ ГЗ")
    print(" 4 - Управление ОП на КТВ РТНПА\n")

    print(" 5 - Управление ПУ на КТВ ГЗ")
    print(" 6 - Управление НПУ на КТВ РТНПА")
    print(" 7 - Смещение ПУ на КТВ ГЗ")
    print(" 8 - Смещение НПУ на КТВ РТНПА\n")

    print(" 9 - Управление лазером на КТВ РТНПА")
    print(" 0 - Калибровка двигателей\n")
    print(" c - Выход из приложения ")
    print("------------------------------")

#------------------------------------------------------------------------------------------

#Меню калибровки двигателей
def calibrationMenu():
    print(Fore.MAGENTA + ("\nКАЛИБРОВКА ДВИГАТЕЛЕЙ КТВ \n"))

    print(Fore.LIGHTYELLOW_EX + "Выберите КТВ (1 - КТВ ГЗ 2 - КТВ РТНПА) :",end=' ')

    #Выбор устройства
    while 1:
        curDevice = int(input(Fore.CYAN))
      
        if(curDevice==1):
            print(Fore.MAGENTA + "Калибровка двигателя КТВ ГЗ")
            cur_socket = tcp_socket1
            break
        elif(curDevice==2):
            print(Fore.MAGENTA + "Калибровка двигателей КТВ РТНПА")
            cur_socket = tcp_socket2
            break
                      

    
    #Выбор для РТНПА
    if curDevice==2:
        print(Fore.LIGHTYELLOW_EX + "\nВыберите что калибровать (1 - горизонтальная ось 2 - гертикальная ось 3 - все оси):",end=' ')
        while 1:
            
            curMotor = int(input(Fore.CYAN))
            if(curMotor==1):
                print(Fore.YELLOW + "Калибровка горизонтальной оси")
                break
            elif(curMotor==2):
                print(Fore.YELLOW + "Калибровка вертикальной оси")
                break
            elif(curMotor==3):
                print(Fore.YELLOW + "Калибровка всех осей")
                break
                                         
    elif curDevice==1:
        print(Fore.YELLOW + "Калибровка горизонтальной оси")
        curMotor=1
    
    #Формируем пакет данных
    calibrateData = []  
    calibrateData.append((curMotor).to_bytes(1,byteorder=BYTEORDER,signed=False))
    calibrateData.append((0).to_bytes(3,byteorder=BYTEORDER,signed=False))
    calibrateData = bytes(b'').join(calibrateData)                              
    
    #Формируем полный пакет
    dataTx = createPocket(id=ID_CALIBRATION,lenght=8,data = calibrateData)
    
    #Выводим его
    print((Fore.MAGENTA + "\nОтправка пакета "),len(dataTx),"Байт :" + Fore.WHITE)
    for i in range(0,8 + 4):
        if(i==8):
            print(Fore.YELLOW,end='')
        print((hex(dataTx[i])),end=' ')
    print()

    #Отправляем пакет и получаем ответ от сервера
    responce = sendNrecv(tcp_socket1,dataTx)
    print((Fore.LIGHTMAGENTA_EX+"RESPONCE:"),end='')
    if b'\xccw\xaaU\x00\x00\x06 ':
        print(Fore.LIGHTGREEN_EX+"CALIBRATE_OK")
    else:
        print(Fore.LIGHTRED_EX+"CALIBRATE_ERROR")

    input()

#Меню управления лазером  
def setLaserMenu():
    print(Fore.MAGENTA + ("\n  УПРАВЛЕНИЕ ЛАЗЕРНЫМ УКАЗАТЕЛЕМ КТВ РТНПА \n"))
    
    print(Fore.LIGHTYELLOW_EX + "Выберите состояние лазера (1 - вкл 0 - выкл)")
    while 1:
        key = keyboard.read_event()
        if   key.event_type=='down':
            if key.name == 'esc':
                mainMenuList()
                return 0
            
            try:
                laserState = int(key.name)
                if(laserState==1):
                    print(Fore.CYAN + "Включение лазера")
                    break
                elif(laserState==0):
                    print(Fore.CYAN + "Выключение лазера")
                    break
                else:
                    0                      
            except:
                0
    
    #Формируем пакет данных
    laserData = []  
    laserData.append((laserState).to_bytes(1,byteorder=BYTEORDER,signed=False))
    laserData.append((0).to_bytes(3,byteorder=BYTEORDER,signed=False))
    laserData = bytes(b'').join(laserData)                              
    
    #Формируем полный пакет
    dataTx = createPocket(id=ID_SETLASER,lenght=8,data = laserData)
    
    #Выводим его
    print((Fore.MAGENTA + "\nОтправка пакета "),len(dataTx),"Байт :" + Fore.WHITE)
    for i in range(0,8 + 4):
        if(i==8):
            print(Fore.YELLOW,end='')
        print((hex(dataTx[i])),end=' ')
    print()

    #Отправляем пакет и получаем ответ от сервера
    request = sendNrecv(tcp_socket1,dataTx)

    print((Fore.LIGHTMAGENTA_EX+"RESPONCE:"),end='')
    if b'\xccw\xaaU\x00\x00\x05 ':
        print(Fore.LIGHTGREEN_EX+"LASER_OK")
    else:
        print(Fore.LIGHTRED_EX+"LASER_ERROR")

    input()

#Меню смещения углов двигателей
def setOffsetMotorMenu(device_num):

    if device_num==1:
        cur_socket = tcp_socket1
        dataN = 4
        pitch=0
        print(Fore.MAGENTA + ("\n  СМЕЩЕНИЕ ПОВОРОТНог УСТРОЙСТВа КТВ ГЗ \n"))

    elif device_num==2:
        cur_socket = tcp_socket2
        dataN = 8
        print(Fore.MAGENTA + ("\n  СМЕЩЕНИЕ НАКЛОННО-ПОВОРОТНОГО УСТРОЙСТВА КТВ РТНПА \n"))

    while 1:
        try:
            yaw = float(input(Fore.LIGHTYELLOW_EX+"Введите горизонтальный угол (от -180.0 до 180.0): "+Fore.CYAN))
            if(yaw>=-180.0 and yaw<=180.0):
                break
            else:
                print(Fore.RED + "Неподходящее значение угла. Введите от -180.0 до 180.0  (float)")
        except:
            print(Fore.RED + "Неподходящее значение угла. Введите от -180.0 до 180.0  (float)")

    if device_num==2:
        while 1:
            try:
                pitch = float(input(Fore.LIGHTYELLOW_EX+"Введите вертикальный угол (от -180.0 до 180.0): "+Fore.CYAN))
                if(pitch>=-180.0 and pitch<=180.0):
                    break
                else:
                    print(Fore.RED + "Неподходящее значение угла. Введите от -180.0 до 180.0  (float)") 
            except:
                print(Fore.RED + "Неподходящее значение угла. Введите от -180.0 до 180.0  (float)") 

    
    print((Fore.MAGENTA + "Рысканье = "),end='')
    if yaw>0:
        print("+",yaw)
    else:
        print(yaw)
        
    
    if device_num==2:
        print((Fore.MAGENTA + "Тангаж = "),end='')
        if yaw>0:
            print("+",pitch)
        else:
            print(pitch)


    motorData = []
    yaw = struct.pack('f',yaw)
    pitch = struct.pack('f',pitch)

    motorData.append(yaw)
    motorData.append(pitch)
    
    motorData.append((0).to_bytes(4,byteorder=BYTEORDER,signed=False)) # Резерв 4 байта


    motorData = bytes(b'').join(motorData)


    dataTx = createPocket(id=ID_SETOFFMOTORS,lenght=16,data = motorData)

    try:
        cur_socket.send(dataTx)
    except Exception as err:
        print(Fore.RED + "ОШИБКА ОТПРАВКИ\n")
        print(err)
        time.sleep(1)
        quit()

    input()

#Меню установки углов двигателей



def setMotorMenu(device_num):

    if device_num==1:
        cur_socket = tcp_socket1
        dataN = 4
        pitch=0
        print(Fore.MAGENTA + ("\n  УПРАВЛЕНИЕ ПОВОРОТНЫМ УСТРОЙСТВОМ КТВ ГЗ \n"))

    elif device_num==2:
        cur_socket = tcp_socket2
        dataN = 8
        print(Fore.MAGENTA + ("\n  УПРАВЛЕНИЕ НАКЛОННО-ПОВОРОТНЫМ УСТРОЙСТВОМ КТВ РТНПА \n"))

    while 1:
        try:
            yaw = float(input(Fore.LIGHTYELLOW_EX+"Введите горизонтальный угол (от -180.0 до 180.0): "+Fore.CYAN))
            if(yaw>=-180.0 and yaw<=180.0):
                break
            else:
                print(Fore.RED + "Неподходящее значение угла. Введите от -180.0 до 180.0  (float)")
        except:
            print(Fore.RED + "Неподходящее значение угла. Введите от -180.0 до 180.0  (float)")

    if device_num==2:
        while 1:
            try:
                pitch = float(input(Fore.LIGHTYELLOW_EX+"Введите вертикальный угол (от -180.0 до 180.0): "+Fore.CYAN))
                if(pitch>=-180.0 and pitch<=180.0):
                    break
                else:
                    print(Fore.RED + "Неподходящее значение угла. Введите от -180.0 до 180.0  (float)") 
            except:
                print(Fore.RED + "Неподходящее значение угла. Введите от -180.0 до 180.0  (float)") 

    
    print((Fore.MAGENTA + "Рысканье = "),yaw)
    if device_num==2:
        print((Fore.MAGENTA + "Тангаж = "),pitch)

    motorData = []
    yaw = struct.pack('f',yaw)
    pitch = struct.pack('f',pitch)

    motorData.append(yaw)
    motorData.append(pitch)
    
    motorData.append((0).to_bytes(4,byteorder=BYTEORDER,signed=False)) # Резерв 4 байта


    motorData = bytes(b'').join(motorData)


    dataTx = createPocket(id=ID_SETMOTORS,lenght=16,data = motorData)

    responce = sendNrecv(tcp_socket1,dataTx)

    print((Fore.LIGHTMAGENTA_EX+"RESPONCE: "),end='')
    if b'\xccw\xaaU\x00\x00\x02 ':
        print(Fore.LIGHTGREEN_EX+"MOTOR_OK")
    else:
        print(Fore.LIGHTRED_EX+"MOTOR_ERROR")
        

    input()


#setMotorMenu(2)

#Меню управления светильниками
def setLampMenu(device_num):
    print(Fore.MAGENTA + ("\n  УПРАВЛЕНИЕ СВЕТИЛЬНИКОМ \n"))
    
    if device_num==1:
        print(Fore.LIGHTYELLOW_EX + "Выберите номер ОП для КТВ ГЗ(от 1 до 3) :",end=' ')
        cur_socket = tcp_socket1
        max_lamp = 3
    else:
        print(Fore.LIGHTYELLOW_EX + "Выберите номер ОП для КТВ РТНПА(от 1 до 9)   ",end=' ')
        cur_socket = tcp_socket2
        max_lamp = 9

    while 1:

        lamp_id = int(input(Fore.CYAN))
            
        if(lamp_id>0 and lamp_id<max_lamp+1):
            print(Fore.CYAN + "Выбран ОП №" + str(lamp_id))
            break
        else:
            print(Fore.RED + "Неподходящий номер ОП. Выберите от 1 до "+str(max_lamp)+ Fore.CYAN)
            time.sleep(0.2)            


    while 1:
        try:
            print(Fore.LIGHTYELLOW_EX)  

            bright = input("Введите яркость в процентах: "+Fore.CYAN)
            lamp_bright = int(bright)
            if lamp_bright>=0 and lamp_bright<=100:
                break
            else:
                print(Fore.RED + "Неподходящее значение яркости. Введите от 0 до 100%")
        except:
            print(Fore.RED + "Неподходящее значение яркости. Введите от 0 до 100%")

    print(Fore.CYAN + "Выбрана яркость " + str(lamp_bright) + '%\n')

    lampData = []
    lampData.append((lamp_id).to_bytes(1,byteorder=BYTEORDER,signed=False)) 
    lampData.append((lamp_bright).to_bytes(1,byteorder=BYTEORDER,signed=False))    
    lampData.append((0).to_bytes(2,byteorder=BYTEORDER,signed=False))
    lampData = bytes(b'').join(lampData)
    dataTx = createPocket(id=ID_SETLAMPS,lenght=8,data = lampData)

    print((Fore.MAGENTA + "Отправка пакета "),len(dataTx),"Байт :" + Fore.WHITE)
    for i in range(0,10):
        if(i==8):
            print(Fore.YELLOW,end='')
        print((hex(dataTx[i])),end=' ')
    print()

    responce = sendNrecv(cur_socket,dataTx)

    print((Fore.LIGHTMAGENTA_EX+"RESPONCE:"),end='')
    if b'\xccw\xaaU\x00\x00\x04 ':
        print(Fore.LIGHTGREEN_EX+"LAMP_OK")
    else:
        print(Fore.LIGHTRED_EX+"LAMP_ERROR")


    input()


def parseGZ(dataRx):
    header = bytes(dataRx[:4])
    lenght = bytes(dataRx[4:5])
    header = (struct.unpack('I', bytearray(dataRx[0:4]))[0])
    length = (struct.unpack('B', bytearray(dataRx[4:5]))[0])
    id = (struct.unpack('H', bytearray(dataRx[6:8]))[0])
    H_angle = (struct.unpack('f', bytearray(dataRx[8:12]))[0])
    OPstate = {}
    OPstate[0] = (struct.unpack('B', bytearray(dataRx[12:13]))[0])
    OPstate[1] = (struct.unpack('B', bytearray(dataRx[14:15]))[0])
    OPstate[2] = (struct.unpack('B', bytearray(dataRx[16:17]))[0])
    OPbright = {}
    OPbright[0] = (struct.unpack('B', bytearray(dataRx[13:14]))[0])
    OPbright[1] = (struct.unpack('B', bytearray(dataRx[15:16]))[0])
    OPbright[2] = (struct.unpack('B', bytearray(dataRx[17:18]))[0])
    SysTemp = (struct.unpack('b', bytearray(dataRx[18:19]))[0])
    PowerFlags = (struct.unpack('L', bytearray(dataRx[20:24]))[0])
    flowing = (struct.unpack('B', bytearray(dataRx[24:25]))[0])
    calibrating = (struct.unpack('B', bytearray(dataRx[25:26]))[0])

    print(Fore.LIGHTMAGENTA_EX +"Header"+Fore.WHITE+" ="+Fore.GREEN,hex(header),end='       ')
    print(Fore.LIGHTMAGENTA_EX +"Length"+Fore.WHITE+" ="+Fore.GREEN,length,end='       ' )
    print(Fore.LIGHTMAGENTA_EX +"ID"+Fore.WHITE+" ="+Fore.GREEN,hex(id))
    print(Fore.LIGHTRED_EX +"H_angle"+Fore.WHITE+" ="+Fore.YELLOW,H_angle)
    for i in range(0,3):
        print(Fore.LIGHTCYAN_EX +"LAMP"+str(i)+".state"+Fore.WHITE+" ="+Fore.YELLOW,bin(OPstate[i]),end='       ')
        print(Fore.LIGHTCYAN_EX +"LAMP"+str(i)+Fore.BLUE+".bright"+Fore.WHITE+" ="+Fore.YELLOW,OPbright[i],end='\n')
    print(Fore.LIGHTRED_EX +"System temperature"+Fore.WHITE+" ="+Fore.YELLOW,SysTemp)
    print(Fore.LIGHTBLUE_EX +"Power flags"+Fore.WHITE+" ="+Fore.YELLOW,end=' ')
    flags = str(bin(PowerFlags))[2:]
    for i in range(0,7):
        if flags[i]=='1':
            print(Fore.GREEN+flags[i],end =' ')
        else:
            print(Fore.RED+flags[i],end =' ')
    print(Fore.LIGHTRED_EX +"\nCalibrating"+Fore.WHITE+" ="+Fore.YELLOW,calibrating)

def parseRTNPA(dataRx):
    header = bytes(dataRx[:4])
    lenght = bytes(dataRx[4:5])
    header = (struct.unpack('I', bytearray(dataRx[0:4]))[0])
    length = (struct.unpack('B', bytearray(dataRx[4:5]))[0])
    id = (struct.unpack('H', bytearray(dataRx[6:8]))[0])
    H_angle = (struct.unpack('f', bytearray(dataRx[8:12]))[0])
    V_angle = (struct.unpack('f', bytearray(dataRx[12:16]))[0])

    OPstate = {}
    for i in range(0,9):
        OPstate[i] = (struct.unpack('B', bytearray(dataRx[16+2*i:17+2*i]))[0])

    OPbright = {}
    for i in range(0,9):
        OPbright[i] = (struct.unpack('B', bytearray(dataRx[17+2*i:18+2*i]))[0])

    SysTemp = (struct.unpack('b', bytearray(dataRx[34:35]))[0])
    PowerFlags = (struct.unpack('L', bytearray(dataRx[36:40]))[0])
    flowing = (struct.unpack('B', bytearray(dataRx[40:41]))[0])
    calibrating = (struct.unpack('B', bytearray(dataRx[41:42]))[0])

    print(Fore.LIGHTMAGENTA_EX +"Header"+Fore.WHITE+" ="+Fore.GREEN,hex(header),end='       ')
    print(Fore.LIGHTMAGENTA_EX +"Length"+Fore.WHITE+" ="+Fore.GREEN,length,end='       ' )
    print(Fore.LIGHTMAGENTA_EX +"ID"+Fore.WHITE+" ="+Fore.GREEN,hex(id))
    print(Fore.LIGHTRED_EX +"H_angle"+Fore.WHITE+" ="+Fore.YELLOW,H_angle)
    for i in range(0,3):
        print(Fore.LIGHTCYAN_EX +"LAMP"+str(i)+".state"+Fore.WHITE+" ="+Fore.YELLOW,bin(OPstate[i]),end='       ')
        print(Fore.LIGHTCYAN_EX +"LAMP"+str(i)+Fore.BLUE+".bright"+Fore.WHITE+" ="+Fore.YELLOW,OPbright[i],end='\n')
    print(Fore.LIGHTRED_EX +"System temperature"+Fore.WHITE+" ="+Fore.YELLOW,SysTemp)
    print(Fore.LIGHTBLUE_EX +"Power flags"+Fore.WHITE+" ="+Fore.YELLOW,end=' ')
    flags = str(bin(PowerFlags))[2:]
    for i in range(0,7):
        if flags[i]=='1':
            print(Fore.GREEN+flags[i],end =' ')
        else:
            print(Fore.RED+flags[i],end =' ')
    print(Fore.LIGHTRED_EX +"\nCalibrating"+Fore.WHITE+" ="+Fore.YELLOW,calibrating)


#Меню запроса данных с БУ
def getDataMenu(device_num):

    if device_num==1:
        cur_socket=tcp_socket1
    else:
        cur_socket=tcp_socket2

    dataTx = createPocket(id=ID_GETSTATES,lenght=4,data=0)
    print(Fore.MAGENTA + ("\n  ЗАПРОС НА ПОЛУЧЕНИЕ ДАННЫХ \n"))
    
    if(device_num==1):
        dataRx = sendNrecv(cur_socket,dataTx)

        parseGZ(dataRx)
        
    elif(device_num==2):
        #print("\033[35m{}".format("Отправка запроса на КТВ РТНПА...") )
        print("@@@@@Еще делаю")

    input()
#Главное меню
def mainMenu():

    

    while(1):
        
        mainMenuList()
        command = input(Fore.GREEN + "Выбранная команда:"+ Fore.CYAN)
        
        if   command=='1':
            getDataMenu(1)
        elif command=='2':
            getDataMenu(2)
        elif command=='3':
            setLampMenu(1)
        elif command=='4':
            setLampMenu(2)
        elif command=='5':
            setMotorMenu(1)
        elif command=='6':
            setMotorMenu(2)
        elif command=='7':
            setOffsetMotorMenu(1)
        elif command=='8':
            setOffsetMotorMenu(2)
        elif command=='9':
            setLaserMenu()
        elif command=='0':
            calibrationMenu()
        elif command=='c':
            tcp_socket1.close()
            tcp_socket2.close()
            quit()
        else:
            print("Ошибка")
    

