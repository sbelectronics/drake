import RPi.GPIO as GPIO
import time

PIN_CLK = 22
PIN_LOAD = 23
PIN_DATA = 24
PIN_RESET = 25


class DDSVFO:
    def __init__(self, 
                 pinClk=PIN_CLK,
                 pinLoad=PIN_LOAD,
                 pinData=PIN_DATA,
                 pinReset=PIN_RESET):
        self.pinClk = pinClk
        self.pinLoad = pinLoad
        self.pinData = pinData
        self.pinReset = pinReset

        GPIO.setup(self.pinClk, GPIO.OUT)
        GPIO.setup(self.pinLoad, GPIO.OUT)
        GPIO.setup(self.pinData, GPIO.OUT)
        GPIO.setup(self.pinReset, GPIO.OUT)

        GPIO.output(self.pinClk, False)
        GPIO.output(self.pinLoad, False)
        GPIO.output(self.pinData, False)
        GPIO.output(self.pinReset, False)

    def tick(self, pin):
        GPIO.output(pin, True)
        time.sleep(0.0001)
        GPIO.output(pin, False)
        time.sleep(0.0001)

    def sendByte(self, b):
        for i in range(0,8):
            GPIO.output(self.pinData, b & 0x01)
            b = b >> 1
            self.tick(self.pinClk)

    def setFrequency(self, freq):
        freq = int(freq*4294967296/125000000)
        for i in range(0, 4):
            self.sendByte(freq & 0xFF)
            freq = freq >> 8
        self.sendByte(0x00)
        self.tick(self.pinLoad)

def main():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    vfo = DDSVFO()
    vfo.setFrequency(2000000)

if __name__ == "__main__":
    main()
