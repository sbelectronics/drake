import os
from smbpi.pigencoder import PigEncoder
from alnum.segments import Seg14x4
from threading import Thread, Timer, Lock
import time
import traceback

PIN_ENC_A = 20
PIN_ENC_B = 21

KEY_BAND_UP = 1
KEY_BAND_DOWN = 2
KEY_MEM = 4
KEY_STEP = 8

BANDS = [
    {"name": "80 M", "start": 3500000, "span": 500000},
    {"name": "40 M", "start": 7000000, "span": 300000, "mem": [7074000, 7240000, 7284000]},
    {"name": "20 M", "start": 14000000, "span": 350000, "mem": [14074000]},
    {"name": "15 M", "start": 21000000, "span": 450000},
    {"name": "10 M", "start": 28000000, "span": 1700000}
]

class DDSControl(Thread):
    def __init__(self, vfo, i2c, enableInterp=True, intfreq=0, step=10, pi=None):
        Thread.__init__(self)
        self.daemon = True
        self.lock = Lock()
        self.vfo = vfo
        self.i2c = i2c
        self.displayLeft = Seg14x4(i2c, 0x70)
        self.displayLeft.brightness = 0.25
        self.displayRight = Seg14x4(i2c, 0x71)
        self.displayRight.brightness = 0.25
        self.enableInterp = enableInterp
        self.intfreq = intfreq
        self.step = step
        self.frequency = 7074000
        self.interp = []
        self.pi = pi
        self.curBand = None
        self.localChange = 0
        self.informTimer = None
        self.memIndex = None
        self.selectBandByName("40 M")

        self.asyncFrequencyRequest = None

        if self.enableInterp:
            self.loadCorrections()

        self.inform("R.L. DRAKE")

    def start(self):
        self.encoder = PigEncoder(self.pi, PIN_ENC_A, PIN_ENC_B)
        Thread.start(self)

    def loadCorrections(self, fn="correct.txt"):
        if os.path.exists(fn):
            self.interp=[]
            for line in open(fn,"r").readlines():
                parts = line.split()
                if len(parts)!=2:
                    print("Ignoring correction line %s" % line)
                    continue
                v0 = int(parts[0])
                v1 = int(parts[1])
                self.interp.append((v1,v0))

    def interpolate(self, v):
        for i in range(0, len(self.interp)-1):
            row0 = self.interp[i]
            row1 = self.interp[i+1]

            if (row0[0] <=v) and (row1[1] >= v):
                iv = row0[1] + (v-row0[0]) * ((row1[1] - row0[1]) / (row1[0] - row0[0]))
                return iv
        return int(v)

    def setFrequency(self, freq):
        self.frequency = freq
        print("SF", freq)
        self.displayFrequency(freq)
        if self.vfo:
            self.vfo.setFrequency(self.interpolate(freq + self.intfreq))

    def displayFrequency(self, freq):
        freqStr = "%8d" % freq
        self.displayLeft.print(freqStr[:2] + "." + freqStr[2:4])
        self.displayRight.print(freqStr[4:5] + "." + freqStr[5:])

    def getBandList(self):
        return BANDS

    def selectBand(self, band):
        if band.get("mem"):
            self.setFrequency(band["mem"][0])
        else:
            self.setFrequency(band["start"])
        self.curBand = band
        self.memIndex = None

    def selectBandByName(self, name):
        for band in BANDS:
            if band["name"] == name:
                self.selectBand(band)

    def nextBand(self):
        prev = None
        for band in BANDS:
            if prev == self.curBand:
                self.selectBand(band)
                return
            prev = band

    def prevBand(self):
        prev = None
        for band in BANDS:
            if (band == self.curBand) and (prev is not None):
                self.selectBand(prev)
                return
            prev = band

    def onKeyDown(self, k):
        pass

    def onKeyUp(self, k):
        if k == KEY_BAND_UP:
            self.prevBand()
            self.localChange += 1
        elif k == KEY_BAND_DOWN:
            self.nextBand()
            self.localChange += 1
        elif k == KEY_MEM:
            mem = self.curBand.get("mem")
            if mem:
                if self.memIndex is None:
                    self.memIndex = 0
                else:
                    self.memIndex += 1
                    if self.memIndex >= len(mem):
                        self.memIndex = 0
                self.setFrequency(mem[self.memIndex])
                self.localChange += 1
        elif k == KEY_STEP:
            if self.step == 10:
                self.step = 100
            else:
                self.step = 10
            self.inform("Step %3d" % self.step)

    def setFrequencyAsync(self, freq):
        with self.lock:
            self.asyncFrequencyRequest = freq

    def inform(self, msg):
        llen = 0
        lstr = ""
        rstr = ""
        for c in msg:
            if (llen>=4):
                rstr = rstr + c
            else:
                lstr = lstr + c
                if c!=".":
                    llen += 1

        self.displayLeft.print(lstr)
        self.displayRight.print(rstr)

        if (self.informTimer is not None):
            self.informTimer.cancel()
        self.informTimer = Timer(5, self.informTimeout)
        self.informTimer.start()
    
    def informTimeout(self):
        if (self.informTimer is not None):
            self.informTimer.cancel()
            self.informTimer = None
        self.displayFrequency(self.frequency)

    def run(self):
        while True:
            newFreq = None
            with self.lock:
                if self.asyncFrequencyRequest is not None:
                   newFreq = self.asyncFrequencyRequest
                   self.asyncFrequencyRequest = None
            if newFreq:
                self.setFrequency(newFreq)

            encoderDelta = self.encoder.getAndResetDelta()
            if (encoderDelta != 0):
                self.setFrequency((self.frequency//self.step + (-encoderDelta)) * self.step)
                self.localChange += 1
            time.sleep(0.001)


def main():
    from smbus2 import SMBus
    daemon = DDSControl(None, SMBus(1))
    daemon.displayFrequency(12345678)


if __name__ == "__main__":
    main()
