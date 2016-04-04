#!/usr/bin/env python

import glob
from matplotlib import pyplot as plt
import datetime
import xmltodict
import pandas as pd

dateset = set()
kwhs= {}
f = open("SDGE.csv",'r')
f.readline()
zips = {}
for line in f:
	sline = line.strip().split(",")
	zipcode = sline[0]
	month = int(sline[1])
	year = int(sline[2])
	cls = sline[3]
	combined = sline[4]
	customercount = sline[5]
	totalkwh = sline[6]
	avgkwh = sline[7]
	#if zipcode == "91978" and cls == 'R':
	if cls == 'R':
		d = datetime.date(year,month,1)
		dateset.add(d)
		if d not in kwhs:
			kwhs[d]=0
			zips[d]=0
		kwhs[d]+=int(avgkwh)
		zips[d]+=1
f.close()
dateset = list(dateset)
dates = []
power = []
for d in sorted(dateset):
	dates.append(d)
	power.append(kwhs[d]/zips[d])

readings = {}
index = []
for fname in ['rvg.xml','rvg1.xml']:
	with open(fname) as fd:
		obj = xmltodict.parse(fd.read())
	feed = obj['feed']
	entries = feed['entry']


	for entry in entries:
		#print entry.keys()
		if 'title' in entry and entry['title'] == 'Energy Usage':
			blocks = entry['content']['IntervalBlock']
			#print blocks.keys()
			for reading in blocks['IntervalReading']:
				#print reading
				ts = pd.to_datetime(int(reading['timePeriod']['start']),unit='s')

				dt = datetime.date(ts.year,ts.month,1)
				#print ts, dt
				if dt not in readings:
					readings[dt] = 0
				readings[dt]+=int(reading['value'])

rvg = []
rvgdates = []

for dt in dates:
	if dt in readings:
		rvgdates.append(dt)
		rvg.append(readings[dt]/1000)
plt.figure(figsize=(12,5))
plt.title('Individual Power Use vs Regional Average')

plt.plot(dates[18:],power[18:],'r', label = 'Regional Average')
plt.plot(rvgdates[1:],rvg[1:],'b', label='Individual')
plt.xlabel('Month')
plt.legend()
plt.ylabel('Power Use (Kilowatts)')
ax = plt.gca()
ax.set_axis_bgcolor('#f0f0f0')
plt.grid(True)
diff=0

for date in rvgdates[1:]:
	diff+=abs((readings[date]/1000)-kwhs[d]/zips[d])/float(kwhs[d]/zips[d])
print diff / (len(rvgdates)-1)

plt.draw()
plt.show()

