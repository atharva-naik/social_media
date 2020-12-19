import colors
import requests
import selenium
import prettytable
import pandas as pd
# from .utils import *
from .models import *
from colors import color
from instabot import Bot
import tqdm, logging, calendar
from selenium import webdriver
import os, re, time, random, copy
from string import ascii_lowercase
from prettytable import PrettyTable
from datetime import datetime, timedelta
from dotenv import load_dotenv, find_dotenv
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options  
from webdriver_manager.chrome import ChromeDriverManager 
from social_media.utils import split_by_template, format_time, smart_int, rainbow_text
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, ElementClickInterceptedException

# once you logout, the engine has to be destroyed

class InstagramEngine(object):
    """
    The YouTubeEngine class contains all the methods necessary to perform basic user functions
    Data members
    current_user : username of the account used 
    patience : time waited implicitly for elements to load
    driver : the webdriver onject for using selinium
    List of member functions
    """
    def __init__(self, patience=5, maximize=True):
        super().__init__()
        load_dotenv(find_dotenv())
        self.type = "instagram"  
        self.patience = patience
        self.logged_in = False
        self.username = None
        if self.patience <= 0:
            self.patience = 1    
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
        if maximize:
            self.driver.maximize_window()

    def __repr__(self):
        if self.logged_in:
            return f"Instagram engine with patience={self.patience}, {self.username} is logged in ..."
        else:
            return f"Instagram engine with patience={self.patience}, user is not logged in ..."

    def login(self, email=None, contact=None, username=None, password=None, read_from_env=True):
        if self.logged_in:
            return
        uid = ''
        if read_from_env:
            email = os.environ.get('INSTAGRAM_EMAIL')
            contact = os.environ.get('INSTAGRAM_CONTACT')
            username = os.environ.get('INSTAGRAM_USERNAME')
            password = os.environ.get('INSTAGRAM_PASSWORD')
    
        if email is None:
            if contact is None:
                if username is None:
                    print("Username, contact number and email can't all be None")
                else:
                    uid = username
                    self.username = username
            else:
                uid = contact            
        else:         
            uid = email

        if password is None:
            print("Password can't be None")
            return

        self.driver.maximize_window()
        self.driver.get('http://instagram.com/')
        self.driver.implicitly_wait(self.patience)
        
        uid_field = self.driver.find_element_by_xpath("//input[@name='username']")
        password_field = self.driver.find_element_by_xpath("//input[@name='password']")
        for letter in uid:
            time.sleep(0.01*random.randint(3,20))
            uid_field.send_keys(letter)
        for letter in password:
            time.sleep(0.01*random.randint(3,20))
            password_field.send_keys(letter)

        password_field.send_keys(Keys.ENTER)
        self.driver.implicitly_wait(self.patience)
        self.logged_in = True
        time.sleep(4)

        if not(self.username):
            self.driver.get("https://www.instagram.com/fuck")
            self.driver.implicitly_wait(self.patience)
            self.username = self.driver.find_element_by_xpath("//li[@id='link_profile']").text
        self.driver.get("https://www.instagram.com/")
        self.driver.implicitly_wait(self.patience)

    def get_stories(self, rate=0.5, limit=20):
        self.driver.get("https://www.instagram.com/")
        self.driver.implicitly_wait(self.patience)
        time.sleep(1)

        first_story = self.driver.find_element_by_xpath("//button[@role='menuitem']")
        first_story.click()
        self.driver.implicitly_wait(self.patience)
        time.sleep(3)

        stories = {}
        pause_btn = self.driver.find_element_by_tag_name("svg")
        pause_btn.click()
        forward_btn = self.driver.find_element_by_class_name("coreSpriteRightChevron")
        # backward_btn = self.driver.find_element_by_class_name("coreSpriteLeftChevron")
        num_stories=0
        pbar = tqdm.tqdm(limit)

        while num_stories < limit:
            link = self.driver.current_url 
            date = self.driver.find_element_by_xpath("//time").get_attribute("datetime")
            curr_user = link.split('/')[-3]
            
            if curr_user not in stories:
                stories[curr_user] = [{'link':link, 'date':date}]
                num_stories += 1
                pbar.update(1)
            else:
                stories[curr_user].append({'link':link, 'date':date})
            time.sleep(rate)
            try:
                forward_btn.click()
            except:
                break

        pbar.close()
        return stories

    def feed(self):
        self.driver.get('https://www.instagram.com/')
        self.driver.implicitly_wait(self.patience)
        time.sleep(2)
        iposts = []

        articles = self.driver.find_elements_by_xpath("//article[@role='presentation']")
        for i, article in enumerate(tqdm.tqdm(articles)):
            by = article.text.split('\n')[0]
            try:
                geo = article.find_element_by_xpath(".//a[contains(@href, 'explore')]").text
                geo_link = article.find_element_by_xpath(".//a[contains(@href, 'explore')]").get_attribute("href")
            except:
                geo = None
                geo_link = None
            try:
                meta = article.find_element_by_xpath(".//div/div/div/div/div/img").get_attribute('alt')
            except:
                meta = None
            likes = smart_int(article.find_element_by_xpath(".//button/span").text.strip())

            # article.find_element_by_xpath(".//a[contains(@href, '/p/')]").text.replace(",","")
            timestamp = article.find_element_by_xpath(".//time").get_attribute('datetime')
            timestamp = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f%z")
            # images = article.find_element_by_xpath(".//div/div/div/div/div/img").get_attribute('srcset').split(',')
            images = article.find_element_by_xpath(".//img[@class='FFVAD']").get_attribute('srcset').split(',')
            images = [image.split()[0].strip() for image in images]

            # comments = smart_int(re.findall(r"([0-9]+)", article.find_element_by_xpath(".//a[contains(@href, '/p/')]").replace(",",""))[0])
            comments = smart_int(article.find_element_by_xpath(".//a[contains(@href, '/p/')]").text.split()[-2])
            url = article.find_element_by_xpath(".//a[contains(@href, '/p/')]").get_attribute("href")
            caption = article.find_element_by_xpath(".//div[@data-testid='post-comment-root']").text
            iposts.append(InstagramPost(by=by,
                                        geo=geo,
                                        url=url,
                                        meta=meta,
                                        likes=likes,
                                        images=images,
                                        caption=caption,
                                        comments=comments,
                                        driver=self.driver,
                                        timestamp=timestamp,
                                        patience=self.patience))

        return iposts

    def get_profile(self, user='willsmith', hard=False):
        if hard:
            self.driver.get(f"https://www.instagram.com/{user}/")
            self.driver.implicitly_wait(self.patience)
            time.sleep(2)
            username = user
        else:
            self.search(user, user=True)
            time.sleep(2)
            username = self.driver.current_url.split('/')[-2]

        if self.driver.find_element_by_tag_name('h2') == "Sorry, this page isn't available.":
            print(color('Profile not available!', fg='red'))
            return
        else:
            url = self.driver.current_url
        name = self.driver.find_element_by_xpath("//section//div//h1").text 
        
        posts = smart_int(self.driver.find_element_by_xpath("//li//span//span").text)
        followers = self.driver.find_element_by_xpath("//a[contains(@href, 'followers')]").text.replace("followers","")
        following = self.driver.find_element_by_xpath("//a[contains(@href, 'following')]").text.replace("following","")
        followers = smart_int(followers)
        following = smart_int(following)
        
        try:
            bio = self.driver.find_element_by_xpath("//section//div//h1/../span").text 
        except:
            bio = None
        try:
            link = self.driver.find_element_by_xpath("//section//div//h1/../a").text 
        except:
            link = None
        profile_photo = self.driver.find_element_by_xpath("//img[@data-testid='user-avatar']").get_attribute('src')
        try:
            useless = self.driver.find_element_by_xpath("//span[@title='Verified']")
            isverified = True
        except:
            isverified = False
        return InstagramProfile(url=url,
                                bio=bio,
                                name=name,
                                link=link,
                                posts=posts,
                                username=username,
                                driver=self.driver,
                                following=following,
                                followers=followers,
                                isverified=isverified,
                                patience=self.patience,
                                profile_photo=profile_photo)

    def post(self, img='https://upload.wikimedia.org/wikipedia/en/7/7d/Lenna_%28test_image%29.png', caption="I'm a bot, please ban me"):
        self.logout()
        if 'http' in img:
            open('DELETE_ME.png', "wb").write(requests.get(img).content)
            img = "DELETE_ME.png"
        print(rainbow_text("Passing the ⚽ to my friend instabot"))
        print("please check out their repo: https://github.com/instagrambot/instabot/tree/master/instabot/api")
        bot = Bot()
        bot.login(username=self.username, password=os.environ.get('INSTAGRAM_PASSWORD'))
        bot.upload_photo(img, caption)
        bot.logout()
        self.login()
        os.system('rm DELETE_ME.png')

    def logout(self):
        if not(self.logged_in):
            return
        self.driver.get(f"https://www.instagram.com/{self.username}")
        self.driver.implicitly_wait(self.patience)

        avatar = self.driver.find_element_by_xpath(f"//img[@data-testid='user-avatar' and contains(@alt, '{self.username}')]")
        avatar.click()
        self.driver.implicitly_wait(self.patience)
        self.logged_in = False

        log_out = self.driver.find_element_by_xpath("//div[contains(text(), 'Log Out')]")  
        log_out.click()

    def search(self, query="a_the_rva", user=True, filter_=None):
        if not(user):
            if not(query.startswith('#')):
                query = '#'+query
        self.driver.get('http://instagram.com/')
        self.driver.implicitly_wait(self.patience)
        search_bar = self.driver.find_element_by_xpath("//input[@placeholder='Search']")
        
        mistakes = random.randint(1, min(4, len(query)))
        mistake_indices = random.sample([i for i in range(len(query))], mistakes)
        new_query = []
        mask = []

        j = 0
        for i in range(len(query)+mistakes):
            if i in mistake_indices:
                random_letter = random.sample(ascii_lowercase, 1)
                new_query.append(random_letter[0])
                j += 1
                mask.append(0)
            else:
                new_query.append(query[i-j])
                mask.append(1)

        for i, letter in enumerate(new_query):
            search_bar.send_keys(letter)
            time.sleep(0.01*random.randint(10,15))
            if mask[i] == 0:
                search_bar.send_keys(Keys.BACKSPACE)
                time.sleep(0.01*random.randint(10,15))
        search_bar.send_keys(Keys.ENTER)
        
        while True:
            try:
                first_result = self.driver.find_element_by_xpath("//input[@placeholder='Search']/../div/following-sibling::div/following-sibling::div/following-sibling::div//a")
                first_result.click()
                break
            except:
                time.sleep(0.5)
        self.driver.implicitly_wait(self.patience)
        time.sleep(1)

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
