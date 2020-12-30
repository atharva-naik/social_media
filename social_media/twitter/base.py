import colors
import selenium
import pandas as pd
from .models import *
import os
import time
import random
from colors import color
import tqdm
import logging
import calendar
from selenium import webdriver
from string import ascii_lowercase
from datetime import datetime, timedelta
from dotenv import load_dotenv, find_dotenv
from webdriver_manager.utils import ChromeType
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from social_media.utils import smart_int, get_attribute_rec, clean_url
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, ElementClickInterceptedException


class TwitterEngine(object):
    """
    The TwitterEngine class contains all the methods necessary to perform basic user functions
    Data members
    patience : time waited implicitly for elements to load
    driver : the webdriver onject for using selinium
    List of member functions
    """

    def __init__(self, patience=5, maximize=True):
        super().__init__()
        load_dotenv(find_dotenv())
        self.type = "twitter"
        self.patience = patience
        self.logged_in = False
        if self.patience <= 0:
            self.patience = 1
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        self.driver = webdriver.Chrome(ChromeDriverManager(
            chrome_type=ChromeType.GOOGLE).install(), chrome_options=chrome_options)
        if maximize:
            self.driver.maximize_window()

    def __repr__(self):
        if self.logged_in:
            return f"Twitter engine with patience={self.patience}, user logged in ..."
        else:
            return f"Twitter engine with patience={self.patience}, user not logged in ..."

    def scrolly(self):
        for i in range(10):
            self.driver.execute_script(
                "window.scroll(0, document.body.scrollHeight);")
            self.driver.implicitly_wait(self.patience)
            time.sleep(0.5)
            self.driver.execute_script("window.scroll(0,0);")
            self.driver.implicitly_wait(self.patience)
            time.sleep(0.5)

    def login(self, email=None, username=None, contact=None, password=None, read_from_env=True):
        uid = ''
        if read_from_env:
            email = os.environ.get('TWITTER_EMAIL')
            password = os.environ.get('TWITTER_PASSWORD')
            contact = os.environ.get('TWITTER_CONTACT')
            username = os.environ.get('TWITTER_USERNAME')

        if email is None:
            if contact is None:
                if username is None:
                    print("Username, contact number and email can't all be None")
                else:
                    uid = username
            else:
                uid = contact
        else:
            uid = email
        if password is None:
            print("Password can't be None")
            return

        self.driver.get('https://twitter.com/')
        self.driver.implicitly_wait(self.patience)
        login_btn = self.driver.find_element_by_xpath(
            "//span[text()='Log in']")
        login_btn.click()

        time.sleep(2.1)
        self.driver.implicitly_wait(self.patience)
        uid_field = self.driver.find_element_by_xpath(
            "//input[@name='session[username_or_email]']")
        for letter in uid:
            uid_field.send_keys(letter)
            time.sleep(0.01*random.randint(5, 15))

        password_field = self.driver.find_element_by_xpath(
            "//input[@name='session[password]']")
        for letter in password:
            password_field.send_keys(letter)
            time.sleep(0.01*random.randint(5, 15))

        time.sleep(1)
        self.driver.implicitly_wait(self.patience)
        submit_btn = self.driver.find_element_by_xpath(
            "//div[@data-testid='LoginForm_Login_Button']")
        submit_btn.click()
        self.driver.implicitly_wait(self.patience)

        if self.driver.current_url == r"https://twitter.com/login?email_disabled=true&redirect_after_login=%2F":
            if username is not None:
                time.sleep(3)
                self.driver.implicitly_wait(self.patience)
                uid_field = self.driver.find_element_by_xpath(
                    "//input[@name='session[username_or_email]']")
                for letter in username:
                    uid_field.send_keys(letter)
                    time.sleep(0.01*random.randint(5, 15))

                password_field = self.driver.find_element_by_xpath(
                    "//input[@name='session[password]']")
                for letter in password:
                    password_field.send_keys(letter)
                    time.sleep(0.01*random.randint(5, 15))

                time.sleep(1)
                self.driver.implicitly_wait(self.patience)
                submit_btn = self.driver.find_element_by_xpath(
                    "//div[@data-testid='LoginForm_Login_Button']")
                submit_btn.click()

                self.driver.implicitly_wait(self.patience)
                time.sleep(0.5)

    def get_profile(self, username):
        start = time.time()
        self.driver.get(f"https://twitter.com/{username.replace('@','')}")
        self.driver.implicitly_wait(self.patience)

        try:
            try:
                username = username
                name = self.driver.find_element_by_xpath(
                    "//a[contains(@href, '/photo')]").find_element_by_xpath("../following-sibling::div").text.split('\n')[0]
                tweets = smart_int(self.driver.find_element_by_xpath(
                    ".//div[contains(text(), 'Tweets')]").text.split()[0])
                bio = self.driver.find_element_by_xpath("//div[@data-testid='UserDescription']").text if len(
                    self.driver.find_elements_by_xpath("//div[@data-testid='UserDescription']")) > 0 else None
                profile_header = self.driver.find_element_by_xpath(
                    "//div[@data-testid='UserProfileHeader_Items']")
                join_date = profile_header.find_elements_by_xpath(
                    ".//span")[-1].text.replace("Joined", "").strip()
                # try:
                #     verified = self.driver.find_element_by_xpath("//*[local-name() = 'svg'][@aria-label='Verified account']")
                #     verified_name = self.driver.find_element_by_xpath("//*[local-name() = 'svg'][@aria-label='Verified account']/../preceding-sibling::span").text
                #     if verified_name == name:
                #         isverified = True
                #     else:
                #         isverified = False
                # except:
                #     isverified = False
                isverified = True if len(self.driver.find_element_by_xpath("//a[contains(@href, '/photo')]").find_element_by_xpath(
                    "../following-sibling::div").find_elements_by_xpath("//*[local-name() = 'svg'][@aria-label='Verified account']")) > 0 else False

                following = self.driver.find_element_by_xpath(
                    "//a[contains(@href, 'following')]").text.split()[0]
                following = smart_int(following)
                followers = self.driver.find_element_by_xpath(
                    "//a[contains(@href, 'followers')]").text.split()[0]
                followers = smart_int(followers)

                link = profile_header.find_elements_by_xpath(".//a")
                if len(link) > 0:
                    link = link[0].text
                else:
                    link = None

                location = profile_header.find_elements_by_xpath(
                    ".//span")[0].text
                if 'Joined' in location:
                    location = None

                # self.driver.get(f"https://twitter.com/{username.replace('@','')}/header_photo")
                # self.driver.implicitly_wait(self.patience)
                # banner_photo = self.driver.find_elements_by_xpath("//img[@alt='Image' and @draggable='true']")
                # if len(banner_photo)>0:
                #     banner_photo = banner_photo[0].get_attribute("src")
                # else:
                #     banner_photo = None
                banner_photo = self.driver.find_element_by_xpath("//a[contains(@href, 'header_photo')]").find_element_by_xpath(
                    ".//img").get_attribute("src") if len(self.driver.find_elements_by_xpath("//a[contains(@href, 'header_photo')]")) > 0 else None
                profile_photo = self.driver.find_element_by_xpath("//a[contains(@href, '/photo')]").find_element_by_xpath(
                    ".//img").get_attribute("src") if len(self.driver.find_elements_by_xpath("//a[contains(@href, '/photo')]")) > 0 else None

                # self.driver.get(f"https://twitter.com/{username.replace('@','')}/photo")
                # self.driver.implicitly_wait(self.patience)
                # profile_photo = self.driver.find_elements_by_xpath("//img[@alt='Image' and @draggable='true']")
                # if len(profile_photo)>0:
                #     profile_photo = profile_photo[0].get_attribute("src")
                # else:
                #     profile_photo = None

                # self.driver.get("https://twitter.com/home")
                # self.driver.implicitly_wait(self.patience)
                # print(color(f"profile fetched in {time.time()-start} s ...", fg='yellow', style='bold'))

                return TwitterProfile(name=name,
                                      username=username,
                                      bio=bio,
                                      join_date=join_date,
                                      followers=followers,
                                      following=following,
                                      tweets=tweets,
                                      link=link,
                                      location=location,
                                      isverified=isverified,
                                      profile_pic=profile_photo,
                                      banner_pic=banner_photo)
            except:
                notice = self.driver.find_element_by_xpath(
                    "//span[contains(text(), 'This account')]")
                print(notice.find_element_by_xpath("../..").text)
                return None

        except:
            notice = self.driver.find_element_by_xpath(
                "//span[contains(text(), 'Account suspended')]")
            print(notice.find_element_by_xpath("../..").text)
            return None

    def logout(self):
        self.driver.get("https://twitter.com/home")
        self.driver.implicitly_wait(self.patience)

        account_switcher = self.driver.find_element_by_xpath(
            "//div[@data-testid='SideNav_AccountSwitcher_Button']")
        account_switcher.click()
        self.driver.implicitly_wait(self.patience)

        logout_btn = self.driver.find_element_by_xpath("//a[@href='/logout']")
        logout_btn.click()
        self.driver.implicitly_wait(self.patience)

        submit_btn = self.driver.find_element_by_xpath(
            "//span[text()='Log out']")
        submit_btn.click()
        self.driver.implicitly_wait(self.patience)
        # time.sleep(0.5)
    """
    since: a lower limit on dates
    until: an upper limit on dates
    top: get tweets with more engagement (boolean flag)
    if top is set to false (the default value), results 
    from the latest tab are fetched

    Enter since and until as yyyy/mm/dd
    """

    def advanced_search(self, query='', to=None, top=False, until=None, since=None, hashtags=None):
        if hashtags:
            query += " ("
            for hashtag in hashtags:
                if hashtag.startswith('#'):
                    query += (hashtag+' OR ')
                else:
                    query += ('#'+hashtag+' OR ')
            query = query[:-4]
            query += ")"

        if to:
            query += f' to:{to}'

        if until:
            query += f' until:{until}'
        if since:
            query += f' since:{since}'

        latest = not(top)
        self.search(query, latest)
        time.sleep(2)

    def search(self, query="""lol`&?""", latest=True):
        query = clean_url(query)
        search_url = f"https://twitter.com/search?q={query}&src=typed_query"
        if latest:
            search_url += "&f=live"
        self.driver.get(search_url)
        self.driver.implicitly_wait(self.patience)
        time.sleep(3)
        self.scrolly()
        # search_bar = self.driver.find_element_by_xpath("//input[@data-testid='SearchBox_Search_Input']")
        # self.driver.implicitly_wait(self.patience)
        # search_bar.clear()
        # search_bar.send_keys(query + Keys.ENTER)
        # self.driver.implicitly_wait(self.patience)
        # time.sleep(0.5)

    def tweet(self, text=''):
        self.driver.get("https://twitter.com/compose/tweet")
        self.driver.implicitly_wait(self.patience)
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

    def get_tweets(self, limit=20, filter=None, save=True, output='tweets.csv', return_df=False):
        tweet = self.driver.find_element_by_xpath(
            "//div[@aria-label='Timeline: Search timeline']/div/div")
        results = []
        limit += int(0.08*limit)
        STOPS = 0

        for i in tqdm.tqdm(range(limit)):
            self.driver.execute_script("arguments[0].scrollIntoView();", tweet)
            self.driver.implicitly_wait(self.patience)
            try:
                content = tweet.find_element_by_xpath(
                    ".//div[@data-testid='tweet']")
            except NoSuchElementException:
                try:
                    tweet = tweet.find_element_by_xpath(
                        "./following-sibling::div")
                    continue
                except NoSuchElementException:
                    print(color(
                        f"Truncating at {len(results)} tweets, as no more results exist ...", fg='yellow', style='bold'))
                    if save:
                        df = dump_tweets(results)
                        df.to_csv(output)
                    if return_df:
                        return dump_tweets(results)
                    else:
                        return results

            links = content.find_elements_by_tag_name('a')
            links = [link.get_attribute("href") for link in links]
            # mostly goes to except for ads
            try:
                permalink = links[2]
                tweet_id = int(links[2].split('/')[-1])
            except:
                tweet = tweet.find_element_by_xpath("./following-sibling::div")
                # print(f"{content.text} has an issue")
                continue

            try:
                likes = smart_int(content.find_element_by_xpath(
                    ".//div[@data-testid='like']").text)
            except:
                likes = smart_int(content.find_element_by_xpath(
                    ".//div[@data-testid='unlike']").text)
            replies = smart_int(content.find_element_by_xpath(
                ".//div[@data-testid='reply']").text)
            try:
                retweets = smart_int(content.find_element_by_xpath(
                    ".//div[@data-testid='retweet']").text)
            except:
                retweets = smart_int(content.find_element_by_xpath(
                    ".//div[@data-testid='unretweet']").text)

            hashtags = ['#'+link.split('/')[-1].split('?')[0]
                        for link in links if'?src=hashtag_click' in link]
            lang = get_attribute_rec(content, 'lang')
            username = content.find_element_by_xpath(
                ".//span[contains(text(), '@')]").text

            timestamp = content.find_element_by_xpath(
                ".//time").get_attribute('datetime')
            name = content.find_element_by_xpath(".//span").text
            text = content.find_elements_by_xpath(
                ".//div[@dir='auto']")[3].text
            tweet_object = Tweet(text=text,
                                 links=links,
                                 driver=self.driver,
                                 patience=self.patience,
                                 permalink=permalink,
                                 hashtags=hashtags,
                                 tweet_id=tweet_id,
                                 lang=lang,
                                 username=username,
                                 name=name,
                                 likes=likes,
                                 replies=replies,
                                 retweets=retweets,
                                 timestamp=timestamp)
            results.append(tweet_object)
            for j in range(self.patience):
                try:
                    tweet = tweet.find_element_by_xpath(
                        "./following-sibling::div")
                    break
                except:
                    print(color("Waiting for page to load ...",
                                fg='red', style='bold'))
                    time.sleep(1)
            if j == self.patience:
                print(color("skipping ...", fg='red', style='bold'))
                continue

            while tweet.text == '':
                try:
                    tweet = tweet.find_element_by_xpath(
                        "./following-sibling::div")
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView();", tweet)
                    self.driver.implicitly_wait(self.patience)
                    break
                except Exception as error:
                    # just avoid the weird old Stale Element error for now
                    if isinstance(error, StaleElementReferenceException):
                        continue
                    elif isinstance(error, NoSuchElementException):
                        STOPS += 1
                        if i == limit-1:
                            if save:
                                df = dump_tweets(results)
                                df.to_csv(output)
                            if return_df:
                                return dump_tweets(results)
                            else:
                                return results
                        if STOPS <= 5:
                            self.scrolly()
                            continue
                        else:
                            # time.sleep(5)
                            print(color(
                                f"Truncating at {len(results)} tweets, as no more results exist ...", fg='yellow', style='bold'))
                            if save:
                                df = dump_tweets(results)
                                df.to_csv(output)
                            if return_df:
                                return dump_tweets(results)
                            else:
                                return results
        if save:
            df = dump_tweets(results)
            df.to_csv(output)
        if return_df:
            return dump_tweets(results)
        else:
            return results
            # while True:
            #     try:
            #         tweet = tweet.find_elements_by_xpath("./following-sibling::div")
            #         break
            #     except:
            #         time.sleep(0.5)

    def close(self, wait_for_input=False):
        if wait_for_input:
            while True:
                i = input("Please enter q to quit now!\n")
                if i == 'q':
                    try:
                        self.logout()
                        self.driver.implicitly_wait(self.patience)
                        self.driver.quit()
                    except:
                        self.driver.quit()
                    break
        else:
            try:
                self.logout()
                self.driver.implicitly_wait(self.patience)
                self.driver.quit()
            except:
                self.driver.quit()
