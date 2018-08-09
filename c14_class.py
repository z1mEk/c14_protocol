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
        self.SerialPort = "/dev/ttyUSB0" # Device name of the serial port (USB adapter > RS485).
        self.BaudRate = 9600             # Serial baud rate
        self.FrameSize = 30              # Size of frame

    # Read from serial Port
    def SerialRequest(self, RequestFrame):
        try:
            ser = serial.Serial(self.SerialPort, self.BaudRate, timeout=1)
            ser.setRTS(0) # RTS=1,~RTS=0 so ~RE=0, Receive mode enabled for MAX485
            ser.setDTR(0)
            ser.open()
            ser.write(RequestFrame)
            time.sleep(3) # to test
            ReceiveFrame = ser.read(size=self.FrameSize)
            ser.close()
        except serial.SerialException:
            continue
        return ReceiveFrame

    # Calculate control sum
    def CalcCSum(self, bFrame):
        i = 0
        cSum = 0
        for x in bFrame:
            if i != 2:
                cSum += x
            i += 1
        return cSum & 0x7

    # Check control sum
    def CheckCSum(self, bFrame):
        cSum = self.CalcCSum(bFrame)
        if cSUM == bFrame[2]:
            return 1
	else:
            return 0

    def ReadSerial(self, SendFrame):
	SendFrame[2] = CalcCSum(SendFrame)
        ReceiveFrame = SerialRequest(SendFrame)
	if CheckCSum(ReceiveFrame):
            print("Checksum OK!")
            ret = ReceiveFrame
        else:
            print("Invalid checksum!")
            ret = -1
        return ret

    # Read Temperatures
    def ReadTemps(self):
        #TODO: Add read temps
        RecFrame = self.ReadSerial(SendFrame)
        return RecFrame

    # Read other parameters
    def ReadParams(self):
	#TODO: Add read parametes
        RecFrame = self.ReadSerial(SendFrame)
        return RecFrame

    # Write parameters
    def WriteParams(self):
        #TODO: Add write parameters
        RecFrame = self.ReadSerial(SendFrame)
        return RecFrame
