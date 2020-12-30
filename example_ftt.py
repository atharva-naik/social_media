# fetch tweets from twitter
from social_media.twitter.base import TwitterEngine
t = TwitterEngine()
t.search('"cancel culture"')
tweets = t.get_tweets(limit=200)
t.close(wait_for_input=True)