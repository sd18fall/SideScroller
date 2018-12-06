""" Calibration and support functions to interact with via python
    Assumes arduino is coded to constantly spit out sonar readings"""

import serial

# Multiplier given to player jump height and duration
minJumpPower = 1
maxJumpPower = 4

# ------------------------------------------------------------------------------
#                                Main Class
# ------------------------------------------------------------------------------
class SonarController():
    """Controller class for an Arduino supporting a Sonar sensor.
    Attributes: port, high, low, max
    Methods: data, calibrate, reCal
    """
    def __init__(self):
        self.port = "com22"
        self.arduinoSerialData = serial.Serial(self.port, 9600)   # Initialize arduino for sonar
        self.low = 0
        self.high = 100
        self.noHand = 200
        self.rangeRatio = ((maxJumpPower-minJumpPower)/(self.high-self.low))

    def data(self):
        raw = self.arduinoSerialData.readline()
        data = raw.decode().strip('\r\n')
        scaleData = (data-self.low)*self.rangeRatio + minJumpPower
        return scaleData

    def reset(self):
        self.port = "com" + str(input("Arduino Port (just the number):"))
        print("\nBegin calibration...")
        self.calibrate()   #resets low, high, noHand, rangeRatio

#--------------------------- Calibration Function -----------------------------
    def calibrate(self):
        calCount = 0
        calThresh = 1

    #----------Min----------
        print("Please hold your hand at your comfortable lower limit")
        input("     ** Press Enter to take the reading.")
        self.low = int(self.data())
        print("Reading taken")

    #----------Max----------
        print("Please hold your hand at your comfortable upper limit")
        input("     ** Press Enter to take the reading.")
        self.high = int(self.data())
        print("Reading taken")

    #----------None----------
        print("Please remove both of your hands from near the sensor")
        input("     ** Press Enter to take the reading.")
        self.noHand = int(self.data())
        print("Reading taken")

    #----------Check and Re-Cal----------
        if (abs(self.noHand - self.high) < calThresh):
            self.reCal()
            self.calibrate()
            return

    #----------Print----------
        print("Lower, Upper, Max")
        print(self.low, self.high, self.noHand)
        self.rangeRatio = ((maxJumpPower-minJumpPower)/(self.high-self.low))

        print("Calibration complete.")
        input("     ** Press Enter to continue.")



    def reCal(self):
        calCount += 1
        print("\nWe couldn't tell the difference between no hand and your upper height.")

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




# ------------------------------------------------------------------------------
#                          Testing: Random Output
# ------------------------------------------------------------------------------
import random

class randomController(SonarController):
    def __init__(self):
        self.low = 300
        self.high = 1600
        self.noHand = 200
        self.rangeRatio = ((maxJumpPower-minJumpPower)/(self.high-self.low))

    def data(self):
        if random.randint(0,5) == 5:
            raw = random.randint(300,1600)
            scaleData = (raw-self.low)*self.rangeRatio + minJumpPower
        else:
            scaleData = None
        return scaleData
