import RPi.GPIO as GPIO
import time

LED_RED = 17
LED_GREEN = 27
LED_BLUE = 22 

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(LED_RED, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(LED_GREEN, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(LED_BLUE, GPIO.OUT, initial=GPIO.HIGH)

def redON():
    GPIO.output(LED_RED, GPIO.LOW)

def redOFF():
    GPIO.output(LED_RED, GPIO.HIGH)

def greenON():
    GPIO.output(LED_GREEN, GPIO.LOW)
    
def greenOFF():
    GPIO.output(LED_GREEN, GPIO.HIGH)
    
def blueON():
    GPIO.output(LED_BLUE, GPIO.LOW)
    
def blueOFF():
    GPIO.output(LED_BLUE, GPIO.HIGH)

def red():
    redON()
    greenOFF()
    blueOFF()

def green():
    redOFF()
    greenON()
    blueOFF()
    
def blue():
    redOFF()
    greenOFF()
    blueON()

def white():
    redON()
    greenON()
    blueON()

def yellow():
    redON()
    greenON()
    blueOFF()

def cyan():
    redOFF()
    greenON()
    blueON()

def magenta():
    redON()
    greenOFF()
    blueON()

def off():
    redOFF()
    greenOFF()
    blueOFF()