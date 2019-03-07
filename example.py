import c14_class

c14 = c14_class.C14_RS485('/dev/ttyUSB1')
arTemp = c14.ReadValues('T',100, 1, [3])

