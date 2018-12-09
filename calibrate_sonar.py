''' Calibration and support functions to interact with via python
    Assumes arduino is coded to constantly spit out sonar readings'''

import serial
import pdb

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
        self.high = 300
        self.noHand = 1000
        self.calThresh = 10
        self.prevData = 220

        self.minPower = minPower
        self.maxPower = maxPower
        self.rangeRatio = (maxPower-minPower)/(self.high-self.low)

        self.port = "com22"
        self.arduinoConnect()

    def data(self):
        print('A', end="\n")
        if (self.arduinoSerialData.inWaiting()>0):
            raw = arduinoSerialData.readline()
        else:
            print('No Reading Flag---')
            return self.prevData
        # raw = self.arduinoSerialData.readline()

        print('B', end="\n")
        data = raw.decode().strip('\r\n')
        print('C', end="\n")
        if '-' in data or data is None:
            print('None', end="\n")
            return None
        data = int(data.split('.')[0])
        print('D', end="\n")
        if data > (self.high + self.calThresh) or data < (self.low - self.calThresh):
            print('NoneTwo', end="\n")
            return None
        scaleData = (data-self.low)*self.rangeRatio + self.minPower
        print('E', end="\n")
        print('Data', scaleData, end="\n")
        self.prevData = scaleData
        return scaleData

    def rawData(self):
        if (self.arduinoSerialData.inWaiting()>0):
            raw = arduinoSerialData.readline()
        else:
            return self.prevData
        # raw = self.arduinoSerialData.readline()

        data = raw.decode().strip('\r\n')
        if data is None:
            return None
        data = int(data.split('.')[0])
        self.prevData = data
        return data

    def arduinoConnect(self):
        try:
            self.arduinoSerialData = serial.Serial(self.port, 9600)   # Initialize arduino for sonar
        except:
            print("Arduino not found. Reset commencing.")
            self.reset()
            return

    def reset(self):
        if hasattr(self, 'arduinoSerialData'):
            print('yep')
            self.arduinoSerialData.close()
        self.port = str(input("Arduino Connection Port (i.e. com22 or /dev/ttyACM0):"))
        self.arduinoConnect()
        print("\nBegin calibration...")
        self.calibrate()

#--------------------------- Calibration Function -----------------------------
    def calibrate(self, calCount = 0):
        #resets low, high, noHand, rangeRatio
    #----------Min----------
        print("Please hold your hand at your comfortable lower limit")
        input("     ** Press Enter to take the reading.")
        self.low = self.rawData()
        print("Reading taken")

    #----------Max----------
        print("Please hold your hand at your comfortable upper limit")
        input("     ** Press Enter to take the reading.")
        self.high = self.rawData()
        print("Reading taken")

    #----------None----------
        print("Please remove both of your hands from near the sensor")
        input("     ** Press Enter to take the reading.")
        self.noHand = self.rawData()
        print("Reading taken")

    #----------Check and Re-Cal----------
        if self.low is None or self.high is None or self.noHand is None:
            print("\nSomething didn't read right. Please try again.")
            calCount = self.reCal(calCount)
            self.calibrate(calCount)
            return

        if (abs(self.noHand - self.high) < self.calThresh):
            print("\nWe couldn't tell the difference between no hand and your upper height.")
            calCount = self.reCal(calCount)
            self.calibrate(calCount)
            return

    #----------Print----------
        print("Lower, Upper, No Hand")
        print(self.low, self.high, self.noHand)
        self.rangeRatio = ((self.maxPower-self.minPower)/(self.high-self.low))
        print("Calibration complete.")
        return



    def reCal(self):
        calCount += 1
        #Variable instructions
        if calCount <= 2:
            print("Please ensure your hand is directly over the sensor so it still sees you.")
        if calCount >= 1 and calCount <= 4:
            print("Consider keeping your range smaller and lowering your upper limit.")
        if calCount >= 3:
            print("Calibration is struggling. Consider repositioning the sensors.")
            print("     Try to ensure straight lines of hand movement, and reduce\
                possible interferences within a wide code around the sensor.")

        print("Please retry calibration.\n")
        return calCount




# ------------------------------------------------------------------------------
#                          Testing: Random Output
# ------------------------------------------------------------------------------
import random

class randomController(SonarController):
    def __init__(self, minPower = 1, maxPower = 4):
        self.low = 200
        self.high = 300
        self.noHand = 1000
        self.minPower = minPower
        self.maxPower = maxPower
        self.rangeRatio = ((self.maxPower-self.minPower)/(self.high-self.low))

    def data(self):
        raw = random.randint(300,700)
        if raw > self.high:
            return None
        scaleData = (raw-self.low)*self.rangeRatio + self.minPower
        return scaleData
