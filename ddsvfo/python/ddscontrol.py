import os
from alnum.segments import Seg14x4

class DDSControl:
    def __init__(self, vfo, i2c, enableInterp=True, intfreq=0):
        self.vfo = vfo
        self.i2c = i2c
        self.displayLeft = Seg14x4(i2c, 0x70)
        self.displayLeft.brightness = 0.25
        self.displayRight = Seg14x4(i2c, 0x71)
        self.displayRight.brightness = 0.25
        self.enableInterp = enableInterp
        self.intfreq = intfreq
        self.interp = []
        if self.enableInterp:
            self.loadCorrections()

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
                print("%0.8f" % (float(v0)/float(v1)))
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
        self.displayFrequency(freq)
        if self.vfo:
            self.vfo.setFrequency(self.interpolate(freq + self.intfreq))

    def displayFrequency(self, freq):
        freqStr = "%8d" % freq
        self.displayLeft.print(freqStr[:2] + "." + freqStr[2:4])
        self.displayRight.print(freqStr[4:5] + "." + freqStr[5:])


def main():
    from smbus2 import SMBus
    daemon = DDSControl(None, SMBus(1))
    daemon.displayFrequency(12345678)


if __name__ == "__main__":
    main()
