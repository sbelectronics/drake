from smbus2 import SMBus
import pigpio
import RPi.GPIO as GPIO
import argparse
import time
from ddsvfo import DDSVFO
from ddscontrol import DDSControl


def parse_args():
    parser = argparse.ArgumentParser()

    defs = {
      "nointerp": False,
      "intfreq": 5645000
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

    if args.cmd == "setfreq":
        setFrequency(control, args)

    if args.cmd == "run":
        control.start()
        while True:
            control.loop()
            time.sleep(0.0001)



if __name__ == "__main__":
    main()
