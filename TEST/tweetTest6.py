import tweepy
import logging
import time


# Authenticate to Twitter
auth = tweepy.OAuthHandler("2V9sr0LnXGYd4xhHpaHo0qAiN", 
    "bAWaOApquGcBbgBhPUVRlsB8gYxagm9uXdFGtYjw7hmmLHf5q4")
auth.set_access_token("1395238073303126016-sUuVvRffNxLfO7EbvYFKUCA3tKYw4W", 
    "axpj3XB1lWQy75YTnpQRJQ5d6izelf85ybYUEUFO7lHYs")


api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def checkfollower(tid):
    for follower in tweepy.Cursor(api.followers).items():
      if follower.id == tid:
          return False
    return True      


def check_mentions(api, since_id):
    logger.info("Retrieving mentions")
    new_since_id = since_id

    for tweet in tweepy.Cursor(api.search, q="@saverbot1", since_id = since_id).items():
        new_since_id = max(tweet.id, new_since_id)

        if checkfollower(tweet.user.id):
            api.update_status(status = 'Please follow @saverbot1 to get this tweet link as DM', in_reply_to_status_id = tweet.id , auto_populate_reply_metadata=True)
            continue

        #only get mentions that are replies to other tweets
        if tweet.in_reply_to_status_id_str is None:
            continue
        else:
            parentTweet = api.get_status(tweet.in_reply_to_status_id_str)
            logger.info(f"Saving tweet with Id: {parentTweet.id_str} for {tweet.user.name}") 
           
            api.send_direct_message(tweet.user.id,"https://twitter.com/twitter/statuses/"+str(parentTweet.id) ) 
            print(parentTweet.text)
        
    return new_since_id
         
         
