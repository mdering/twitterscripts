#!/usr/bin/env python
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cm as cm, matplotlib.font_manager as fm
import xmltodict

f = open("rvg.csv",'w')

f.write("date,usage\n")


with open('rvg.xml') as fd:
	obj = xmltodict.parse(fd.read())

feed = obj['feed']
entries = feed['entry']
readings = []
index = []

for entry in entries:
	if 'IntervalBlock' in entry['content']:
		iblocks = entry['content']['IntervalBlock']['IntervalReading']
		for iblock in iblocks:
			usage = interval['value']
			starttime= interval['timePeriod']['start']
			ts = pd.to_datetime(int(starttime),unit='s')

for entry in entries:
	if 'IntervalBlock' in entry['content']:
		iblocks = entry['content']['IntervalBlock']
		for iblock in iblocks:
			intervals = iblock['IntervalReading']
			for interval in intervals:
				usage = interval['value']
				starttime= interval['timePeriod']['start']
				ts = pd.to_datetime(int(starttime),unit='s')
				f.write(str(ts)+","+usage+"\n")