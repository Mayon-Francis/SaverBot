while True:
    f=open('since_id.txt','r')

    since_id = int(f.read())
    f.close()
    try:

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


        #Bot User Object (self)
        screen_name = "saverbot1"
        botUser = api.get_user(screen_name)



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
                            parentTweet = api.get_status(tweet.in_reply_to_status_id_str)
                            logger.info(f"Saving tweet with Id: {parentTweet.id_str} for {tweet.user.name}") 
                            api.send_direct_message(tweet.user.id,"https://twitter.com/twitter/statuses/"+str(parentTweet.id) ) 
                            print(parentTweet.text)

                        #they might not be following us
                        except tweepy.TweepError as e:
                            logger.info(e.reason)
                            if e.reason == "[{'code': 144, 'message': 'No status found with that ID.'}]":
                                logger.info(f"Replying to {tweet.user.name}'s tweet with Id: {tweet.id_str} ,parent tweet deleted")
                                api.update_status(status = 'Uh oh, seems like that tweet was deleted!', in_reply_to_status_id = tweet.id , auto_populate_reply_metadata=True)
                                continue
                            
                            
                            logger.info(f"Replying and asking to follow to {tweet.user.name}'s tweet with Id: {tweet.id_str} ")
                            api.update_status(status = 'Please follow @saverbot1 to get this tweet link as DM', in_reply_to_status_id = tweet.id , auto_populate_reply_metadata=True)
                            continue

                except tweepy.TweepError as e:
                    logger.error(e.reason)
                    continue

            return new_since_id
                


        
        try:
            api.verify_credentials()
            print("Authentication OK")
        except:
            raise Exception("Error during authentication")


        while True:
            since_id = check_mentions(api, since_id)
            f= open("since_id.txt","w")
            f.write(str(since_id))
            f.close()
            logger.info("Waiting...")
            time.sleep(5)

    except tweepy.TweepError as e:
        import logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger()
        logger.error(e.reason)
        logger.error("Full Refresh")
