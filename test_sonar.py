''' Calibration and support functions to interact with via python
    Assumes arduino is coded to constantly spit out sonar readings'''

import serial

# ------------------------------------------------------------------------------
#                                Main Class
# ------------------------------------------------------------------------------
class SonarController():
    '''Controller class for an Arduino supporting a Sonar sensor.
    Attributes: port, high, low, max
    Methods: data, calibrate, reCal
    '''
    def __init__(self, minPower = 1, maxPower = 4):
        self.low = 200
        self.high = 1000
        self.noHand = 11000
        self.calThresh = 10
        self.minPower = minPower
        self.maxPower = maxPower
        self.rangeRatio = (maxPower-minPower)/(self.high-self.low)

        self.port = "com22"
        self.arduinoConnect()

    def data(self):
        try:
            raw = self.arduinoSerialData.readline()
            data = raw.decode().strip('\r\n')
            print(data)
            if '-' in data or data is None:
                return None
            scaleData = data/100
            return scaleData

        except:
            pass

    def rawData(self):
        raw = self.arduinoSerialData.readline()
        data = raw.decode().strip('\r\n')
        print(data)
        if data is None:
            return None
        data = int(data.split('.')[0])
        return int(data)

    def arduinoConnect(self):
        try:
            self.arduinoSerialData = serial.Serial('com22', 9600)   # Initialize arduino for sonar
        except:
            print("Arduino not found. Reset commencing.")
            self.reset()
            return

    def reset(self):
        self.port = str(input("Arduino Connection Port (i.e. com22 or /dev/ttyACM0):"))
        self.arduinoConnect()
        self.data()
