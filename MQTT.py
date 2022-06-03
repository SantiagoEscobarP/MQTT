import serial
import threading
import time
import sys
from time import sleep
import tkinter.font
import paho.mqtt.client as paho

broker="192.168.0.17"
port=1883

client1= paho.Client("control1")
client1.connect(broker,port)


while True:
    ret= client1.publish("casa/despacho/temperatura","hola")
    print("hola")
    time.sleep(1)         
    