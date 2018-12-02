import c14_class

c14 = c14_class.C14_RS485('/dev/ttyUSB0')
arTemp = c14.ReadValues('T', 1, 21, [1, 2, 3])
print(arTemp)
