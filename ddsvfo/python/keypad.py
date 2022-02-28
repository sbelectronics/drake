from threading import Thread
import time
import RPi.GPIO as GPIO

PIN_BTN1 = 5
PIN_BTN2 = 6
PIN_BTN3 = 12
PIN_BTN4 = 13

class DDSKeypad(Thread):
    def __init__(self, control=None):
        Thread.__init__(self)
        self.daemon = True
        self.control = control
        self.btn1 = PIN_BTN1
        self.btn2 = PIN_BTN2
        self.btn3 = PIN_BTN3
        self.btn4 = PIN_BTN4

        GPIO.setup(self.btn1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.btn2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.btn3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.btn4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def run(self):
        lastKeyState = None
        lastKeyDown = None
        while True:
            keyState = self.readKeypad()
            if (keyState != lastKeyState):
                # for debounce, ensure we get the same thing twice in a row
                lastKeyState = keyState
                time.sleep(0.001)
                continue

            if (lastKeyDown == keyState):
                # the last key is still down
                time.sleep(0.001)
                continue

            if (lastKeyDown != None):
                self.onKeyUp(lastKeyDown)
                lastKeyDown = None

            if (keyState != None):
                self.onKeyDown(keyState)
                lastKeyDown = keyState

            time.sleep(0.001)

    def readKeypad(self):
        bits = 0
        if not GPIO.input(self.btn1):
            bits += 1
        if not GPIO.input(self.btn2):
            bits += 2
        if not GPIO.input(self.btn3):
            bits += 4
        if not GPIO.input(self.btn4):
            bits += 8
        if bits == 0:
            return None
        return bits

    def onKeyDown(self, key):
        if self.control is not None:
            self.control.onKeyDown(key)
        else:
            print("Keydown %d" % key)

    def onKeyUp(self, key):
        if self.control is not None:
            self.control.onKeyUp(key)
        else:
            print("Keyup %d" % key)


def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    DDSKeypad().start()

    while True:
        pass


if __name__ == "__main__":
    main()
