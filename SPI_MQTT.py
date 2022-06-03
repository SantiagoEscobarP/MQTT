import serial
import threading
import time
import collections
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from tkinter import Tk,Label,Button,Entry,Scale
import sys
import spidev
from time import sleep
import tkinter.font
import paho.mqtt.client as paho

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 976000
spi.bits_per_word = 8
spi.mode = 0b00

broker="192.168.0.14"
port=1883

client1= paho.Client("control1")
client1.connect(broker,port)


#serialPortbt = "/dev/rfcomm0"
#baudRatebt = 38400
#SerialConnection = Serial(serialPortbt , baudRatebt) #ensure non-blocking

gData = []
gData.append([0])
gData.append([0])

resp=range(0)
#Configuramos la gráfica
fig = plt.figure()
ax = fig.add_subplot(111)
hl, = plt.plot(gData[0], gData[1])
plt.ylim(0, 100)
plt.xlim(0,200)
# Función que se va a ejecutar en otro thread
# y que guardará los datos del serial en 'out_data'

   

def GetData(out_data):
        global resp
        while True:
            try:
                send = [0]
                print ("RPi SPI sending:", send)
                resp = spi.xfer2(send)  
                print ("RPi received:", resp[0])
                ret= client1.publish("casa/despacho/temperatura",resp[0])
                #SerialConnection.write((str(resp[0]).encode("ascii")))
                time.sleep(0.01)
                
            except KeyboardInterrupt:
                spi.close()
            line = resp[0]
            # Si la línea tiene 'Roll' la parseamos y extraemos el valor
            try:
                out_data[1].append(float(line))
                if len(out_data[1]) > 300:
                    out_data[1].pop(0)
            except:
                pass


    
def update_line(num, hl, data):
    hl.set_data(range(len(data[1])), data[1])
    return hl
# Configuramos la función que "animará" nuestra gráfica
line_ani = animation.FuncAnimation(fig, update_line, fargs=(hl, gData),
                                    interval=50, blit=False)
# Configuramos y lanzamos el hilo encargado de leer datos del serial

dataCollector = threading.Thread(target = GetData, args=(gData,))
dataCollector.start()
plt.show()
dataCollector.join()