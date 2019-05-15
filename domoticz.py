import c14_class, request

c14 = c14_class.C14_RS485('/dev/ttyUSB1')
arTemp = c14.ReadValues('T', 100, 1, [1, 2, 3, 4])

response = requests.get('http://localhost:8080/json.htm?type=command&param=udevice&nvalue=0&idx=idx&svalue='+arTemp[0])
response = requests.get('http://localhost:8080/json.htm?type=command&param=udevice&nvalue=0&idx=idx&svalue='+arTemp[1])
response = requests.get('http://localhost:8080/json.htm?type=command&param=udevice&nvalue=0&idx=idx&svalue='+arTemp[2])
response = requests.get('http://localhost:8080/json.htm?type=command&param=udevice&nvalue=0&idx=idx&svalue='+arTemp[3])
