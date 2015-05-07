import urllib2
import time
import json
import serial

ser = serial.Serial('/dev/tty.usbserial', 9600)

def disp (loc) :
    if   loc=="F1":
	   dispense(1);
    elif loc=="F2":
	   dispense(2);
    elif loc=="F3":
	   dispense(3);
    elif loc=="F4":
	   dispense(4);
    elif loc=="F5":
	   dispense(5);
    elif loc=="-":
	time.sleep(1) 

def dispense(port): #ge signal
    
    time.sleep(1) 


    #time.sleep(5)


#init music

pygame.mixer.init()


#Definera fackens pinnar
fack1 = 7
fack2 = 11
fack3 = 12
fack4 = 13
fack5 = 15

urltoload = "url"

while(True):
    try:
        response = "0"
        location = "0"
        url = urllib2.urlopen(urltoload)
        response = url.read()
        url.close()
        json_doc = json.loads(response)
        location = json_doc.get('location')
        print location
	disp(location)
    except ValueError, e: #Start over
        time.sleep(3)
        continue
    except urllib2.URLError,e:
        time.sleep(3)
        continue






