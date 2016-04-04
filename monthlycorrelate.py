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
p=np.array(power)

columns=['value']
chopoff=1
#readarray=readarray[:-chopoff,:]


#print "read in energy data"

table = {}

#to_datetimeindex=index[:-chopoff]
for idx,time in enumerate(dates):
	table[time]=[]
#detectionframe = pd.read_csv("detections.csv", encoding="utf-8", index_col='time', parse_dates=True)

#print "loaded dataframe"
filedets = {}
filedets= pickle.load(open("detections.pkl",'rb'))

td = pd.Timedelta('8 hours')
# f = open("longdetections.csv")
# f.readline()
# for line in f:
# 	sline = line.strip().split(",")
# 	fname = sline[0]
# 	tstring= sline[3][1:-7]
# 	#print tstring
# 	t = pd.to_datetime(datetime.datetime.strptime(tstring,'%Y-%m-%d %H'))-td
# 	year = t.year
# 	month = t.month
# 	ts = datetime.date(year,month,1)
# 	#t.minute = 0
# 	cls = sline[2]
# 	score = float(sline[1])
# 	if fname not in filedets:
# 		filedets[fname]=[]
# 	filedets[fname].append([ts,cls,score])

# f.close()

pickle.dump(filedets,open("detections.pkl",'wb'))
#print len(filedets)
#print "read in detections"
#exit()

#table = pickle.load(open("table.pkl",'rb'))

#print type(table.keys()[0])
for fname in filedets:
	v = sorted(vectorize(filedets[fname],.5))
	#print v
	t = filedets[fname][0][0]
	if t not in table:
		pass
	else:
		table[t].extend(v)

# pickle.dump(table,(open("table.pkl",'wb')))

#print "vectorized files"
counts = {}
counts=pickle.load(open("counts.pkl",'rb'))
# f = open("longimages.csv",'r')
# f.readline()
# for line in f:
# 	sline = line.strip()
# 	tstring= sline[1:-7]
# 	#print tstring
# 	t = pd.to_datetime(datetime.datetime.strptime(tstring,'%Y-%m-%d %H'))-td
# 	year = t.year
# 	month = t.month
# 	ts = datetime.date(year,month,1)
# 	if ts not in counts:
# 		counts[ts]=0
# 	counts[ts]+=1

pickle.dump(counts,(open("counts.pkl",'wb')))

#print "read in images"

for item in masterset:
	columnvec = []
	total = 0
	for idx,ts in enumerate(dates):
		cnt = table[ts].count(item)
		total+=cnt
		if cnt > 0:
			pass
			#print item, cnt
		if ts in counts:
			#print counts[ts]
			columnvec.append(float(cnt)/counts[ts])
		else:
			if cnt > 0: 
				print cnt
			columnvec.append(0)
	x = np.array(columnvec)
	if total < 10:
		continue
	#print x.shape, p.shape
	print item+","+str(pearsonr(x, p)[0])+","+str(total)

exit()