while True:
    try:
        f=open('since_id.txt','r')
        since_id = int(f.read())
        f.close()

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
            logger.error("Couldn't Read Api Key from Env Variable!!")

        if('TWITTER_API_SECRET_KEY' in os.environ):
            TWITTER_API_SECRET_KEY = str(os.environ['TWITTER_API_SECRET_KEY'])
        else:
            logger.error("cannot access api key secret") 
            logger.error("Couldn't Read Api Key Secret from Env Variable!!")

        if('TWITTER_ACCESS_TOKEN' in os.environ):
            TWITTER_ACCESS_TOKEN = str(os.environ['TWITTER_ACCESS_TOKEN'])
        else:
            logger.error("cannot access, Access Token") 
            logger.error("Couldn't Read Twitter Access Token from Env Variable!!")

        if('TWITTER_ACCESS_TOKEN_SECRET' in os.environ):
            TWITTER_ACCESS_TOKEN_SECRET = str(os.environ['TWITTER_ACCESS_TOKEN_SECRET'])
        else:
            logger.error("cannot access, Access Token Secret") 
            logger.error("Couldn't Read Twitter Access Token Secret from Env Variable!!")




        # Authenticate to Twitter
        auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET_KEY)
        auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)

        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


        #Bot User Object (self)
        screen_name = "saverbot1"
        botUser = api.get_user(screen_name)

        class pendingTweets:
            recieverId = ""
            parentTweetId = ""
            iterationsOver = 1

            def __init__(self, recieverId, parentTweetId):
                self.recieverId = recieverId
                self.parentTweetId = parentTweetId

        pendingTweetsList = list()



        def sendDm(recieverId, message):
            logger.info(f"Attempting to send tweet with message: '{message}' for person with Id{recieverId}")
            try: 
                api.send_direct_message(recieverId,message)
                logger.info("Dm sent Successfully")
                return "success"
            except tweepy.TweepError as e:
                logger.info(e.reason)
                return e.reason
        
        ## PENDING DOES NOT WORK YET!!
        def tryPending(pendingTweetsList):
            listLen = len(pendingTweetsList)
            listLen -=1
            while(listLen >= 0):
                instance = pendingTweetsList[listLen]
                dmStatus = sendDm(instance.recieverId, "https://twitter.com/twitter/statuses/"+ instance.parentTweetId )
                if(dmStatus == "success"):
                    pendingTweetsList.pop(listLen)
                    listLen-=1
                    continue
                elif (instance.iterationsOver > 120960 ) :   # adjust 120960 which is 7 days as per requirements,
                    pendingTweetsList.pop(listLen)
                    listLen-=1
                else:
                    pendingTweetsList[listLen].iterationsOver+=1
                listLen-=1                
            

            return pendingTweetsList

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
                        parentTweet = api.get_status(tweet.in_reply_to_status_id_str)
                        dmStatus = sendDm(tweet.user.id, "https://twitter.com/twitter/statuses/"+ parentTweet.id_str)

                        if(dmStatus == "success"):
                            continue
                        elif (dmStatus == "[{'code': 144, 'message': 'No status found with that ID.'}]"):
                            logger.info(f"Replying to {tweet.user.name}'s tweet with Id: {tweet.id_str} : parent tweet deleted")
                            api.update_status(status = 'Uh oh, seems like that tweet was deleted!', in_reply_to_status_id = tweet.id , auto_populate_reply_metadata=True)
                            continue
                        else:
                            logger.info(f"adding {tweet.user.id_str}'s {parentTweet.id_str} to pendingTweets")
                            pendingTweetsList.append(pendingTweets(tweet.user.id_str, parentTweet.id_str))  # 1 so that initialise with iterated times 1 
            
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
            logger.error("Error during authentication")


        while True:
            since_id = check_mentions(api, since_id)
            f= open("since_id.txt","w")
            f.write(str(since_id))
            f.close()
            if( len(pendingTweetsList) != 0 ):
                logger.info("Trying Peninding...")
                print(pendingTweetsList)
                pendingTweetsList = tryPending(pendingTweetsList)

            logger.info("Waiting...")
            time.sleep(5)
                


    except tweepy.TweepError as e:
        import logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger()
        logger.error(e.reason)
        logger.error("Full Refresh")
    except:
        logger.error("Full Refresh")