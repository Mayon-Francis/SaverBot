import tweepy

# Authenticate to Twitter
auth = tweepy.OAuthHandler("2V9sr0LnXGYd4xhHpaHo0qAiN", 
    "bAWaOApquGcBbgBhPUVRlsB8gYxagm9uXdFGtYjw7hmmLHf5q4")
auth.set_access_token("1395238073303126016-sUuVvRffNxLfO7EbvYFKUCA3tKYw4W", 
    "axpj3XB1lWQy75YTnpQRJQ5d6izelf85ybYUEUFO7lHYs")

api = tweepy.API(auth, wait_on_rate_limit=True,
                wait_on_rate_limit_notify=True)

try:
    api.verify_credentials()
    print("Authentication OK")
    for tweet in api.search(q="Python", lang="en", rpp=10):
        print(f"{tweet.user.name}:{tweet.text}")

except:
    print("Error during authentication")