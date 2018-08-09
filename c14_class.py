######################################################################################
# Descirption: C14 Protocol python class
# author: Gabriel Zima (z1mEk)
# e-mail: gabriel.zima@wp.pl
# github: https://github.com/z1mEk/c14_protocol.git
# create date: 2018-08-09
# update date: 2018-08-09
######################################################################################

import serial, time

class C14:
    def __init__(self):
        SERIALPORT = "/dev/ttyUSB0" # device name of the serial port (USB adapter> RS485).
        BAUDRATE = 9600 # Baud rate

    def ReadFromSerial(self, byRef(SendFrame)):
        return 0

    def WriteToSerial(self, byRef(SendFrame)):
        return 0

    def CalcCSum(self, bFrame):
        cSum = 0
        return cSum

    def CheckCSum(self, bFrame, CompCSum):
        cSum = self.CalcCSum(bFrame)
        if cSUM == CompCSum:
            return 1
	else:
            return 0

    def ReadTemps(self, SendFrame):
        RecFrame = SendFrame
        return RecFrame

    def ReadParams(self, SendFrame):
        RecFrame = SendFrame
        return RecFrame

    def WriteParams(self, SendFrame):
        RecFrame = SendFrame
        return RecFrame
