from urllib import urlencode
import urllib2
import time
from hashlib import sha512
from hmac import HMAC
import base64
import json

# Adapted from snippets found https://bitcointalk.org/index.php?amp;topic=49789.20
# This code displays account balance information

# enter API credentials here
auth_key = ''
auth_secret = ''

url_info = "https://mtgox.com/api/0/info.php" # using older API

def get_nonce():
    return int(time.time()*100000)

def sign_data(secret, data):
    return base64.b64encode(str(HMAC(secret, data, sha512).digest()))
      

class requester:
    def __init__(self, auth_key, auth_secret):
        self.auth_key = auth_key
        self.auth_secret = base64.b64decode(auth_secret)
        
    def build_query(self, req={}):
        req["nonce"] = get_nonce()
        post_data = urlencode(req)
        headers = {}
        headers["User-Agent"] = "GoxApi"
        headers["Rest-Key"] = self.auth_key
        headers["Rest-Sign"] = sign_data(self.auth_secret, post_data)
        return (post_data, headers)
        
    def perform(self, url, args):
        data, headers = self.build_query(args)
        req = urllib2.Request(url, data, headers)
        res = urllib2.urlopen(req, data)
        return json.load(res)

args = {}
tuer = requester(auth_key,auth_secret)
r = tuer.perform(url_info,args)

#print "Balance:"
USD = r['Wallets']['USD']['Balance']['display']
print "USD: ",USD

BTC = r['Wallets']['BTC']['Balance']['display']
print "BTC: B"+BTC[0:10]
