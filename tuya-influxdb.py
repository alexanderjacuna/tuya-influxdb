import pytuya
from time import sleep
import os
import datetime

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
			
		else:
			print "Unable to connect to device: " + deviceID + " @ " + deviceIP
		
if __name__ == "__main__":
	main()

