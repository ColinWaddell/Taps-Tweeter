import tweepy
import time
import sys
import urllib
import json
import os
import csv

CACHE_DIR = "sent_cache"
SITE_URL = "http://taps-aff.co.uk"

#Load API keys
execfile('config.py')

def generate_location_date_filename(location):
  return CACHE_DIR+"/"+location+"-"+time.strftime("%Y-%m-%d")+".csv"

def get_taps_status(location):
  url = "http://taps-aff.co.uk/?api&location="+location
  response = urllib.urlopen(url)
  data = json.loads(response.read())
  if data['taps']=='oan':
    return data
  else:
    return None

def stash_tapsaff_info(status, filename):
    w = csv.writer(open(filename, "w"))
    for key, val in status.items():
        w.writerow([key, val])

def send_tweet(tweet):
  #cfg pulled in from config.py
  try:
    api = get_api(API_KEYS)
    print "Attempting to tweet("+str(len(tweet))+"): "+tweet
    status = api.update_status(status=tweet)
    return True

  except tweepy.error.TweepError:
    print "Error sending tweet"
    return False

def get_api(cfg):
  auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
  auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
  return tweepy.API(auth)

def main(location):
  cache_file = generate_location_date_filename(location)
  if os.path.isfile(cache_file):
    print "Already sent a tweet about "+location
    return

  taps_data=get_taps_status(location)
  if taps_data!=None:
    message="Officially #TapsAff in "+location.upper()+"! "+SITE_URL+" [I'm a robot]"
    success = send_tweet(message)
    if success:
      stash_tapsaff_info(taps_data, cache_file)
  else:
    print ("Taps Oan")

if __name__ == "__main__":
  if len(sys.argv)>1:
    location = sys.argv[1]
    main(location)
  else:
    print "No location specified"
