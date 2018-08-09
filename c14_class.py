######################################################################################
# Descirption: C14_RS485 Protocol python class
# author: Gabriel Zima (z1mEk)
# e-mail: gabriel.zima@wp.pl
# github: https://github.com/z1mEk/c14_protocol.git
# create date: 2018-08-09
# update date: 2018-08-09
######################################################################################

import serial, time, logging

class C14_RS485:

    def __init__(self, SerialPort):
        self.SerialPort = SerialPort
        self.BaudRate = 9600

        logging.basicConfig(filename='/home/pi/C14_class.log', level=logging.DEBUG) # For silent set logging.CRTITICAL, please set path to log file.
        logging.debug('Started')

    # Calculate checksum
    # @param self, bytearray(30) bFrame
    # @return byte
    def CalcChecksum(self, bFrame):
        i = 0
        cSum = 0
        for x in bFrame:
            if i != 2:
                cSum += x
            i += 1
        return cSum & 0x7f

    # Validate checksum
    # @param self, bytearray(30) bFrame
    # @return int
    def ValidChecksum(self, bFrame):
        cSum = self.CalcChecksum(bFrame)
        if cSUM == bFrame[2]:
            return 1
        else:
            return 0

    # Read frame from serial port
    # @param self, bytearray(30) bFrame
    # @return int
    def SerialRequest(self, byref(bFrame)):
        bFrame[2] = CalcChecksum(bFrame)
        bFrame[29] = ord('#')
        try:
            logging.debug('Open serial...')
            ser = serial.Serial(self.SerialPort, self.BaudRate, timeout=1)
            ser.setRTS(0) # RTS=1,~RTS=0 so ~RE=0, Receive mode enabled for MAX485
            ser.setDTR(0)
            ser.open()
            logging.debug('OK')
            logging.debug('Write query...')
            logging.debug('Send data: '.join("{:02x}".format(x) for x in bFrame)
            ser.write(bFrame) # send request frame
            logging.debug('OK')
            time.sleep(3) # set empirically
            logging.debug('Read frame...')
            bFrame = bytearray(ser.read(size=len(bFrame))) # receive request frame
            logging.debug('Receive data: '.join("{:02x}".format(x) for x in bFrame)
            logging.debug('OK')
            ser.close()
        except serial.SerialException:
            logging.debug('Serial error!')
            continue

        if ValidChecksum(bFrame):
            logging.debug('Checksum OK')
            return 1
        else:
            logging.debug('Invalid Checksum')
            return 0

    # Read values to array
    # @param self, char ['T'=temperature/'R'=other parameters] ValueType, byte RecipientAddress, byte SenderAddress, list [max list(6)] ValueNumbers
    # @return list
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
        self.SerialRequest(bFrame)
        vnr = 7
        arVal = []
        for i in range(0, len(ValueNumbers)):
            arVal.append(bFrame[vnr] << 8 | bFrame[vnr + 1])
            vnr += 4
        return arVal

