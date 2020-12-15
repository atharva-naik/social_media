import colors
import pandas as pd
from colors import color

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

class TwitterProfile(object):
    def __init__(self, name, username, bio, join_date, followers, following, tweets, link=None, location=None, isverified=False, profile_pic=None, banner_pic=None):
        self.name=name
        self.username=username
        self.bio=bio
        self.link=link
        self.isverified=isverified
        self.followers=followers
        self.following=following
        self.tweets=tweets
        self.location=location
        self.join_date=join_date
        self.profile_pic=profile_pic
        self.banner_pic=banner_pic

    def __str__(self):
        op = f"{self.name} "
        if self.isverified:
            op += color(f"✓", fg="blue")
        op += "\n"
        op += f"{self.tweets} Tweets\n"
        if self.bio:
            op += f"{self.bio}\n"
        if self.location:
            op += f"⌖  {self.location} "
        if self.link:
            op += f"🔗  {self.link} "
        op += f"📅  Joined {self.join_date}\n"
        op += f"{self.following} Following {self.followers} Followers\n"
        
        return op

    def __repr__(self):
        return f"{self.username}: {self.name}, {self.tweets} tweets, {self.followers} followers, following {self.following} ..."

    def to_dict(self):
        profile={}

        profile['name']=self.name
        profile['username']=self.username
        profile['bio']=self.bio 
        profile['link']=self.link
        profile['isverified']=self.isverified
        profile['followers']=self.followers
        profile['following']=self.following
        profile['tweets']=self.tweets
        profile['date joined']=self.join_date
        profile['profile photo']=self.profile_pic
        profile['banner photo']=self.banner_pic

        return profile