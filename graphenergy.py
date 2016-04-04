#!/usr/bin/env python
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cm as cm, matplotlib.font_manager as fm
import xml.etree.ElementTree as ET

import xmltodict

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
print 
index = []
for entry in entries:
	#print entry.keys()
	if 'title' in entry and (entry['title'] == 'Energy Usage' or entry['title'] == 'Usage Data'):
		blocks = entry['content']['IntervalBlock']
		#print len(blocks)
		for block in blocks:
			reads = block['IntervalReading']
			for reading in reads:
				#print reading
				ts = pd.to_datetime(int(reading['timePeriod']['start']),unit='s')
				dt = datetime.date(ts.year,ts.month,1)
				index.append(ts)
				readings.append([int(reading['value'])])

print readings[0]
readarray = np.array(readings,dtype=np.int32)
columns=['value']
chopoff=1
readarray=readarray[:-chopoff,:]
index=index[:-chopoff]
df = pd.DataFrame.from_records(readarray,index=index)#, columns=columns)
td = pd.Timedelta(8,unit='h')
start = pd.to_datetime(1306886400,unit='s')
#print start
print df.index[0]
df.index -= td
print df.index[0]
end = pd.to_datetime(1399507200,unit='s')
df = df[df.index>start]
countdata = df.groupby(df.index.hour).mean()

countdata.index = [s + ':00' for s in countdata.index.astype(str)]
ax = countdata.plot(kind='bar', figsize=[19,7], width=0.6, alpha=0.5, color='c', edgecolor='gray', grid=False, label=r" >.5")

ax.set_xticks(map(lambda x: x, range(0, len(countdata))))
ax.set_xticklabels(countdata.index, rotation=45, rotation_mode='anchor', ha='right', fontproperties=ticks_font)
ax.yaxis.grid(True)

for label in ax.get_yticklabels():
    label.set_fontproperties(ticks_font)
 
ax.set_axis_bgcolor(axis_bgcolor)
ax.legend().set_visible(False)
ax.set_title('Power in the Data Set, by hour of the day', fontproperties=title_font)
ax.set_xlabel('Hour (24H)', fontproperties=label_font)
ax.set_ylabel('Mean Watts', fontproperties=label_font)

plt.show()




countdata = df.groupby(df.index.date).sum()[:-1]
countdata /=1000.0
#countdata.index = [s for s in countdata.index.astype(str)]
ax = countdata.plot(figsize=[19,7])
#idx = [s.to_pydatetime() for s in countdata.index]
ax.plot_date(countdata.index, countdata.values, fmt='b')
#ax.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=(1),
#                                                interval=1))
#ax.xaxis.set_minor_formatter(mdates.DateFormatter('%d\n%a'))
ax.xaxis.grid(True, which="minor")
ax.yaxis.grid()
#ax.xaxis.set_minor_locator(mdates.MonthLocator())
#ax.xaxis.set_minor_formatter(mdates.DateFormatter('\n\n\n%B\n'))



ax.yaxis.grid(True)
for label in ax.get_yticklabels():
    label.set_fontproperties(ticks_font)
 
ax.set_axis_bgcolor(axis_bgcolor)
ax.legend().set_visible(False)
ax.set_title('Power use in the dataset, by daily total', fontproperties=title_font)
ax.set_xlabel('Date', fontproperties=label_font)
ax.set_ylabel('Kilowatts', fontproperties=label_font)

plt.show()

exit()

