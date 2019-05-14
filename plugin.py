"""
<plugin key="solarcomp971" name="SolarComp 971" author="z1mEk" version="0.9.0" wikilink="https://github.com/z1mEk/c14_protocol" externallink="">
    <description>
        <h2>solarcomp 971 - Domoticz plugin ver. 0.9.0</h2>
    </description>
    <params>
        <param field="Address" label="Port USB" width="100px" required="true" default="/dev/ttyUSB1"/>
        <param field="Mode1" label="Rejestry danych" width="400px" required="true" default="T;100;1;1,2,3,4"/>
        <param field="Mode2" label="Częstotliwość odczytu" width="30px" required="true" default="60"/>
        <param field="Mode6" label="Debug" width="75px">
            <options>
                <option label="True" value="Debug"/>
                <option label="False" value="Normal"  default="true" />
            </options>
        </param>
    </params>
</plugin>
"""

import Domoticz, time
from c14_class import C14_RS485

class BasePlugin:
    units = {"T":"Temperature", "P":"Percentage", "B":"Barometer", "C":"Custom"}
    c14 = none

    def onStart(self):
        if Parameters["Mode6"] == "Debug":
            Domoticz.Debugging(1)
        Domoticz.Debug("onStart called")

        self.c14 = c14_class.C14_RS485(Parameters["Address"])

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
            time.sleep(3)

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
