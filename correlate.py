#!/usr/bin/env python
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cm as cm, matplotlib.font_manager as fm
import xml.etree.ElementTree as ET
from sklearn.preprocessing import normalize
import xmltodict
import cPickle as pickle

from scipy.stats.stats import pearsonr

masterset = set()

def vectorize(l,tolerance):
	vector = set()
	for item in l:
		masterset.add(item[1])
		if item[2] < tolerance:
			continue
		if item[1] in vector:
			vector.add(item[1]+"+")
			masterset.add(item[1]+"+")
			vector.remove(item[1])
		if item[1]+"+" not in vector:
			vector.add(item[1])
	if "person" in vector and "person+" in vector:
		print "uh oh "
		exit()
	return list(vector)

title_font = fm.FontProperties(family='Bitstream Vera Sans', style='normal', size=15, weight='normal', stretch='normal')
label_font = fm.FontProperties(family='Bitstream Vera Sans', style='normal', size=12, weight='normal', stretch='normal')
ticks_font = fm.FontProperties(family='Bitstream Vera Sans', style='normal', size=10, weight='normal', stretch='normal')
annotation_font = fm.FontProperties(family='Bitstream Vera Sans', style='normal', size=10, weight='normal', stretch='normal')
axis_bgcolor = '#f0f0f0'

with open('edata.xml') as fd:
	obj = xmltodict.parse(fd.read())

feed = obj['feed']
entries = feed['entry']
readings = []
#print 
index = []
table = {}
#readarray = pickle.load(open("readings.pkl",'rb'))

#index = pickle.load(open("index.pkl",'rb'))
#print len(index), readarray.shape

end = pd.to_datetime(1399572000,unit='s')
start = pd.to_datetime(1306886400,unit='s')
print start
td = pd.Timedelta(8,unit='h')
for entry in entries:
	#print entry.keys()
	if 'title' in entry and (entry['title'] == 'Energy Usage' or entry['title'] == 'Usage Data'):
		blocks = entry['content']['IntervalBlock']
		#print len(blocks)
		for block in blocks:
			reads = block['IntervalReading']
			for reading in reads:
				#print reading
				ts = pd.to_datetime(int(reading['timePeriod']['start']),unit='s')-td
				#dt = datetime.date(ts.year,ts.month,1)
				if ts > start:
					index.append(ts)
					readings.append(int(reading['value']))
# for entry in entries:
# 	#print entry.keys()
# 	if 'title' in entry and entry['title'] == 'Energy Usage':
# 		blocks = entry['content']['IntervalBlock']
# 		#print blocks.keys()
# 		for reading in blocks['IntervalReading']:
# 			#print reading
# 			ts = pd.to_datetime(int(reading['timePeriod']['start']),unit='s')
# 			if ts < end:
# 				index.append(ts)
# 				readings.append(int(reading['value']))

readarray = np.array(readings,dtype=np.int32)
pickle.dump(readarray,(open("readings.pkl",'wb')))
pickle.dump(index,(open("index.pkl",'wb')))
columns=['value']
chopoff=1
#readarray=readarray[:-chopoff,:]


print "read in energy data"



#to_datetimeindex=index[:-chopoff]
for idx,time in enumerate(index):
	table[time]=[]
#detectionframe = pd.read_csv("detections.csv", encoding="utf-8", index_col='time', parse_dates=True)

#print "loaded dataframe"
#filedets= pickle.load(open("detections.pkl",'rb'))
filedets = {}

f = open("2011detections.csv")
f.readline()
for line in f:
	sline = line.strip().split(",")
	fname = sline[0]
	tstring= sline[3][1:-7]
	#print tstring
	#print tstring
	td = pd.Timedelta('8 hours')
	t = pd.to_datetime(datetime.datetime.strptime(tstring,'%Y-%m-%d %H'))-td
	#t.minute = 0
	cls = sline[2]
	score = float(sline[1])
	if fname not in filedets:
		filedets[fname]=[]
	filedets[fname].append([t,cls,score])

# f.close()

#pickle.dump(filedets,(open("detections.pkl",'wb')))
print "read in detections"
#exit()

#table = pickle.load(open("table.pkl",'rb'))

#print type(table.keys()[0])
for fname in filedets:
	v = sorted(vectorize(filedets[fname],.5))
	#print v
	t = filedets[fname][0][0]
	if t not in table:
		print t
	else:
		table[t].extend(v)

# pickle.dump(table,(open("table.pkl",'wb')))

#print "vectorized files"
counts = {}
#counts=pickle.load(open("counts.pkl",'rb'))
f = open("2011images.csv",'r')
f.readline()
for line in f:
	sline = line.strip()
	tstring= sline[1:-7]
	#print tstring
	td = pd.Timedelta('8 hours')
	t = pd.to_datetime(datetime.datetime.strptime(tstring,'%Y-%m-%d %H'))-td
	if t not in counts:
		counts[t]=0
	counts[t]+=1

# pickle.dump(counts,(open("counts.pkl",'wb')))

#print "read in images"
#readarray = (readarray-min(readarray))/(max(readarray)-min(readarray))

for item in masterset:
	columnvec = []
	total = 0
	for idx,ts in enumerate(index):
		cnt = table[ts].count(item)
		total+=cnt
		if cnt > 0:
			pass
			#print item, cnt
		if ts in counts:
			#print counts[ts]
			columnvec.append(float(cnt)/counts[ts])
		else:
			columnvec.append(0)
	x = np.array(columnvec)
	if total < 3:
		continue
	#print x.shape, readarray.shape
	print item+","+str(pearsonr(x, readarray)[0])

exit()