from smbus2 import SMBus
import RPi.GPIO as GPIO
import argparse
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
        '-i', '--nointerp', dest='nointerp', action='store_true',
        default=defs['nointerp'],
        help=_help)

    _help = "Intermediate frequency (default: %s)" % defs['intfreq']
    parser.add_argument("-f", "--freq", dest='intfreq', type=int,
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

    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    bus = SMBus(1)
    vfo = DDSVFO()
    control = DDSControl(vfo, 
                         bus,
                         enableInterp=(not args.nointerp),
                         intfreq=args.intfreq)

    if args.cmd == "setfreq":
        setFrequency(control, args)


if __name__ == "__main__":
    main()
