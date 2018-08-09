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
    # @param self, bytearray(30) bFrame
    # @return byte
    def CalcCSum(self, bFrame):
        i = 0
        cSum = 0
        for x in bFrame:
            if i != 2:
                cSum += x
            i += 1
        return cSum & 0x7f

    # Check control sum
    # @param self, bytearray(30) bFrame
    # @return int
    def CheckCSum(self, bFrame):
        cSum = self.CalcCSum(bFrame)
        if cSUM == bFrame[2]:
            return 1
        else:
            return 0

    # Read from serial Port
    # @param self, bytearray(30) bFrame
    # @return bytearray(30)
    def SerialRequest(self, byref(bFrame)):
        bFrame[2] = CalcCSum(bFrame)
        bFrame[29] = ord('#')
        try:
            ser = serial.Serial(self.SerialPort, self.BaudRate, timeout=1)
            ser.setRTS(0) # RTS=1,~RTS=0 so ~RE=0, Receive mode enabled for MAX485
            ser.setDTR(0)
            ser.open()
            ser.write(bFrame) # send request frame
            time.sleep(3) # set empirically
            bFrame = bytearray(ser.read(size=self.FrameSize)) # receive request frame
            ser.close()
        except serial.SerialException:
            continue

        if CheckCSum(bFrame):
            return 1
        else:
            return 0

    # Function ReadValues
    # Read frames
    # @param self, char ['T'=temperature/'R'=other parameters] ValueType, byte RecipientAddress, byte SenderAddress, array [max array(6)] ValueNumbers
    # @return array
    def ReadValues(self, ValueType, RecipientAddress, SenderAddress, ValueNumbers):
        bFrame = b'\0' * 30
        bFrame[0] = 128 + RecipientAddress
        bFrame[1] = ord(ValueType)
        bFrame[3] = SenderAddress
        i = 5
        for vnr in ValueNumbers:
            bFrame[i] = vnr / 128
            bFrame[i + 1] = vnr % 128
            i += 4
        ret = self.SerialRequest(bFrame)
        vnr = 7
        arVal = [0, 0, 0, 0, 0, 0] # ??
        for i in range(0, len(ValueNumbers)):
            arVal[i] = bFrame[tnr] << 8 | bFrame[tnr + 1]
            vnr += 4
        return arVal

