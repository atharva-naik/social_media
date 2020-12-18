import colors
import dotenv
import selenium
import pandas as pd
# from .utils import *
from .models import *
import os, time, random
from colors import color
import tqdm, logging, calendar
from selenium import webdriver
from string import ascii_lowercase
from social_media.utils import smart_int
from datetime import datetime, timedelta
from dotenv import load_dotenv,find_dotenv
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options  
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, ElementClickInterceptedException


class GMailEngine(object):
    """
    The GMailEngine class contains all the methods necessary to perform basic user functions
    Data members
    current_user : name of the current user (in this case name of the person who owns the gmail account)
    patience : time waited implicitly for elements to load
    driver : the webdriver onject for using selinium
    List of member functions
    """
    def __init__(self, patience=5, maximize=True):
        super().__init__()
        # self.current_user = None
        load_dotenv(find_dotenv())
        self.patience = patience
        if self.patience <= 0:
            self.patience = 1        
        self.driver = webdriver.Chrome(ChromeDriverManager().install())         
        self.current_user=None
        self.email=None
        if maximize:
            self.driver.maximize_window()
        # self.driver.get('https://twitter.com/')
        # self.driver.implicitly_wait(self.patience)

    def login(self, email=None, password=None, read_from_env=True):
        if read_from_env:
            email = os.environ.get('GMAIL')
            password = os.environ.get('GMAIL_PASSWORD')

        if email is None:
            print("email id can't be None")
            return 
        if password is None:
            print("Password can't be None")
            return

        self.email = email
        self.driver.maximize_window()
        self.driver.get("https://stackoverflow.com/users/login")
        self.driver.implicitly_wait(self.patience) 
        
        sign_in = self.driver.find_element_by_xpath("//button[@data-provider='google']")
        sign_in.click()
        self.driver.implicitly_wait(self.patience)
        if "https://accounts.google.com/o/oauth2/auth/identifier" not in self.driver.current_url:
            self.login(email, password, read_from_env)

        uid_field = self.driver.find_element_by_xpath("//input[@type='email']")
        self.driver.implicitly_wait(self.patience)

        for letter in email:
            time.sleep(0.01*random.randint(3,20))
            uid_field.send_keys(letter)
        uid_field.send_keys(Keys.ENTER)
        
        self.driver.implicitly_wait(self.patience)
        time.sleep(4)

        password_field = self.driver.find_element_by_xpath("//input[@type='password']")
        self.driver.implicitly_wait(self.patience)
        # password_field.clear()
        for letter in password:
            time.sleep(0.01*random.randint(3,20))
            password_field.send_keys(letter)
        password_field.send_keys(Keys.ENTER)
        
        time.sleep(5)
        self.driver.get('https://gmail.com/')
        self.driver.implicitly_wait(self.patience)
        self.current_user = self.driver.find_element_by_xpath("//a[contains(@aria-label, 'Google Account')]").get_attribute('aria-label').split(':')[1].split('\n')[0].strip()

    def logout(self):
        self.driver.get("https://mail.google.com/mail/u/0/#inbox")
        self.driver.implicitly_wait(self.patience)
        
        account = self.driver.find_element_by_xpath("//a[contains(@aria-label, 'Google Account')]")
        account.click()
        sign_out = self.driver.find_element_by_xpath("//a[text()='Sign out']")
        sign_out.click()
        self.driver.implicitly_wait(self.patience)

    def search(self, query='drew is danny'):
        self.driver.get("https://mail.google.com/mail/u/0/#inbox")
        self.driver.implicitly_wait(self.patience)
        search_bar = self.driver.find_element_by_xpath("//input[@aria-label='Search mail']")
        
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

    def get_stats(self):
        self.driver.get("https://mail.google.com/mail/u/0/#inbox")
        self.driver.implicitly_wait(self.patience)
        primary = smart_int(self.driver.find_element_by_xpath("//head//title").get_attribute("innerHTML").split()[1][1:-1])

        self.driver.get("https://mail.google.com/mail/u/0/#drafts")
        self.driver.implicitly_wait(self.patience)
        drafts = smart_int(self.driver.find_element_by_xpath("//head//title").get_attribute("innerHTML").split()[1][1:-1])

        categories = {}
        self.driver.get("https://mail.google.com/mail/u/0/#category/social")
        self.driver.implicitly_wait(self.patience)
        categories['social'] = smart_int(self.driver.find_element_by_xpath("//head//title").get_attribute("innerHTML").split()[1][1:-1])

    def send_mail(self, body, to, subject):
        compose = self.driver.find_element_by_xpath("//div[text()='Compose']")
        compose.click()
        time.sleep(0.5*random.randint(1,4))
        
        to_field = self.driver.find_element_by_xpath("//textarea[@aria-label='To']")
        subject_field = self.driver.find_element_by_xpath("//input[@placeholder='Subject']")

        for letter in to:
            time.sleep(0.01*random.randint(5,20))
            to_field.send_keys(letter)

        for letter in subject:
            time.sleep(0.01*random.randint(5,20))
            subject_field.send_keys(letter)

        text_body = self.driver.find_element_by_xpath("//div[@aria-label='Message Body']")
        mistakes = random.randint(1,4)
        mistake_indices = random.sample([i for i in range(len(body))], mistakes)
        new_body = []
        mask = []

        j = 0
        for i in range(len(body)+mistakes):
            if i in mistake_indices:
                random_letter = random.sample(ascii_lowercase, 1)
                new_body.append(random_letter[0])
                j += 1
                mask.append(0)
            else:
                new_body.append(body[i-j])
                mask.append(1)

        for i, letter in enumerate(new_body):
            text_body.send_keys(letter)
            time.sleep(0.01*random.randint(10,15))
            if mask[i] == 0:
                text_body.send_keys(Keys.BACKSPACE)
                time.sleep(0.01*random.randint(10,15))
        
        time.sleep(1)
        text_body.send_keys(Keys.CONTROL+Keys.ENTER)
        self.driver.implicitly_wait(self.patience)

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

#1DK#2KK#1dk#2kk