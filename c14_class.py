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

    # Read frame from serial port
    # @param self, bytearray(30) bFrame
    # @return intgb = bytearray(30)
    def SerialRequest(self, bFrame):
        try:
            logging.debug('Serial initial...')
            ser = serial.Serial(self.SerialPort, self.BaudRate, timeout=30)
            ser.setRTS(1) # RTS=1,~RTS=0 so ~RE=0, Receive mode enabled for MAX485
            ser.setDTR(1)
            logging.debug('Write query...')
            logging.debug('Send data: ' + str(bFrame))
            ser.write(bFrame) # send request frame
            logging.debug('OK')
            print('OK')
            time.sleep(3) # set empirically
            logging.debug('Read frame...')
            print('Read frame...')
#            dd = ser.read_until(expected='#')
            bFrame = ser.read(size=len(bFrame)) # receive request frame
            logging.debug('Receive data: ' + str(bFrame))
            logging.debug('OK')
            print('OK')
            ser.close()
        except serial.SerialException:
            logging.debug('Serial error')
        return bFrame

    # Read values to array
    # @param self, char ['T'=temperature/'R'=other parameters] ValueType, byte RecipientAddress, byte SenderAddress, list [max list(6)] ValueNumbers
    # @return list
    def ReadValues(self, ValueType, RecipientAddress, SenderAddress, ValueNumbers):
        bFrame = bytearray(30)
        bFrame[0] = 128 + RecipientAddress
        bFrame[1] = ord(ValueType)
        bFrame[3] = SenderAddress
        i = 5
        for vnr in ValueNumbers:
            bFrame[i] = vnr / 128
            bFrame[i + 1] = vnr % 128
            i += 4
        bFrame[29] = ord('#')
        bFrame[2] = (sum(bFrame) - bFrame[2]) & 0x7f
        rbFrame = self.SerialRequest(bFrame)
        vnr = 7
        arVal = []
        for i in range(0, len(ValueNumbers)):
            arVal.append(rbFrame[vnr] << 7 | rbFrame[vnr + 1])
            vnr += 4
        return arVal

