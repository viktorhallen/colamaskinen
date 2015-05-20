import requests
import time
import json
import serial
import os

usbport = os.popen("ls /dev/ |grep ttyUSB").read().translate(None,'\n')
print usbport

ser = serial.Serial("/dev/" + usbport, 9600)

def disp (loc) :
    if   loc=="F1":
	   dispense('1')
    elif loc=="F2":
	   dispense('2')
    elif loc=="F3":
	   dispense('3')
    elif loc=="F4":
	   dispense('4')
    elif loc=="F5":
	   dispense('5')
    elif loc=="-":
	time.sleep(1) 

def dispense(port): #ge signal
    ser.write(port)
    time.sleep(1) 


    #time.sleep(5)


#init music



#Definera fackens pinnar


urltoload = ""

while(True):
    try:
        response = "0"
        location = "0"
        data = requests.get(urltoload)
        location = data.json()['location']
        print location
	disp(location)
    except ValueError, e: #Start over
        time.sleep(3)
        continue
    if(os.popen("ls /dev/ |grep ttyUSB").read().translate(None,'\n')!=usbport):
	time.sleep(1)
	usbport = os.popen("ls /dev/ |grep ttyUSB").read().translate(None,'\n')	 
	print usbport	
	ser = serial.Serial("/dev/" + usbport, 9600)
	






