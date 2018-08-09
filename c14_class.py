######################################################################################
# Descirption: C14_RS485 Protocol python class
# author: Gabriel Zima (z1mEk)
# e-mail: gabriel.zima@wp.pl
# github: https://github.com/z1mEk/c14_protocol.git
# create date: 2018-08-09
# update date: 2018-08-09
######################################################################################

import serial, time

class C14_RS485:

    def __init__(self):
        self.SerialPort = "/dev/ttyUSB0"           # Device name of the serial port (USB adapter > RS485). TODO: change to init parameter.
        self.BaudRate = 9600                       # Serial baud rate

    # Calculate control sum
    def CalcCSum(self, bFrame):
        i = 0
        cSum = 0
        for x in bFrame:
            if i != 2:
                cSum += x
            i += 1
        return cSum & 0x7f # ?? check

    # Check control sum
    def CheckCSum(self, bFrame):
        cSum = self.CalcCSum(bFrame)
        if cSUM == bFrame[2]:
            return 1
        else:
            return 0

    # Read from serial Port
    def SerialRequest(self, RequestFrame):
        RequestFrame[2] = CalcCSum(SendFrame)
	RequestFrame[29] = ord('#')
        try:
            ser = serial.Serial(self.SerialPort, self.BaudRate, timeout=1)
            ser.setRTS(0) # RTS=1,~RTS=0 so ~RE=0, Receive mode enabled for MAX485
            ser.setDTR(0)
            ser.open()
            ser.write(RequestFrame) # send request frame
            time.sleep(3) # set empirically
            ReceiveFrame = bytearray(ser.read(size=self.FrameSize)) # receive request frame
            ser.close()
        except serial.SerialException:
            continue

        if CheckCSum(ReceiveFrame):
            return ReceiveFrame
        else:
            return -1

    # Read Temperatures
    def ReadTemps(self):
        #TODO: Add read temps
        RequestFrame = b'\0' * 30
        RequestFrame[0] = 128 + 1 #????
        RequestFrame[1] = ord('T')
        RequestFrame[3] = 21
        nr_temp = 1
        RequestFrame[5] = nr_temp / 128
        RequestFrame[6] = nr_temp % 128
        RecFrame = self.SerialRequest(RequestFrame)
        return RecFrame

'''
    # Read other parameters
    def ReadParams(self):
        #TODO: Add read parametes
        RequestFrame = b'\0' * 30
        RequestFrame[1] = ord('R')
        RecFrame = self.SerialRequest(RequestFrame)
        return RecFrame

    # Write parameters
    def WriteParams(self):
        #TODO: Add write parameters
        RequestFrame = b'\0' * 30
        RequestFrame[1] = ord('W')
        RecFrame = self.SerialRequest(RequestFrame)
        return RecFrame
'''
