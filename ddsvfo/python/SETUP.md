# smb-pi-lib
cd smb-pi-lib
sudo python3 ./setup.py install

# pigpiod
wget https://github.com/joan2937/pigpio/archive/master.zip -O pigpio.zip
unzip pigpio.zip
cd pigpio-master
make
sudo make install
sudo pigpiod

# python dependencies
sudo pip3 install adafruit-circuitpython-ht16k33 scipy bottle
