import urllib2
import RPi.GPIO as GPIO
import time
import json
import pygame



def disp (loc) :
    if loc=="F1":
	playCola()
        dispense(fack1)
    elif loc=="F2":
	playOther()
        dispense(fack2)
    elif loc=="F3":
	playOther()
        dispense(fack3)
    elif loc=="F4":
	playOther()
        dispense(fack4)
    elif loc=="F5":
	playOther()
        dispense(fack5)
    elif loc=="-":
	time.sleep(1)

def playCola():
    pygame.mixer.music.load("Cola.ogg")
    pygame.mixer.music.play()

def playOther():
    pygame.mixer.music.load("SweetHome.ogg")
    pygame.mixer.music.play()

def dispense(port): #ge signal
    GPIO.output(port,1)
    time.sleep(1)
    GPIO.output(port,0)
    while pygame.mixer.music.get_busy() == True:
        time.sleep(0.2)
	continue


    #time.sleep(5)


#init music

pygame.mixer.init()


#Definera fackens pinnar
fack1 = 7
fack2 = 11
fack3 = 12
fack4 = 13
fack5 = 15

#Setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(fack1,GPIO.OUT)
GPIO.setup(fack2,GPIO.OUT)
GPIO.setup(fack3,GPIO.OUT)
GPIO.setup(fack4,GPIO.OUT)
GPIO.setup(fack5,GPIO.OUT)
GPIO.output(fack1,0)
GPIO.output(fack2,0)
GPIO.output(fack3,0)
GPIO.output(fack4,0)
GPIO.output(fack5,0)

#Fixa detta
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








