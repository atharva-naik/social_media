import colors
import selenium
import prettytable
import pandas as pd
# from .utils import *
from .models import *
from colors import color
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
from social_media.utils import split_by_template, format_time, smart_int
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

    def get_profile(self):
        pass

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

    def search(self, query="a_the_rva", filter_=None):
        self.driver.get('https://youtube.com/')
        self.driver.implicitly_wait(self.patience)
        search_bar = self.driver.find_element_by_xpath("//input[@id='search']")
        
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
        
        self.driver.implicitly_wait(self.patience)
        time.sleep(1)
        # if filter_ is not None:
        #     filter_btn = self.driver.find_element_by_xpath("//paper-button[@aria-label='Search filters']")
        #     filter_btn.click()
            
        #     if not isinstance(filter_, dict):
        #         print(f"filter_ argument is of type {type(filter_)}, it needs to be of dict type")
        #         return
        #     else:
        #         if filter_.keys() not in ALLOWED_FILTERS.keys():
        #             print(f"filter needs to adhere to the following format: \n{filters_table}")
        #         else:
        #             for key in filter_:
        #                 if filter_[key] not in ALLOWED_FILTERS[key]:
        #                     print(f"filter needs to adhere to the following format: \n{filters_table}")
            


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
