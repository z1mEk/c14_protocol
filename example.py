import c14_class

c14 = c14_class.C14_RS485('/dev/ttyUSB0')
arValNum = [1, 2, 3]
arTemp = c14.ReadValues('T', 100, 21, arValNum)
print(arTemp)
if len(arTemp) == 30:
    for i in arValNum:
        print("Temperatura nr: " + str(arValNum[i]) + " = " + str(arTemp[i]) + "*C")

