#!/usr/bin/env python

import numpy as np

f = open("detections.csv",'r')

files = {}
betterfiles = {}

f.readline()
for line in f:
	line=line.replace('\0', '').replace("\"",'').strip()
	fname = line.split(",")[0]
	#print line
	score = float(line.split(",")[1])
	cls = line.split(",")[2]
	if fname not in files:
		files[fname]=[]
	files[fname].append(cls)
	if score > .8:
		if fname not in betterfiles:
			betterfiles[fname]=[]
		betterfiles[fname].append(cls)


for d in [files,betterfiles]:
	finalcounts={}
	for fname in d:
		classes={}
		for cls in d[fname]:
			if cls not in classes:
				classes[cls]=0
			classes[cls]+=1
		for cls in classes:
			if classes[cls]>1:
				if cls+"+" not in finalcounts:
					finalcounts[cls+"+"]=0
				finalcounts[cls+"+"]+=1
			if cls not in finalcounts:
				finalcounts[cls]=0
			finalcounts[cls]+=1

	for key in sorted(finalcounts, key=finalcounts.get)[-10:]:
		print key+"&"+str(finalcounts[key])+"\\\\"
	tot=0
	for key in finalcounts:
		tot+=finalcounts[key]
	print tot
	print
	print
	
