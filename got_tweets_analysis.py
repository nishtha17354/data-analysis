#!/usr/bin/env python
# coding: utf-8

from pymongo import MongoClient 
import tweepy
from datetime import datetime
import pandas as pd
from tqdm import tqdm
import os


# YOUR TWITTER ACCESS KEYS
CONSUMER_KEY=''
CONSUMER_SECRET=''
ACCESS_TOKEN=''
ACCESS_TOKEN_SECRET=''
MONGODB_CONNECTIONSTRING='mongodb://<username>:<password>@<hostname>:<port>'
PLOTLY_USERNAME=''
PLOTLY_API_KEY=''


#access keys
consumer_key = CONSUMER_KEY
consumer_secret = CONSUMER_SECRET

access_token = ACCESS_TOKEN
access_token_secret = ACCESS_TOKEN_SECRET

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


#code to connect the database
client = MongoClient(MONGODB_CONNECTIONSTRING)
twitter_db = client['admin'] 
tweets_collection = twitter_db['tweets']

api.search('GameOfThrones')


#part (a): the sample tweets
# to insert data
for tweet in tweepy.Cursor(api.user_timeline, screen_name = 'GameOfThrones', rpp=3200, count=20, result_type="recent", include_entities=True, lang="en").items(3200):
    d = tweet._json
    d['_id'] = d['id_str']
    print(d)
#     tweets_collection.insert_one(d)

tweets_collection.count()

#tweets is dictionary of dictionary
#i is dictionary
#print(i['created_at']): dates of every tweet
tweets = tweets_collection.find({})
date_List = list()
for i in tqdm(tweets):
    format= '%a %b %d %X %z %Y'
    #i['created_at']=datetime.datetime.strptime(i['created_at'], format)
    date=datetime.strptime(i['created_at'], format)
    
    date_List.append(date)
    
date_List.sort()   
# print(date_List)
#     print(i['created_at'])

# print(date_List[0])
count_dates={}
for i in date_List:
    s=str(i.day)+ "-"+ str(i.month)+ "-"+ str(i.year)
    if s in count_dates:
        count_dates[s]+=1
    else:
         count_dates[s]=1
# print(count_dates)
        
        
# !pip install -U pandas
df = pd.DataFrame(count_dates.items(), columns=['date', 'frequency'])
# !pip install plotly==3.7.1
# !pip uninstall plotly
get_ipython().system('pip install chart-studio')





#part(d)
import chart_studio.plotly as py 
import plotly.graph_objs as go
import chart_studio
chart_studio.tools.set_credentials_file(username=PLOTLY_USERNAME, api_key=PLOTLY_API_KEY)

l1 = list(count_dates.keys())
l2 = list(count_dates.values())
trace1 = go.Bar(
    x=l1,
    y=l2,
    marker=dict(
        color='rgb(225,0,0)',
        line=dict(
            color='rgb(8,48,107)',
            width=1.5),
        ),
    opacity=0.55
)
data = [trace1]
py.iplot(data, filename='fil')
# ("plot for No. of tweets vs days")





count_months={}
num2month = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}
for i in date_List:
    s = num2month[i.month]
    if s in count_months:
        count_months[s]+=1
    else:
        count_months[s]=1
# print(count_months)
    
    

#plot for No. of tweets vs months
l1 = list(count_months.keys())
l2 = list(count_months.values())
trace1 = go.Bar(
    x=l1,
    y=l2,
    marker=dict(
        color='rgb(225,0,0)',
        line=dict(
            color='rgb(8,48,107)',
            width=1.5),
        ),
    opacity=0.55
)
data = [trace1]
py.iplot(data, filename='fil')


# print(date_List[0])
count_time={}
for i in date_List:
    s=str(i.hour) + ":00:00"
    if s in count_time:
        count_time[s]+=1
    else:
         count_time[s]=1
# print(count_time)


#plot for No. of tweets vs time(in hours)
l1 = list(count_time.keys())
l2 = list(count_time.values())
trace1 = go.Bar(
    x=l1,
    y=l2,
    marker=dict(
        color='rgb(225,0,0)',
        line=dict(
            color='rgb(8,48,107)',
            width=1.5),
        ),
    opacity=0.55
)
data = [trace1]
py.iplot(data, filename='fil')


#part e, printing formula
tweets = tweets_collection.find({})
retweet_dict=dict()
favCount_dict=dict()
formula=dict()
for i in tweets:
    retweet_dict[i['_id']]=i['retweet_count']
    favCount_dict[i['_id']]=i['favorite_count']
    formula[i['_id']]=(1*(int(i['favorite_count']))) +( 1*(int(i['retweet_count'])) )
import pprint
pp = pprint.PrettyPrinter(indent=4)
# # pp.pprint(retweet_dict)
# pp.pprint(favCount_dict)

pp.pprint(formula)


retweets=[]
l = tweets_collection.find({})
for i in l:
    retweets.append(api.retweeters(i['id']))



#part c
count_retweets=dict()
for i in retweets:
    for j in i:
        if(j in count_retweets):
            count_retweets[j]+=1
        else:
            count_retweets[j]=1
            
import pprint
pp = pprint.PrettyPrinter(indent=4)
import operator
sorted_count_retweets = sorted(count_retweets.items(), key=operator.itemgetter(1))
sorted_count_retweets=list(reversed(sorted_count_retweets))

# pp.pprint(sorted_count_retweets)
frequency=dict()
for i in range(10):
    frequency[sorted_count_retweets[i][0]]=sorted_count_retweets[i][1]

    
ids=list()
for i in range(10):
    ids.append(sorted_count_retweets[i][0])
# print(ids)


def num_to_string(s):
    d = ""
    for i in s:
        d+=chr(int(i)+65)
    return d


new_freq = {}
for i in frequency:
    new_freq[num_to_string(str(i))] = frequency[i]






info=list()
followers_dict=dict()
followees_dict=dict()
location_dict=dict()
profiles_dict=dict()
fav_count=dict()

for i in range(10):
    h=api.get_user(ids[i])
    info.append(h._json)
    profiles_dict[ids[i]]=info[i]['screen_name']

   
names=list()
for i in profiles_dict:
    names.append(profiles_dict[i])
# print(names)

for i in range(10):
    followers_dict[names[i]]=info[i]['followers_count']  
    location_dict[names[i]]=info[i]['location']
    followees_dict[names[i]]=info[i]['friends_count']
    fav_count[names[i]]=info[i]['favourites_count']
    
    
    

print(location_dict)   


#plotting frequency
l1 = list(new_freq.keys())
l2 = list(new_freq.values())
trace1 = go.Bar(
    x=l1,
    y=l2,
    marker=dict(
        color='rgb(255,211,0)',
        line=dict(
            color='rgb(8,48,107)',
            width=1.5),
        ),
    opacity=0.55
)
data = [trace1]
py.iplot(data, filename='fil')


#plotting followers
l1 = list(followers_dict.keys())
l2 = list(followers_dict.values())
trace1 = go.Bar(
    x=l1,
    y=l2,
    marker=dict(
        color='rgb(225,0,0)',
        line=dict(
            color='rgb(8,48,107)',
            width=1.5),
        ),
    opacity=0.55
)
data = [trace1]
py.iplot(data, filename='fil')


#plotting followees


l1 = list(followees_dict.keys())
l2 = list(followees_dict.values())
trace1 = go.Bar(
    x=l1,
    y=l2,
    marker=dict(
        color='rgb(254,127,156)',
        line=dict(
            color='rgb(8,48,107)',
            width=1.5),
        ),
    opacity=0.55
)
data = [trace1]
py.iplot(data, filename='fil')


#plotting favourite count

l1 = list(fav_count.keys())
l2 = list(fav_count.values())
trace1 = go.Bar(
    x=l1,
    y=l2,
    marker=dict(
        color='rgb(106,13,173)',
        line=dict(
            color='rgb(8,48,107)',
            width=1.5),
        ),
    opacity=0.55
)
data = [trace1]
py.iplot(data, filename='fil')


get_ipython().system('pip install gmplot')
get_ipython().system('pip install geopy')



import ssl

ssl._create_default_https_context = ssl._create_unverified_context
from geopy.geocoders import Nominatim 
geolocator = Nominatim(user_agent="nishtha17354") 
locations=list(location_dict.values())

latitudes = []
longitudes = []
for i in locations:
    loc = geolocator.geocode(i)
    if(loc != None):
        latitudes.append(loc.latitude)
        longitudes.append(loc.longitude)
        


print(longitudes)
print(latitudes)





import gmplot 
gmap4 = gmplot.GoogleMapPlotter(28.7041, 77.1025, 5)
gmap4.scatter( latitudes, longitudes, '# FF0000', size = 40, marker = False )
gmap4.heatmap( latitudes, longitudes )
gmap4.draw( "map1.html" )



followers = []
for follower in tweepy.Cursor(api.followers_ids, screen_name = 'GameOfThrones').pages():
    followers.extend(follower)





print(len(followers))
print(followers)





tweets_collection = twitter_db['followers_collections']





#storing followers
import time
i = 0
follower_collection = twitter_db['followers']
while(i < len(followers)):
    try:
        follower = api.get_user(followers[i])._json
        follower['_id'] = follower['id_str']
        follower_collection.insert_one(follower)
    except:
        time.sleep(30)
    i+=1




# part b
def getFollowersLocations():
    locations = []
    tweets_collection = twitter_db['followers']
    followers = tweets_collection.find({})
    for i in followers:
        if(i['profile_location'] != None):
            locations.append(i['profile_location']['name'])
            continue
        if(i['location'] != ''):
            locations.append(i['location'])
    return locations


# locations = getFollowersLocations()
# latitudes = []
# longitudes = []
# print(len(locations))



import ssl

ssl._create_default_https_context = ssl._create_unverified_context
from geopy.geocoders import Nominatim 
geolocator = Nominatim(user_agent="nishtha17354") 

for i in range(2001,len(locations)):
    print(i)
    loc = geolocator.geocode(locations[i])
    if(loc != None):
        latitudes.append(loc.latitude)
        longitudes.append(loc.longitude)


import gmplot 
gmap4 = gmplot.GoogleMapPlotter(28.7041, 77.1025, 5)

gmap4.heatmap( latitudes, longitudes ) 
gmap4.draw("map2.html")
