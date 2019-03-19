import pytuya
from time import sleep
import datetime

# SMART PLUG INFO
# Add to the list in the following format. Don't forget the commas.
'''
devices = [
	[<deviceID>,<deviceIP>,<deviceLocalKey>],
	[<deviceID>,<deviceIP>,<deviceLocalKey>],
	[<deviceID>,<deviceIP>,<deviceLocalKey>]
]
'''

devices = [
	["01200758dc4f22005c14","192.168.1.244","7bac3589afd382e2"]
]

def deviceInfo( deviceid, ip, localkey ):

	counter = 0
	retry = 5
	
	while True:
		try:
		
			d = pytuya.OutletDevice(deviceid, ip, localkey)
			data = d.status()
			
			if(d):
				# state = data['dps']['1']
				devId = data['devId']
				power = (float(data['dps']['5'])/10.0)
				current = float(data['dps']['4']*0.001)
				voltage = (float(data['dps']['6'])/10.0)
				resistance = float(voltage / current)
				
				# print state
				# print devId
				# print 'Power (W): %f' % (float(data['dps']['5'])/10.0)
				# print 'Current (mA): %f' % float(data['dps']['4'])
				# print 'Voltage (V): %f' % (float(data['dps']['6'])/10.0)
				# print 'Ohms (R): %f' % resistance
				
				return devId, power, current, voltage,resistance
				
		except:
			counter+=1
			if(counter>retry):
				print("ERROR: No response from plug %s [%s]." % (deviceid,ip))
				return(0.0)
			sleep(2)

def main():
	for device in devices:
	
		deviceID = device[0]
		deviceIP = device[1]
		deviceLocalKey = device[2]
		
		# DEBUG
		# print device[0]
		# print device[1]
		# print device[2]
		# print deviceID
		# print deviceIP
		# print deviceLocalKey
		
		devId, power, current, voltage, resistance = deviceInfo(deviceID,deviceIP,deviceLocalKey)

		print devId
		print power
		print current
		print voltage
		print resistance
		
if __name__ == "__main__":
	main()

