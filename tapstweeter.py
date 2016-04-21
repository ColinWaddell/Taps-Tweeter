import tweepy
import time
import sys
import urllib
import json
import os

CACHE_DIR = "sent_cache"

#Load API keys
execfile('config.py')

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
  #cfg pulled in from config.py
  api = get_api(cfg)
  #status = api.update_status(status=tweet)
  print "Tweeting: "+tweet

def get_api(cfg):
  auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
  auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
  return tweepy.API(auth)

def main(location):
  cache_file = generate_location_date_filename(location)
  if os.path.isfile(cache_file):
    return

  if get_taps_status(location):
    send_tweet(location)
  else:
    print ("Taps Oan")

if __name__ == "__main__":
  if len(sys.argv)>1:
    location = sys.argv[1]
    main(location)
  else:
    print "No location specified"
