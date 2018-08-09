import c14_class

c14 = C14_RS485('/dev/ttyUSB3')
arTemp = c14.ReadValues('T', 100, 21, [1, 2, 3])
if len(arTemp) == 30:
  print("Temp 1 = " + str(arTemp[0]))
  print("Temp 2 = " + str(arTemp[1]))
  print("Temp 3 = " + str(arTemp[2]))
