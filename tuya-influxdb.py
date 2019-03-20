import pytuya
from time import sleep
import os
import datetime
from influxdb import InfluxDBClient

# SMART PLUG INFO
'''
devices = [
	[<deviceID>,<deviceIP>,<deviceLocalKey>],
	[<deviceID>,<deviceIP>,<deviceLocalKey>],
	[<deviceID>,<deviceIP>,<deviceLocalKey>]
]
'''
devices = [
	["01200758dc4f22005c14","192.168.1.120","7bac3589afd382e2"]
]

# INFLUXDB CONNECTION INFO
host = "192.168.1.67"
port = 8086
user = "writer"
password = "supersecretpassword" 
dbname = "database"

# CREATE CLIENT OBJECT
client = InfluxDBClient(host, port, user, password, dbname)

def pingCheck(ip):

    ipAddress = ip
    response = os.system("ping -c 3 " + ipAddress + " >/dev/null 2>&1")

    if response == 0:
        status = True
    else:
        status = False

    return status

def deviceInfo( deviceid, ip, localkey ):

	counter = 0
	retryCount = 4

	while True:
		try:
			d = pytuya.OutletDevice(deviceid, ip, localkey)
			data = d.status()

			if(d):

				devId = data['devId']
				power = (float(data['dps']['5'])/10.0)
				current = float(data['dps']['4']*0.001)
				voltage = (float(data['dps']['6'])/10.0)
								
				return devId, power, current, voltage
				
		except:
			counter+=1
			if(counter>retryCount):
				print "ERROR: No response from plug %s [%s]." % (deviceid,ip)
				return(0.0)
			sleep(2)

def writeData(id,watts,amps,volts):
	
	measurement = id
	
	data1 = [
	{
	  "measurement": measurement + "-" + "watts",
		  "fields": {
			  "watts" : watts
		  }
	  } 
	]
	
	data2 = [
	{
	  "measurement": measurement + "-" + "amps",
		  "fields": {
			  "amps" : amps
		  }
	  } 
	]
	
	data3 = [
	{
	  "measurement": measurement + "-" + "volts",
		  "fields": {
			  "volts" : volts
		  }
	  } 
	]
	
	client.write_points(data1)
	client.write_points(data2)
	client.write_points(data3)

def main():

	for device in devices:
				
		deviceID = device[0]
		deviceIP = device[1]
		deviceLocalKey = device[2]
	
		if pingCheck(deviceIP) is True:
			
			devId, power, current, voltage = deviceInfo(deviceID,deviceIP,deviceLocalKey)

			print devId
			print 'Power (W): %f' % power
			print 'Current (mA): %f' % current
			print 'Voltage (V): %f' % voltage
			
			writeData(devId,power,current,voltage)
			
		else:
			print "Unable to connect to device: " + deviceID + " @ " + deviceIP
		
if __name__ == "__main__":
	main()

