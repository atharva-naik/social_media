import time
import colors
import random
import pandas as pd
from colors import color
from string import ascii_lowercase
from selenium.webdriver.common.keys import Keys


class Tweet(object):
    def __init__(self, text, tweet_id, permalink, driver, patience, username=None, name=None, lang=None, timestamp=None, likes=None, replies=None, retweets=None, links=None, hashtags=None):
        self.text = text
        self.id = tweet_id
        self.permalink = permalink
        self.driver = driver
        self.patience = patience
        self.username = username
        self.name = name
        self.lang = lang
        self.timestamp = timestamp
        self.links = links
        self.likes = likes
        self.replies = replies
        self.retweets = retweets
        self.hashtags = hashtags

    def to_dict(self):
        tweet = {}
        tweet['id'] = self.id
        tweet['permalink'] = self.permalink
        tweet['text'] = self.text
        tweet['date'] = self.timestamp
        tweet['username'] = self.username
        tweet['name'] = self.name
        tweet['hashtags'] = self.hashtags
        tweet['links'] = self.links
        tweet['lang'] = self.lang

        return tweet

    def __str__(self):
        op = f"id={self.id} text={self.text} \ntimestamp={self.timestamp} username={self.username} \npermalink={self.permalink} name={self.name} \nlinks={self.links} \nhastags={self.hashtags} lang={self.lang}"
        return op

    def __repr__(self):
        return self.__str__()

    def like(self):
        current_url = self.driver.current_url
        self.driver.get(self.permalink)
        self.driver.implicitly_wait(self.patience)
        time.sleep(2)
        try:
            like_btn = self.driver.find_element_by_xpath(
                "//div[@data-testid='like']")
            like_btn.click()
            self.driver.implicitly_wait(self.patience)
            self.likes += 1
        except:
            pass
        self.driver.get(current_url)
        self.driver.implicitly_wait(self.patience)

    def unlike(self):
        current_url = self.driver.current_url
        self.driver.get(self.permalink)
        self.driver.implicitly_wait(self.patience)
        time.sleep(2)
        try:
            like_btn = self.driver.find_element_by_xpath(
                "//div[@data-testid='unlike']")
            like_btn.click()
            self.driver.implicitly_wait(self.patience)
            self.likes -= 1
        except:
            pass
        self.driver.get(current_url)
        self.driver.implicitly_wait(self.patience)

    def reply(self, text):
        current_url = self.driver.current_url
        self.driver.get(self.permalink)
        self.driver.implicitly_wait(self.patience)
        time.sleep(2)
        reply_btn = self.driver.find_element_by_xpath(
            "//div[@data-testid='reply']")
        reply_btn.click()

        text_area = self.driver.find_element_by_xpath(
            "//div[@data-testid='tweetTextarea_0']")
        mistakes = random.randint(1, 4)
        mistake_indices = random.sample(
            [i for i in range(len(text))], mistakes)
        new_text = []
        mask = []
        j = 0

        for i in range(len(text)+mistakes):
            if i in mistake_indices:
                random_letter = random.sample(ascii_lowercase, 1)
                new_text.append(random_letter[0])
                j += 1
                mask.append(0)
            else:
                new_text.append(text[i-j])
                mask.append(1)

        for i, letter in enumerate(new_text):
            text_area.send_keys(letter)
            time.sleep(0.01*random.randint(10, 15))
            if mask[i] == 0:
                text_area.send_keys(Keys.BACKSPACE)
                time.sleep(0.01*random.randint(10, 15))

        submit_btn = self.driver.find_element_by_xpath(
            "//div[@data-testid='tweetButton']")
        submit_btn.click()
        self.driver.implicitly_wait(self.patience)
        time.sleep(0.5)
        self.driver.get(current_url)
        self.driver.implicitly_wait(self.patience)

    def retweet(self):
        current_url = self.driver.current_url
        self.driver.get(self.permalink)
        self.driver.implicitly_wait(self.patience)
        time.sleep(2)

        try:
            retweet_btn = self.driver.find_element_by_xpath(
                "//div[@data-testid='retweet']")
            retweet_btn.click()
            self.driver.implicitly_wait(self.patience)
            time.sleep(1)
            retweet_optn = self.driver.find_element_by_xpath(
                "//div[@data-testid='retweetConfirm']")
            retweet_optn.click()
            self.retweets += 1
        except:
            pass

        time.sleep(1)
        self.driver.get(current_url)
        self.driver.implicitly_wait(self.patience)

    def unretweet(self):
        current_url = self.driver.current_url
        self.driver.get(self.permalink)
        self.driver.implicitly_wait(self.patience)
        time.sleep(2)

        try:
            retweet_btn = self.driver.find_element_by_xpath(
                "//div[@data-testid='unretweet']")
            retweet_btn.click()
            self.driver.implicitly_wait(self.patience)
            time.sleep(1)
            retweet_optn = self.driver.find_element_by_xpath(
                "//div[@data-testid='unretweetConfirm']")
            retweet_optn.click()
            self.replies -= 1
        except:
            pass

        time.sleep(1)
        self.driver.get(current_url)
        self.driver.implicitly_wait(self.patience)


def dump_tweets(tweets):
    tweets_df = []
    for tweet in tweets:
        tweets_df.append(tweet.to_dict())

    return pd.DataFrame(tweets_df)


class TwitterProfile(object):
    def __init__(self, name, username, bio, join_date, followers, following, tweets, link=None, location=None, isverified=False, profile_pic=None, banner_pic=None):
        self.name = name
        self.username = username
        self.bio = bio
        self.link = link
        self.isverified = isverified
        self.followers = followers
        self.following = following
        self.tweets = tweets
        self.location = location
        self.join_date = join_date
        self.profile_pic = profile_pic
        self.banner_pic = banner_pic

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
        profile = {}

        profile['name'] = self.name
        profile['username'] = self.username
        profile['bio'] = self.bio
        profile['link'] = self.link
        profile['isverified'] = self.isverified
        profile['followers'] = self.followers
        profile['following'] = self.following
        profile['tweets'] = self.tweets
        profile['date joined'] = self.join_date
        profile['profile photo'] = self.profile_pic
        profile['banner photo'] = self.banner_pic

        return profile
