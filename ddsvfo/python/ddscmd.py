from smbus2 import SMBus
import pigpio
import RPi.GPIO as GPIO
import argparse
import time
from ddsvfo import DDSVFO
from ddscontrol import DDSControl
from keypad import DDSKeypad


def parse_args():
    parser = argparse.ArgumentParser()

    defs = {
      "nointerp": False,
      "intfreq": 5645000,
      "freq": 7074000
    }

    _help = 'Disable interpolation (default: %s)' % defs['nointerp']
    parser.add_argument(
        '-n', '--nointerp', dest='nointerp', action='store_true',
        default=defs['nointerp'],
        help=_help)

    _help = "Intermediate frequency (default: %s)" % defs['intfreq']
    parser.add_argument("-i", "--int", dest='intfreq', type=int,
        default=defs["intfreq"],
        help=_help)

    _help = "Initial frequency (default: %s)" % defs['freq']
    parser.add_argument("-f", "--freq", dest='freq', type=int,
        default=defs["freq"],
        help=_help)        

    parser.add_argument('cmd', help='command')
    parser.add_argument('args', help='arguments', nargs='*')

    args = parser.parse_args()

    return args


def setFrequency(control, args):
    freq = int(args.args[0])
    control.setFrequency(freq)


def main():
    args = parse_args()

    pi = pigpio.pi()

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    bus = SMBus(1)
    vfo = DDSVFO()
    control = DDSControl(vfo, 
                         bus,
                         enableInterp=(not args.nointerp),
                         intfreq=args.intfreq,
                         pi=pi)

    keypad = DDSKeypad(control = control)

    if args.cmd == "setfreq":
        setFrequency(control, args)

    if args.cmd == "run":
        control.setFrequency(args.freq)
        control.start()
        keypad.start()
        print("started")
        while True:
            control.loop()
            time.sleep(0.0001)

if __name__ == "__main__":
    main()
