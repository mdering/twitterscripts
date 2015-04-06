#!/usr/bin/env python

from twython import Twython

from tokens import *

sn="ghost_0836"

twitter = Twython(app_key=APP_KEY, app_secret=APP_SECRET, oauth_token=OAUTH_TOKEN, oauth_token_secret=OAUTH_TOKEN_SECRET)
followers = twitter.cursor(twitter.get_friends_ids,screen_name = sn)

f=open(sn+".txt",'w')

i=1
users=[]
for follower in followers:
	users.append(str(follower))
	if i==100:
		i=0
		userlist=",".join(users)
		#print len(users)
		users=[]
		results=twitter.lookup_user(user_id=userlist)
		for result in results:
			f.write(result['screen_name']+"\n")
	f.flush()
	i+=1