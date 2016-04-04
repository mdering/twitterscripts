#!/usr/bin/env python
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cm as cm, matplotlib.font_manager as fm

pairs = [['longimages.csv','utf-8','Images'],['longdetections.csv','utf-8','Detections']]

pair = pairs[1]
infile = pair[0]
encoding = pair[1]
text = pair[2]

title_font = fm.FontProperties(family='Bitstream Vera Sans', style='normal', size=20, weight='normal', stretch='normal')
label_font = fm.FontProperties(family='Bitstream Vera Sans', style='normal', size=18, weight='normal', stretch='normal')
ticks_font = fm.FontProperties(family='Bitstream Vera Sans', style='normal', size=12, weight='normal', stretch='normal')
annotation_font = fm.FontProperties(family='Bitstream Vera Sans', style='normal', size=10, weight='normal', stretch='normal')
axis_bgcolor = '#f0f0f0'

years    = mdates.YearLocator()   # every year
months   = mdates.MonthLocator()  # every month
days  = mdates.DayLocator()
yearsFmt = mdates.DateFormatter('%b-%Y')


alltweets=[]

df = pd.read_csv(infile, encoding=encoding, index_col='time', parse_dates=True)
td = pd.Timedelta(8,unit='h')
print df.index[0]
df.index -= td
print df.index[0]
#exit()

classesdfs = []

colors = ['b','r','c','g','y','m']

highdf= None
if pair == pairs[1]:
	highdf = df[df.score>.8]
	
	classesdfs.append(df[df['class'] == "person"])
	classesdfs.append(df[df['class'] == "car"])
	classesdfs.append(df[df['class'] == "tv or monitor"])
	
	
	
	classesdfs.append(highdf[highdf['class'] == "person"])
	classesdfs.append(highdf[highdf['class'] == "car"])
	classesdfs.append(highdf[highdf['class'] == "tv or monitor"])
	
	
	
	#df = df[]

#general plot by hour
countdata = df.groupby(df.index.hour).size()

countdata.index = [s + ':00' for s in countdata.index.astype(str)]
ax0 = countdata.plot(kind='bar', figsize=[10,6], width=0.6, alpha=0.5, color='c', edgecolor='gray', grid=False, label=r" >.5")
if highdf is not None:
	highcountdata = highdf.groupby(highdf.index.hour).size()
	ax = highcountdata.plot(kind='bar', figsize=[10,6], width=0.6, alpha=0.8, color='b', edgecolor='gray', grid=False,ax = ax0, label=r" >.8")
else:
	ax = ax0
#fig, ax = plt.subplots()
#ax.add_line(ax0.get_lines()[0])
#ax.add_line(ax1.get_lines()[0])

ax.set_xticks(map(lambda x: x, range(0, len(countdata))))
ax.set_xticklabels(countdata.index, rotation=45, rotation_mode='anchor', ha='right', fontproperties=ticks_font)
ax.yaxis.grid(True)
for label in ax.get_yticklabels():
    label.set_fontproperties(ticks_font)
 
ax.set_axis_bgcolor(axis_bgcolor)
ax.set_title(text+' in the Data Set, by hour of the day', fontproperties=title_font)
ax.set_xlabel('Hour (24H)', fontproperties=label_font)
ax.set_ylabel('Number of '+text, fontproperties=label_font)
if highdf is not None:
	ax.legend(loc='best',fancybox=True, framealpha=0.5)
plt.show()

plt.cla()
plt.clf()
plt.close('all')

#plot by day

countdata = df.groupby(df.index.weekday).size()
if highdf is not None:
	highcountdata = highdf.groupby(highdf.index.weekday).size()
countdata.index = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
 
ax0 = countdata.plot(kind='bar',
	figsize=[10,6],
                       width=0.6,
                       alpha=0.5,
                       color='c',
                       edgecolor='gray',
                       grid=False,
                       label=u" >.5"
                       )
if highdf is not None:
	ax = highcountdata.plot(kind='bar', 
	figsize=[10,6], width=0.6, alpha=0.8, 
	color='b', edgecolor='gray', grid=False,ax = ax0, label=u" > .8")
	ax.legend(loc='best',fancybox=True, framealpha=0.5)
else:
	ax=ax0
	
 
ax.set_xticks(map(lambda x: x, range(0, len(countdata))))
ax.set_xticklabels(countdata.index, rotation=35, rotation_mode='anchor', ha='right', fontproperties=ticks_font)
ax.yaxis.grid(True)
for label in ax.get_yticklabels():
    label.set_fontproperties(ticks_font)
 
ax.set_axis_bgcolor(axis_bgcolor)
ax.set_title(text+' in the data set, by day of the week', fontproperties=title_font)
ax.set_xlabel('Day of Week', fontproperties=label_font)
ax.set_ylabel('Number of '+text, fontproperties=label_font)
 
plt.show()

plt.cla()
plt.clf()
plt.close('all')

#plot by class
ax = None
for idx,classdf in enumerate(classesdfs):
	countdata = classdf.groupby(classdf.index.weekday).size()
	#print classdf['class'][0]
	label = classdf['class'][0]
	if idx/3 > 0:
		label+=u" > .5"
	else:
		label+=u" > .8"
	ax = countdata.plot(kind='bar',
	figsize=[10,6],
                       width=0.4,
                       alpha=.2*(idx%3+2),
                       color=colors[idx%3],
                       edgecolor='gray',
                       grid=False,
                       label = label,
                       ax = ax,
                       position=idx/3)

ax.legend(loc='best',fancybox=True, framealpha=0.5)
ax.set_xlim(-.5,6.5)
countdata = classesdfs[0].groupby(classesdfs[0].index.weekday).size()
countdata.index = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
 
ax.set_xticks(map(lambda x: x, range(0, len(countdata))))
ax.set_xticklabels(countdata.index, rotation=35, rotation_mode='anchor', ha='right', fontproperties=ticks_font)
ax.yaxis.grid(True)
for label in ax.get_yticklabels():
    label.set_fontproperties(ticks_font)
 
ax.set_axis_bgcolor(axis_bgcolor)
ax.set_title(text+' in the data set, by day of the week', fontproperties=title_font)
ax.set_xlabel('Day of Week', fontproperties=label_font)
ax.set_ylabel('Number of '+text, fontproperties=label_font)
 
plt.show()

ax = None
for idx,classdf in enumerate(classesdfs):
	countdata = classdf.groupby(classdf.index.hour).size()
	#print classdf['class'][0]
	label = unicode(str(classdf['class'][0]), "utf-8")
	if idx/3 > 0:
		label+=r' > .5'
	else:
		label+=r' > .8'
	ax = countdata.plot(kind='bar',
	figsize=[10,6],
                       width=0.4,
                       alpha=.2*(idx%3+2),
                       color=colors[idx%3],
                       edgecolor='gray',
                       grid=False,
                       label = label,
                       ax = ax,
                       position=idx/3)

ax.legend(loc='best',fancybox=True, framealpha=0.5)
ax.set_xlim(-.5,23.5)
countdata = df.groupby(df.index.hour).size()
countdata.index = [s + ':00' for s in countdata.index.astype(str)]

 
ax.set_xticks(map(lambda x: x, range(0, len(countdata))))
ax.set_xticklabels(countdata.index, rotation=35, rotation_mode='anchor', ha='right', fontproperties=ticks_font)
ax.yaxis.grid(True)
for label in ax.get_yticklabels():
    label.set_fontproperties(ticks_font)
 
ax.set_axis_bgcolor(axis_bgcolor)
ax.set_title(text+' in the Data Set, by hour of the day', fontproperties=title_font)
ax.set_xlabel('Hour (24H)', fontproperties=label_font)
ax.set_ylabel('Number of '+text, fontproperties=label_font)
 
plt.show()

exit()

















f = open('images.csv')
for line in f:
	sline = line.replace('\0', '').strip()[1:-1]
	date = sline.split(" ")[0]
	time = sline.split(" ")[1]
	y,m,d = date.split("-")
	h, minute,second = time.split(":")
	d = int(d)
	m = int(m.strip('\0'))
	y = int(y.strip('\0'))
	h = int(h.strip('\0'))
	dt = datetime.datetime(y,m,d,h)
	alltweets.append(dt)

date1 = min(alltweets)
date2 = max(alltweets)



delta = datetime.timedelta(hours=1)
dates = mdates.drange(date1, date2, delta)
y = np.zeros( len(dates)*1.0)
weekdayy = np.zeros(7*24)
weekdayx = np.arange(7*24)
dates.groupby()
for dt in alltweets:
	diff = (dt - date1)
	b = diff.days*24+diff.seconds/3600
	weekdaybin = dt.weekday()*24 + dt.hour
	y[b-1]+=1
	weekdayy[weekdaybin]+=1


fig, ax = plt.subplots()
ax.set_xlim(date1, date2)
ax.plot(dates, y)
plt.legend()
ax.xaxis.set_major_locator(months)
ax.xaxis.set_major_formatter(yearsFmt)
ax.xaxis.set_minor_locator(months)
ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
fig.autofmt_xdate()

plt.show()
plt.cla()
plt.clf()
plt.close('all')
fig, ax = plt.subplots()
ax.plot(weekdayx, weekdayy)
plt.legend()
plt.show()

exit()


f = open("detections.txt",'r')
bettertimes=[]
betterclasses=[]
worsetimes=[]
worseclasses=[]
for line in f:
	#print line
	sline = line.replace('\0', '').strip().split(";")
	score = float(sline[1])
	cls = sline[2]
	date = sline[3].split(" ")[0]
	time = sline[3].split(" ")[1]
	#print date, time
	m,d,y = date.split("/")
	h, minute = time.split(":")
	m = int(m.strip('\0'))
	y = int(y.strip('\0'))
	h = int(h.strip('\0'))
	minute = int(minute)
	d = int(d)
	dt = datetime.datetime(y,m,d,h)
	#print cls, time
	if score > .8:
		bettertimes.append(dt)
		betterclasses.append(cls)
	if score > .5:
		worsetimes.append(dt)
		worseclasses.append(cls)

date1 = min(worsetimes)
date2 = max(worsetimes)

delta = datetime.timedelta(hours=1)
dates = mdates.drange(date1, date2, delta)
worsey = np.zeros( len(dates)*1.0)
bettery = np.zeros( len(dates)*1.0)

for dt in worsetimes:
	diff = (dt - date1)
	b = diff.days*24+diff.seconds/3600
	worsey[b-1]+=1
for dt in bettertimes:
	diff = (dt - date1)
	b = diff.days*24+diff.seconds/3600
	bettery[b-1]+=1
	#print diff.days*24+diff.seconds/3600
worsemask = bettermask = np.ones(len(dates), dtype=bool)
#worsemask[worsey==0]=False
#bettermask[bettery==0]=False
fig, ax = plt.subplots()
#ax.plot(dates, y)
ax.plot(dates[worsemask], worsey[worsemask],'b:',label=u"\u03B5 > .5")
ax.plot(dates[bettermask], bettery[bettermask],'r-',label=u"\u03B5 > .8")
plt.legend()
ax.xaxis.set_major_locator(months)
ax.xaxis.set_major_formatter(yearsFmt)
ax.xaxis.set_minor_locator(months)
ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
fig.autofmt_xdate()

plt.show()
exit()

#for time in times:
