#!/usr/bin/env python

from twython import Twython
import time

from tokens import *




twitter = Twython(APP_KEY, APP_SECRET,
                  OAUTH_TOKEN, OAUTH_TOKEN_SECRET)


f = open('fixed_sdlinks.csv','r')

lastid=0;
g =open('sd_images.csv','r')

for line in g:
	lastid=line.split(",")[0]

g.close()

g=open('sd_images.csv','a')

cont = 1;

count = 0
lineno = 0
for line in f:
	l = line.strip()
	lineno+=1
	if lastid in l:
		cont=0
	if cont==1:
		print "moving on"
		continue;
	tweets=twitter.lookup_status(id=l);
	for data in tweets:
		name=data['user']['screen_name']
		#print data['coordinates'], data['place']
		#if 'text' in data:
			#print name.encode('utf-8')+": "+data['text'].encode('utf-8')
		#for url in data['entities']['urls']:
		#	print url['expanded_url'];
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
	time.sleep(6)






