import tweepy

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

try:
    api.verify_credentials()
    print("Authentication OK")
    since_id = 1
    for tweet in tweepy.Cursor(api.mentions_timeline,since_id=since_id).items():
        print(api.get_status(tweet.in_reply_to_status_id_str).text)
        print(tweet.text)
        

except:
    print("Error during authentication")