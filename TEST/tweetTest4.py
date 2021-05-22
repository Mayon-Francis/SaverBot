import tweepy
import logging
import time
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

#GET KEYS FROM ENVIRONMENT VARIABLE  
if('TWITTER_API_KEY' in os.environ):
    TWITTER_API_KEY = str(os.environ['TWITTER_API_KEY'])
else:
    logger.error("cannot access api key") 
    raise Exception("Couldn't Read Api Key from Env Variable!!")

if('TWITTER_API_SECRET_KEY' in os.environ):
    TWITTER_API_SECRET_KEY = str(os.environ['TWITTER_API_SECRET_KEY'])
else:
    logger.error("cannot access api key secret") 
    raise Exception("Couldn't Read Api Key Secret from Env Variable!!")

if('TWITTER_ACCESS_TOKEN' in os.environ):
    TWITTER_ACCESS_TOKEN = str(os.environ['TWITTER_ACCESS_TOKEN'])
else:
    logger.error("cannot access, Access Token") 
    raise Exception("Couldn't Read Twitter Access Token from Env Variable!!")

if('TWITTER_ACCESS_TOKEN_SECRET' in os.environ):
    TWITTER_ACCESS_TOKEN_SECRET = str(os.environ['TWITTER_ACCESS_TOKEN_SECRET'])
else:
    logger.error("cannot access, Access Token Secret") 
    raise Exception("Couldn't Read Twitter Access Token Secret from Env Variable!!")




# Authenticate to Twitter
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET_KEY)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)



def check_mentions(api, since_id):
    logger.info("Retrieving mentions")
    new_since_id = since_id

    for tweet in tweepy.Cursor(api.search, q="@saverbot1", since_id = since_id).items():
        new_since_id = max(tweet.id, new_since_id)

        #only get mentions that are replies to other tweets
        if tweet.in_reply_to_status_id_str is None:
            continue
        else:
            parentTweet = api.get_status(tweet.in_reply_to_status_id_str)
            logger.info(f"Sending tweet with Id: {parentTweet.id_str} to {tweet.user.name}") 
            direct_message = api.send_direct_message(tweet.user.id, parentTweet.text)  
            print(parentTweet.text)
        
    return new_since_id
         
         
        

since_id = 1
try:
    api.verify_credentials()
    print("Authentication OK")
except:
    raise Exception("Error during authentication")

while True:
    since_id = check_mentions(api, since_id)
    logger.info("Waiting...")
    time.sleep(5)
