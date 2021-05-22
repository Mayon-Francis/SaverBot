import tweepy
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
# Authenticate to Twitter
auth = tweepy.OAuthHandler("2V9sr0LnXGYd4xhHpaHo0qAiN", 
    "bAWaOApquGcBbgBhPUVRlsB8gYxagm9uXdFGtYjw7hmmLHf5q4")
auth.set_access_token("1395238073303126016-sUuVvRffNxLfO7EbvYFKUCA3tKYw4W", 
    "axpj3XB1lWQy75YTnpQRJQ5d6izelf85ybYUEUFO7lHYs")
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)



#Bot User Object (self)
screen_name = "saverbot1"
botUser = api.get_user(screen_name)
#Stores Ids of followers, most recent follower first according to documentation
bot_followers_ids = api.followers_ids(botUser)




# If the person unfollows us after we get value from api, we will think it follows us, hence there is try,except 
# when trying to send dm
# def checkNotFollower(tid,bot_followers_ids):

#     #check if they already follow us in local storage
#     for id in bot_followers_ids:
#         if id == tid:
#             return False
    
#     #if not, then call api to get list of new followers
#     bot_followers_ids = api.followers_ids(botUser)

#     for id in bot_followers_ids:
#         if id == tid:
#             return False

#     return True      


def check_mentions(api, since_id):
    logger.info("Retrieving mentions")
    new_since_id = since_id

    for tweet in tweepy.Cursor(api.search, q="@saverbot1", since_id = since_id).items():
        try:
            new_since_id = max(tweet.id, new_since_id)
            
            #ignore tweets sent by self
            if tweet.user.id_str == botUser.id_str:
                continue

            #only get mentions that are replies to other tweets
            if tweet.in_reply_to_status_id_str is None:
                continue

            else:
                try:
                    try:
                        parentTweet = api.get_status(tweet.in_reply_to_status_id_str)
                        parentweetfound=True
                    except tweepy.TweepError as e:
                        logger.info(e.reason)
                        parentweetfound=False
                    if parentweetfound:
                      logger.info(f"Saving tweet with Id: {parentTweet.id_str} for {tweet.user.name}") 
                      api.send_direct_message(tweet.user.id,"https://twitter.com/twitter/statuses/"+str(parentTweet.id) ) 
                      print(parentTweet.text)
                    else:
                      
                      api.send_direct_message(tweet.user.id,"Sorry, we cannot find the Tweet you tagged, it may have been deleted" )    

                #they might not be following us
                except tweepy.TweepError as e:
                    logger.info(e.reason)
                    logger.info(f"Replying and asking to follow to {tweet.user.name}'s tweet with Id: {tweet.id_str} ")
                    api.update_status(status = 'Please follow @saverbot1 to get this tweet link as DM', in_reply_to_status_id = tweet.id , auto_populate_reply_metadata=True)
                    continue

        except tweepy.TweepError as e:
            logger.error(e.reason)
            continue

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
