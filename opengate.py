import RPi.GPIO as GPIO
from time import sleep

if __name__ == '__main__':
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)
    GPIO.output(17, False)
    print("Opening gate!")
    GPIO.output(17, True)
    sleep(2)
    GPIO.output(17, False)