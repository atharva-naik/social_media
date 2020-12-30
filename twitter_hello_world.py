from social_media.base import Engine

twitter_engine = Engine.select('twitter')
twitter_engine.login()

twitter_engine.search('testbot1797')
tweets = twitter_engine.get_tweets(limit=2, save=False)

tweets[0].like()
tweets[0].reply('Hello World')
tweets[0].retweet()
