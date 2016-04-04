#!/usr/bin/env python
import datetime
import pandas as pd
from pandas.stats import var
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cm as cm, matplotlib.font_manager as fm
import xmltodict
from matplotlib import rcParams
from pandas.stats.api import ols
rcParams.update({'figure.autolayout': True})

pairs = [['USA_CA_San.Diego-Lindbergh.Field.722900_TMY3_LOW.csv','utf-8','Images'],['longdetections.csv','utf-8','Detections']]

pair = pairs[0]
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

#df.index -= td
#exit()

mode = 'hour'

filedict = {
	'low':'USA_CA_San.Diego-Lindbergh.Field.722900_TMY3_LOW.csv',
	'high':'USA_CA_San.Diego-Lindbergh.Field.722900_TMY3_HIGH.csv',
	"base":'USA_CA_San.Diego-Lindbergh.Field.722900_TMY3_BASE.csv',
	"SDGE":'otheredata.csv'}

colors =['r','g','b','y']
start = pd.to_datetime(1299110400,unit='s')
ax = None
bigdf = None
order = ['high','base','low','SDGE']
for idx, fname in enumerate(order):
	print fname
	df = pd.read_csv(filedict[fname], encoding=encoding, index_col='time', parse_dates=True)

	df.columns=[fname]
	df = df[df.index>start]
	if fname == "SDGE":
		df /= 1000
	if bigdf is not None:
		bigdf = bigdf.merge(df,left_index=True,right_index=True)
	else:
		bigdf = df
	if mode == 'hour':
		countdata = df.groupby(df.index.hour).mean()
		countdata.index = [str(s).split(".")[0] + ':00' for s in countdata.index]
		ax = countdata.plot(figsize=[10,6],alpha=0.5, color=colors[idx],grid=False,ax=ax,linewidth=3)
	else:
		countdata = df.groupby(df.index.weekday).mean()
		countdata.index = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
		ax = countdata.plot(kind='bar', figsize=[10,6], width=.2, alpha=0.5, color=colors[idx], edgecolor='gray', grid=False,ax=ax,position=idx-1)

#print edata
ax.set_xlim(-1, len(countdata.index))


# ax = lowcountdata.plot(kind='bar', figsize=[10,6], width=w, alpha=0.5, color='g', edgecolor='gray', grid=False,position=1,label='Low Load Profile')
# ax = edata.plot(kind='bar', figsize=[10,6], width=w, alpha=0.5, color='b', edgecolor='gray', grid=False,ax=ax,position=2,label="SDGE Provided")
# ax = basecountdata.plot(kind='bar', figsize=[10,6], width=w, alpha=0.5, color='y', edgecolor='gray', grid=False,ax=ax,position=3,label="Base Load Profile")
# ax = highcountdata.plot(kind='bar', figsize=[10,6], width=w, alpha=0.5, color='r', edgecolor='gray', grid=False,ax=ax,position=4,label="High Load Profile")

#ax = edata.plot(figsize=[10,6], alpha=0.5, color='b',grid=False,ax=ax,label="SDGE Provided")
#ax = basecountdata.plot(figsize=[10,6],alpha=0.5, color='y', grid=False,ax=ax,label="Base Load Profile")
#ax = highcountdata.plot(figsize=[10,6],alpha=0.5, color='r', grid=False,ax=ax,label="High Load Profile")

#fig, ax = plt.subplots()
#ax.add_line(ax0.get_lines()[0])
#ax.add_line(ax1.get_lines()[0])

ax.set_xticks(map(lambda x: x, range(0, len(countdata))))
ax.set_xticklabels(countdata.index, rotation=45, rotation_mode='anchor', ha='right', fontproperties=ticks_font)
ax.yaxis.grid(True)
for label in ax.get_yticklabels():
    label.set_fontproperties(ticks_font)
 
ax.set_axis_bgcolor(axis_bgcolor)
ax.set_title('Mean Usage in the Data Set, by hour of the day', fontproperties=title_font)
ax.set_xlabel('Day', fontproperties=label_font)
ax.set_ylabel('kW', fontproperties=label_font)
ax.legend(loc='best',fancybox=True, framealpha=0.5)
#ax.legend_.remove()
plt.gcf().tight_layout()
plt.show()

plt.cla()
plt.clf()
plt.close('all')

#bigdf = SDGEdf.merge(lowdf,left_index=True,right_index=True)
#result = var.VAR(bigdf)
# print result.granger_causality['p-value']
# print result.granger_causality['f-stat']
# bigdf = SDGEdf.merge(highdf,left_index=True,right_index=True)
# result = var.VAR(bigdf)
# print result.granger_causality['p-value']
# print result.granger_causality['f-stat']
# bigdf = SDGEdf.merge(basedf,left_index=True,right_index=True)
# result = var.VAR(bigdf)
# print result.granger_causality['p-value']
# print result.granger_causality['f-stat']

#print bigdf.columns

print bigdf.corr()['SDGE']

print ols(y=bigdf['SDGE'], x=bigdf['high'])

print ols(y=bigdf['SDGE'], x=bigdf['low'])

print ols(y=bigdf['SDGE'], x=bigdf['base'])

