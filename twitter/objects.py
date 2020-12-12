import pandas as pd

class Tweet(object):
    def __init__(self, text, tweet_id, permalink, username, name, lang, timestamp, links=None, hashtags=None):
        self.text=text
        self.id=tweet_id
        self.permalink=permalink
        self.username=username
        self.name=name
        self.lang=lang
        self.timestamp=timestamp
        self.links=links
        self.hashtags=hashtags

    def to_dict(self):
        tweet={}
        tweet['id']=self.id
        tweet['permalink']=self.permalink
        tweet['text']=self.text
        tweet['date']=self.timestamp
        tweet['username']=self.username
        tweet['name']=self.name
        tweet['hashtags']=self.hashtags
        tweet['links']=self.links
        tweet['lang']=self.lang

        return tweet

    def __str__(self):
        op=f"id={self.id} text={self.text} \ntimestamp={self.timestamp} username={self.username} \npermalink={self.permalink} name={self.name} \nlinks={self.links} \nhastags={self.hashtags} lang={self.lang}"
        return op

    def __repr__(self):
        return self.__str__()

def tweets_to_df(tweets):
    tweets_df = []
    for tweet in tweets:
        tweets_df.append(tweet.to_dict())
    
    return pd.DataFrame(tweets_df)