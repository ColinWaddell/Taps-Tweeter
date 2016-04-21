import tweepy
import time
import sys
import urllib
import json
import os

CACHE_DIR = "sent_cache"

def generate_location_date_filename(location):
  return CACHE_DIR+"/"+location+"-"+time.strftime("%Y-%m-%d")+".json"

def get_taps_status(location):
  url = "http://taps-aff.co.uk/?api&location="+location
  response = urllib.urlopen(url)
  data = json.loads(response.read())
  if data['taps']=='aff':
    return True
  else:
    return False

def check_tweet_sent(location):
  pass

def send_tweet(tweet):
  # Fill in the values noted in previous step here
  cfg = {
    "consumer_key"        : "DZ9P90gH2s55jnQB64oahbLC6",
    "consumer_secret"     : "epFUhmzLr1nwcd8XWnQaDRgIM0wYe0zabwzCT4UQeQEPIZ4Lpj",
    "access_token"        : "1445997164-niAGZ47NUejugPu22zzbSoZfx322WGTkmmIzzz3",
    "access_token_secret" : "kyWmZtSCS09auF63zK0s2hZVxTQ4kWeZV7S12SNCcwpWK"
    }

  api = get_api(cfg)
  status = api.update_status(status=tweet)
  # Yes, tweet is called 'status' rather confusing


def get_api(cfg):
  auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
  auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
  return tweepy.API(auth)

def main(location):
  cache_file = generate_location_date_filename(location)
  if os.path.isfile(cache_file):
    return

  if get_taps_status(location):
    print "Yaldy"

if __name__ == "__main__":
  if len(sys.argv)>1:
    location = sys.argv[1]
    main(location)
