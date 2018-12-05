""" Calibration and support functions to interact with via python
    Assumes arduino is coded to constantly spit out sonar readings"""

import serial

class SonarController():
    """Controller class for an Arduino supporting a Sonar sensor.
    Attributes: port, high, low, max
    Methods: data, calibrate, reCal
    """
    def __init__(self):
        temp = str(input("Arduino Port Number:"))
        if temp == "testing":
            self.port = "com22"
            self.arduinoSerialData = serial.Serial(self.port, 9600)
            return
        self.port = "com"+temp
        self.arduinoSerialData = serial.Serial(self.port, 9600)   # Initialize arduino for sonar
        # self.calibrate()   #sets self.min and self.max
        for i in range(8):
            print(self.data())

    def data(self):
        raw = self.arduinoSerialData.readline()
        # b'0.00\r\n' b'6344.00\r\n' b'7928.00\r\n'
        data = raw.strip(b'\r')
        return raw

#--------------------------- Calibration Function -----------------------------

    def calibrate(self):
        calCount = 0
        calThresh = 1

    #----------Min----------
        print("Please hold your hand at your comfortable lower limit")
        input("     ** Enter any key to take the reading.")
        self.low = self.data()
        print("Reading taken")

    #----------Max----------
        print("Please hold your hand at your comfortable upper limit")
        input("     ** Enter any key to take the reading.")
        self.high = self.data()
        print("Reading taken")


    #----------BothNone----------
        print("Please remove both of your hands from the sensor")
        input("     ** Enter any key to take the reading.")
        self.max = self.data()
        print("Reading taken")


    #----------Check and Re-Cal----------
        if (abs(self.max - self.high) < calThresh):
            reCal()
            calibrate()
            return


    #----------Diff and Print----------
        self.calDiff = self.high-self.low
        print("Lower, Upper, Max, Diff")
        print(self.low, self.high, self.max)#, self.calDiff)


        print("Calibration complete.")
        input("     ** Enter any key to continue.")



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


        print("Please try calibrating again.\n")
