import c14_class

c14 = C14_RS485('/dev/ttyUSB3')
arTemp = ReadValues('T', 100, 21, [1, 2, 3])
if len(arTemp) == 30:
  print("Temp 1 = ".arTemp[0])
  print("Temp 2 = ".arTemp[1])
  print("Temp 3 = ".arTemp[2])
