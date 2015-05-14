#!/usr/bin/env python

from twython import Twython
import time
import os.path
from tokens import *




twitter = Twython(APP_KEY, APP_SECRET,
                  OAUTH_TOKEN, OAUTH_TOKEN_SECRET)


f = open('matt_links.csv','r')

lastid="1";
if os.path.exists("matt_images.csv"):
	g =open('matt_images.csv','r')

	for line in g:
		lastid=line.split(",")[0]

	g.close()
	cont = 1;
else:
	cont=0;

g=open('matt_images.csv','a')

count = 0
lineno = 0
for line in f:
	l = line.strip()
	lineno+=1
	if lastid in l:
		cont=0
	if cont==1:
		continue;
	tweets=twitter.lookup_status(id=l);
	for data in tweets:
		name=data['user']['screen_name']
		#print data['coordinates'], data['place']
		#if 'text' in data:
			#print name.encode('utf-8')+": "+data['text'].encode('utf-8')
		#for url in data['entities']['urls']:
		#	if url['expanded_url'].startswith("http://instagr.am") or url['expanded_url'].startswith("http://instagram.com"):
				
		if 'media' in data['entities']:
			#print len(data['entities']['media'])
			for i in range(0,len(data['entities']['media'])):
				pic = data['entities']['media'][i]
				image_url = pic['media_url']
				g.write(data['id_str'].encode('utf-8')+","+name.encode('utf-8')+","+data['text'].encode('utf-8')+","+image_url.encode('utf-8')+"\n")
				count+=1
	g.flush()
	print count, lineno*100
	print "sleeping for 5 seconds"
	time.sleep(5)






