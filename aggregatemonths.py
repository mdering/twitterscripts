import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cm as cm, matplotlib.font_manager as fm
from pandas.stats.api import ols
import datetime

colors =['r','g','b','y']
title_font = fm.FontProperties(family='Bitstream Vera Sans', style='normal', size=20, weight='normal', stretch='normal')
label_font = fm.FontProperties(family='Bitstream Vera Sans', style='normal', size=18, weight='normal', stretch='normal')
ticks_font = fm.FontProperties(family='Bitstream Vera Sans', style='normal', size=12, weight='normal', stretch='normal')
annotation_font = fm.FontProperties(family='Bitstream Vera Sans', style='normal', size=10, weight='normal', stretch='normal')
axis_bgcolor = '#f0f0f0'
filedict = {
	'low':'USA_CA_San.Diego-Lindbergh.Field.722900_TMY3_LOW.csv',
	'high':'USA_CA_San.Diego-Lindbergh.Field.722900_TMY3_HIGH.csv',
	"base":'USA_CA_San.Diego-Lindbergh.Field.722900_TMY3_BASE.csv',
	"SDGE":'otheredata.csv'}




ax = None
mode = 'monthly'

bigdf = None



df = pd.read_csv("monthlyaggregates.csv", index_col='date', parse_dates=True)
countdata = df.groupby(pd.TimeGrouper(freq='M')).sum()
#print countdata.index
bigdf = countdata

ax = countdata.plot(figsize=[10,6],alpha=0.5, color='c',grid=False,ax=ax,linewidth=3)

start = min(bigdf.index)
end = max(bigdf.index)


order = ['high','base','low']
for idx, fname in enumerate(order):
	print fname
	df = pd.read_csv(filedict[fname], index_col='time', parse_dates=True)
	temp = df.copy(deep=True)
	for i in range(1,5):
		copy = temp.copy(deep = True)
		td = pd.Timedelta(i*365,unit='d')
		copy.index +=td
		#print copy.index[0].year, df.index[0].year, i 
		df = df.append(copy)
		
	df.columns=[fname]
	#df = df[df.index>=start]
	#df = df[df.index<=end]
	if fname != "SDGE":
		pass
		#df *= 1000
	# if bigdf is not None:
	# 	bigdf = bigdf.merge(df,left_index=True,right_index=True)
	# else:
	# 	bigdf = df
	if mode == 'hour':
		countdata = df.groupby(df.index.hour).mean()
		#countdata.index = [str(s).split(".")[0] + ':00' for s in countdata.index]
		ax = countdata.plot(figsize=[10,6],alpha=0.5, color=colors[idx],grid=False,ax=ax,linewidth=3)
	elif mode == 'monthly':

		countdata = df.groupby(pd.TimeGrouper(freq='M')).sum()
		countdata = countdata[countdata.index>=start]
		countdata = countdata[countdata.index<=end]
		#print countdata.index
		bigdf = bigdf.merge(countdata,left_index=True,right_index=True)
		#print countdata.index
		countdata.index = [str(s).split(" ")[0] for s in countdata.index]

		ax = countdata.plot(figsize=[10,6],alpha=0.5, color=colors[idx],grid=False,ax=ax,linewidth=3)
	else:
		countdata = df.groupby(df.index.weekday).mean()
		countdata.index = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
		ax = countdata.plot(kind='bar', figsize=[10,6], width=.2, alpha=0.5, color=colors[idx], edgecolor='gray', grid=False,ax=ax,position=idx-1)


#ax.set_xlim(-1, len(countdata.index))
#ax.set_xticks(map(lambda x: x, range(0, len(countdata))))
#ax.set_xticklabels(countdata.index, rotation=45, rotation_mode='anchor', ha='right', fontproperties=ticks_font)
ax.yaxis.grid(True)
for label in ax.get_yticklabels():
    label.set_fontproperties(ticks_font)
 
ax.set_axis_bgcolor(axis_bgcolor)
ax.set_title('Simulated Monthly TMY Data/SDGE Provided Monthly Data', fontproperties=title_font)
ax.set_xlabel('Month', fontproperties=label_font)
ax.set_ylabel('kWh', fontproperties=label_font)
ax.legend(loc='best',fancybox=True, framealpha=0.5)
#ax.legend_.remove()
plt.gcf().tight_layout()
plt.show()

plt.cla()
plt.clf()
plt.close('all')

print bigdf.columns
index = []
corrs=[]
rmss=[]

print ols(y=bigdf['SDGE'], x=bigdf['high']).rmse

#print bigdf.corr()['usage'][1:]

print ols(y=bigdf['SDGE'], x=bigdf['base']).rmse 
print ols(y=bigdf['SDGE'], x=bigdf['low']).rmse 
exit()

for y in [2012,2013,2014]:
	start = datetime.datetime(y,1,1)
	end = datetime.datetime(y,12,31)
	yeardf = bigdf[bigdf.index>=start]
	yeardf = yeardf[yeardf.index<=end]
	index.append(start)
	print y#, len(yeardf.index),yeardf['low']
	corrs.append(yeardf.corr()['SDGE'][1:])
	rms = []
	rms.append(ols(y=yeardf['SDGE'], x=yeardf['high']).rmse)

	

	rms.append(ols(y=yeardf['SDGE'], x=yeardf['base']).rmse)
	rms.append(ols(y=yeardf['SDGE'], x=yeardf['low']).rmse)
	rmss.append(rms)

corryears = pd.DataFrame(corrs,index = index)

rmsyears = pd.DataFrame(rmss,index = index,columns=['high','low','base'])

print corryears
print rmsyears

w=2

corryears.plot(linewidth=w)
ax = plt.gca()
linestyles = ['-','--',':']
for idx,l in enumerate(ax.get_lines()):
	l.set_linestyle(linestyles[idx])
ax.set_ylim(0,1)
ax.yaxis.grid(True)
ax.set_axis_bgcolor(axis_bgcolor)
ax.set_title('Correlation Coefficient of Simulated Monthly Models by Year', fontproperties=title_font)
ax.set_xlabel('Year', fontproperties=label_font)
ax.set_ylabel('Correlation Coeffecient', fontproperties=label_font)
ax.legend(loc='best',fancybox=True, framealpha=0.5)
plt.gcf().tight_layout()
plt.show()

rmsyears.plot(linewidth=w)
ax = plt.gca()
for idx,l in enumerate(ax.get_lines()):
	l.set_linestyle(linestyles[idx])
ax.set_ylim(bottom=0)
plt.gcf().tight_layout()
#ax.set_ylim(0,1)
ax.yaxis.grid(True)
ax.set_axis_bgcolor(axis_bgcolor)
ax.set_title('RMSE of Simulated Monthly Models by Year', fontproperties=title_font)
ax.set_xlabel('Year', fontproperties=label_font)
ax.set_ylabel('RMSE (KWH)', fontproperties=label_font)
ax.legend(loc='best',fancybox=True, framealpha=0.5)
plt.gcf().tight_layout()
plt.show()



