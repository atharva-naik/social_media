import colors
import selenium
import prettytable
import pandas as pd
# from .utils import *
# from .objects import *
import os, time, random
from colors import color
import tqdm, logging, calendar
from selenium import webdriver
from string import ascii_lowercase
from prettytable import PrettyTable
from datetime import datetime, timedelta
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options  
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, ElementClickInterceptedException

class YouTubeEngine(object):
    """
    The YouTubeEngine class contains all the methods necessary to perform basic user functions
    Data members
    current_user : username of the account used 
    patience : time waited implicitly for elements to load
    driver : the webdriver onject for using selinium
    List of member functions
    """
    def __init__(self, patience=5):
        super().__init__()
        self.patience = patience
        self.current_user = None
        if self.patience <= 0:
            self.patience = 1    
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)

    def login(self, email=None, contact=None, password=None, read_from_env=True):
        uid = ''
        if read_from_env:
            email = os.environ.get('HANGOUTS_EMAIL')
            contact = os.environ.get('HANGOUTS_CONTACT')
            password = os.environ.get('HANGOUTS_PASSWORD')

        if email is None:
            if contact is None:
                print("contact number and email can't both be None")
            else:
                uid = contact
        else:
            uid = email
        
        self.driver.maximize_window()
        self.driver.get("https://stackoverflow.com/users/login")
        self.driver.implicitly_wait(self.patience) 

        sign_in = self.driver.find_element_by_xpath("//button[@data-provider='google']")
        sign_in.click()
        self.driver.implicitly_wait(self.patience)
        if "https://accounts.google.com/o/oauth2/auth/identifier" not in self.driver.current_url:
            self.login(email, contact, password, read_from_env)

        uid_field = self.driver.find_element_by_xpath("//input[@type='email']")
        self.driver.implicitly_wait(self.patience)
        # uid_field.clear()
        for letter in uid:
            time.sleep(0.01*random.randint(3,20))
            uid_field.send_keys(letter)
        uid_field.send_keys(Keys.ENTER)
        
        self.driver.implicitly_wait(self.patience)
        time.sleep(5)

        password_field = self.driver.find_element_by_xpath("//input[@type='password']")
        self.driver.implicitly_wait(self.patience)
        # password_field.clear()
        for letter in password:
            time.sleep(0.01*random.randint(3,20))
            password_field.send_keys(letter)
        password_field.send_keys(Keys.ENTER)

        time.sleep(5)
        self.driver.get("https://youtube.com/")

    def logout(self):
        self.driver.get("https://youtube.com/")
        self.driver.implicitly_wait(self.patience)
        profile_pic = self.driver.find_element_by_xpath("//img[@id='img']")
        
        profile_pic.click()
        time.sleep(2)
        sign_out = self.driver.find_element_by_xpath("//a[@href='/logout']")
        sign_out.click()

    def search(self, query="greg", filter_=None):
        ALLOWED_FILTERS = {'upload date':['last hour', 'today', 'this week', 'this month', 'this year'],
        'type':['video', 'channel', 'playlist', 'movie', 'show'],
        'duration':['short', 'long'],}
        filters_table = PrettyTable()
        filters_table.field_names = list(ALLOWED_FILTERS.keys())
        filters_table.add_row([""])

        search_bar = self.driver.find_element_by_xpath("//input[@id='search']")
        mistakes = random.randint(1,4)
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
        if filter_ is not None:
            filter_btn = self.driver.find_element_by_xpath("//paper-button[@aria-label='Search filters']")
            filter_btn.click()
            
            if not isinstance(filter_, dict):
                print(f"filter_ argument is of type {type(filter_)}, it needs to be of dict type")
                return
            else:
                if filter_.keys() not in ALLOWED_FILTERS.keys():
                    print(f"filter needs to adhere to the following format: \n{filters_table}")
                else:
                    for key in filter_:
                        if filter_[key] not in ALLOWED_FILTERS[key]:
                            print(f"filter needs to adhere to the following format: \n{filters_table}")

    def get_videos(self):
        pass
    
    def close(self):
        while True:
            i = input("Please enter q to quit now!\n")
            if i == 'q':
                try:
                    self.logout()
                    time.sleep(5)
                except:
                    self.driver.quit()
                break