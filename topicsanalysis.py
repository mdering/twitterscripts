import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cm as cm, matplotlib.font_manager as fm
from pandas.stats.api import ols
from scipy.stats import pearsonr
import datetime
import numpy as np
import matplotlib.ticker as plticker

colors =['r','g','b','y']
title_font = fm.FontProperties(family='Bitstream Vera Sans', style='normal', size=16, weight='normal', stretch='normal')
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
#print countdata
#print countdata.index
bigdf = countdata

df = pd.read_pickle("topicsdf.pkl")
#print df.sum()
#print df.columns
countdata = df.groupby(pd.TimeGrouper(freq='M')).sum()
#print countdata.index
bigdf = bigdf.merge(countdata,left_index=True,right_index=True)#.dropna()

#print bigdf.index
#print bigdf[bigdf.index=='2013-01-31']



goodcs = bigdf.columns[1:]
#print ols(y=bigdf['usage'], x=bigdf[goodcs])
goodcs = []
rhos=[]
for i in xrange(1,len(bigdf.columns)):
	c1 = bigdf.columns[0]
	c2 = bigdf.columns[i]
	#print c1,c2
	df_clean = bigdf[[c1,c2]].dropna()
	rho, p = pearsonr(df_clean[c1],df_clean[c2])
	if p < .05/(len(bigdf.columns)-1):
		print rho,p,c2
		goodcs.append(c2)
		rhos.append(rho)
#goodcs = bigdf.columns[1:]

f, axarr = plt.subplots(3, sharex=True)
plt.locator_params(nbins=4)
interesting=[2,4,8]
titles={
	2:"job",
	4:"wind",
	8:"day, good, morn"
}
print goodcs, rhos

for idx,ax in enumerate(axarr):
	lns1 = bigdf['SDGE'].plot(color='r',label="Power",ax=ax).get_lines()[0]
	topic = interesting[idx]
	c1 = goodcs[topic]
	print c1
	ax.set_axis_bgcolor(axis_bgcolor)
	loc = plticker.MultipleLocator(base=200.0)
	ax.yaxis.set_major_locator(loc)
	ax.set_title(titles[topic]+", r={0:.3f}".format(rhos[topic]), fontproperties=title_font)
	ax.get_xaxis().set_visible(False)
	#ax.set_xlabel('Month', fontproperties=label_font)
	ax2=ax.twinx()
	if idx ==1:
		ax.set_ylabel('KWH', fontproperties=label_font)
		ax2.set_ylabel('Cumulative Rate', fontproperties=label_font)
	lns2 = bigdf[c1].plot(color='b',ax=ax2,label="Topic Rate").get_lines()[0]
	
	lns = [lns1,lns2]
	labs = [l.get_label() for l in lns]
	#print labs
	
	
axarr[1].legend(lns, labs, loc='best',fancybox=True, framealpha=0.5)
axarr[2].get_xaxis().set_visible(True)

plt.show()
print len(goodcs)
for y in [2012,2013,2014]:
	start = datetime.datetime(y,1,1)
	end = datetime.datetime(y,12,31)
	yeardf = bigdf[bigdf.index>=start]
	yeardf = yeardf[yeardf.index<=end].dropna()
	#print y#, yeardf
#print ols(y=bigdf['SDGE'], x=bigdf[goodcs])





