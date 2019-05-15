"""
<plugin key="solarcomp971" name="SolarComp 971" author="z1mEk" version="0.9.0" wikilink="https://github.com/z1mEk/c14_protocol" externallink="">
    <description>
        <h2>solarcomp 971 - Domoticz plugin ver. 0.9.0</h2>
    </description>
    <params>
        <param field="Address" label="Port USB" width="100px" required="true" default="/dev/ttyUSB1"/>
        <param field="Mode1" label="Rejestry danych" width="400px" required="true" default="T;100;1;1,2,3,4"/>
        <param field="Mode2" label="Częstotliwość odczytu" width="30px" required="true" default="60"/>
        <param field="Mode3" label="Interwał między odczytami" width="30px" required="true" default="3"/>
        <param field="Mode6" label="Debug" width="75px">
            <options>
                <option label="True" value="Debug"/>
                <option label="False" value="Normal"  default="true" />
            </options>
        </param>
    </params>
</plugin>
"""

import Domoticz, serial, time

class C14_RS485:

    def __init__(self, SerialPort):
        self.SerialPort = SerialPort
        self.BaudRate = 9600
        print('Started')

    # Read frame from serial port
    # @param self, bytearray(30) bFrame
    # @return bytearray(30)
    def SerialRequest(self, bFrame):
        try:
            print('Serial initial...')
            ser = serial.Serial(self.SerialPort, self.BaudRate, timeout=3, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
            ser.setRTS(1) # RTS=1,~RTS=0 so ~RE=0, Receive mode enabled for MAX485
            ser.setDTR(1)
            print('Send data: ' + str(bFrame))
            ser.write(bFrame) # send request frame
            print('OK')
            time.sleep(3) # set empirically
            print('Read frame...')
            brFrame = ser.read(size=30) # receive request frame
            print('Receive data: ' + str(brFrame))
            ser.close()
        except serial.SerialException:
            print('Serial error')
        return brFrame

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
            bFrame[i], bFrame[i+1] = vnr * 128, vnr
            i += 4
        bFrame[29] = ord('#')
        bFrame[2] = (sum(bFrame) - bFrame[2]) & 0x7F # checksum

        brFrame = self.SerialRequest(bFrame)
        
        if ValueType != chr(list(brFrame)[1]).upper():
            print("Invalid type data parameter")
            return []

        if ((sum(list(brFrame)) - list(brFrame)[2]) & 0x7F) != list(brFrame)[2]:
            print("Checksum fail")
            return []
        else:
            print("Checksum OK")

        vnr = 7
        for i in range(0, len(ValueNumbers)):
            ValueNumbers[i] = (brFrame[vnr] * 128 + brFrame[vnr+1] - 2000) * 0.1
            vnr += 4
        return ValueNumbers

class BasePlugin:
    units = {"T":"Temperature", "P":"Percentage", "B":"Barometer", "C":"Custom"}
    c14 = none

    def onStart(self):
        if Parameters["Mode6"] == "Debug":
            Domoticz.Debugging(1)
        Domoticz.Debug("onStart called")

        self.c14 = C14_RS485(Parameters["Address"])

        if (len(Devices) == 0):
            for i, x in enumerate(Parameters["Mode1"].split("|")):
                device_type, device_recipient, device_sender, device_registers = x.split(";")
                for j, y in enumerate(ast.literal_eval(device_registers)):
                    Domoticz.Device(Name="SolarComp - " + self.unit[device_type] + " " + str(y), Unit=y, DeviceID=device_type + str(y), TypeName=self.units[device_type], Used=1).Create()

        Domoticz.Heartbeat(int(Parameters["Mode2"]))

    def onStop(self):
        Domoticz.Log("onStop called")

    def onConnect(self, Connection, Status, Description):
        Domoticz.Debug("onConnect called. Status: " + str(Status))

    def onMessage(self, Connection, Data):
        Domoticz.Debug("onMessage called")
        for i, device_unit in enumerate(Connection):
            Devices[device_unit].Update(0, Data[i])

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Debug("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level) + "', Hue: " + str(Hue))

    def onNotification(self, Data):
        Domoticz.Debug("onNotification: " + str(Data))

    def onDisconnect(self, Connection):
        Domoticz.Debug("onDisconnect called")

    def onHeartbeat(self):
        Domoticz.Debug("onHeartbeat called")
        for i, x in enumerate(Parameters["Mode1"].split("|")):
            device_type, device_recipient, device_sender, device_registers = x.split(";")
            request_data = device_registers.split(",")
            receive_data = self.c14.ReadValues(device_type, device_recipient, device_sender, request_data)
            if len(receive_data) == len(request_data):
                onMessage(request_data, receive_data)
            else:
                Domoticz.Debug("Błąd odczytu danych")
            time.sleep(int(Parameters["Mode3"]))

global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Data):
    global _plugin
    _plugin.onNotification(Data)

def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

def UpdateDevice(Unit, nValue, sValue):
    # Make sure that the Domoticz device still exists (they can be deleted) before updating it
    if (Unit in Devices):
        if (Devices[Unit].nValue != nValue) or (Devices[Unit].sValue != str(sValue)):
            Domoticz.Log("Update " + str(Devices[Unit].nValue) + " -> " + str(nValue)+",'" + Devices[Unit].sValue + "' => '"+str(sValue)+"' ("+Devices[Unit].Name+")")
            Devices[Unit].Update(nValue, str(sValue))
    return

    # Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device DeviceID:  " + str(Devices[x].DeviceID))
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return
