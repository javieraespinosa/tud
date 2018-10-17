
import os

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

from pymongo import MongoClient

import re
import json

file = open('hashtags.txt')
tags = re.findall(r"(#\w+)", file.read())

print(tags)

#consumer key, consumer secret, access token, access secret.
ckey="8u52CraMket0itE8XCPA"
csecret="qlwVq7gOJM87LjjJg6D4Q05gzSXP9BSJ3h8pTL2u8"
atoken="124131670-Zfq6tAVtEqoJEWVZbeloX53eNcaeEhrzl2ux251c"
asecret="Rk7FXZevGTlIms5AWtJr62Nxde4LfcW4D2IXI9eoI1wE0"

class listener(StreamListener):

    def on_data(self, data):
        host = os.environ['MONGO_HOST'] if 'MONGO_HOST' in os.environ else 'localhost'
        client = MongoClient(host, 27017)
        col = client['tud']['tweets']
        col.insert_one( json.loads(data) )
        print(data)
        return(True)

    def on_error(self, status):
        print (status)

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=tags)

