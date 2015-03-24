import urllib
import sys
import time
import webbrowser
from xml.etree.ElementTree import parse
from geopy.distance import vincenty
dave_lat = float('41.980262')
dave_lon = float('-87.668452')
dave_loc = (dave_lat,dave_lon)
bus_list = []



def get_bus(xml):
#	print 'in get_bus'
	u = urllib.urlopen('http://ctabustracker.com/bustime/map/getBusesForRoute.jsp?route=22')
	data = u.read()
	f = open(xml, 'wb')
	f.write(data)
	f.close()
	return xml

def find_bus(xml):
#	print 'in find_bus'
	doc = parse(xml)
	for bus in doc.findall('bus'):
		d = bus.findtext('d')
		lat = float(bus.findtext('lat'))
		if d == 'North Bound' and lat > dave_lat:
			print 'bus found'
			bus_list.append(bus)
	return bus_list

def track_bus(buses):
	get_bus('rt23.xml')
	doc = parse('rt23.xml')
	for bus in doc.findall('bus'):
		busid = bus.findtext('id')
		for trackedbus in buses:
			if busid == trackedbus.findtext('id'):
				bus_loc = (bus.findtext('lat'),bus.findtext('lon'))
				print 'bus: ' + busid + ' found at: lat - ' + bus.findtext('lat') + ' long - ' + bus.findtext('lon')
				if vincenty(bus_loc,dave_loc).miles < 0.5:
					print 'distance to bus' + bus.findtext('id') + ' is :' + str(vincenty(bus_loc,dave_loc).miles) +' miles.  Chase that mofo down'
					urlstring = 'https://maps.googleapis.com/maps/api/staticmap?center=41.980262,-87.668452'+'&zoom=12&size=400x400&markers=color:blue%7Clabel:S%7C'+bus.findtext('lat')+','+bus.findtext('lon')+'&markers=color:red%7Clabel:S%7C41.980262,-87.668452'
					webbrowser.open(urlstring)



def main(argv):
	bus_list = find_bus(get_bus('rt22.xml'))
	for bus in bus_list:
		print 'tracking bus : ' + bus.findtext('id')

	i = 0
	while True:
		track_bus(bus_list)
		time.sleep(60)




if __name__ == "__main__":
    main(sys.argv)


