import colors
import selenium
import pandas as pd
# from .utils import *
# from .objects import *
import os, time, random
from colors import color
import tqdm, logging, calendar
from selenium import webdriver
from string import ascii_lowercase
from datetime import datetime, timedelta
from dotenv import load_dotenv, find_dotenv
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options  
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, ElementClickInterceptedException

class HangoutsEngine(object):
    '''
    The HangoutsEngine class contains all the methods necessary to perform basic user functions
    Data members
    current_user : current user 
    patience : time waited implicitly for elements to load
    driver : the webdriver onject for using selinium
    List of member functions
    '''
    
    def __init__(self, patience=5, maximize=True):
        super().__init__()
        load_dotenv(find_dotenv())
        self.patience = patience
        self.logged_in = False
        if self.patience <= 0:
            self.patience = 1    
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
        if maximize:
            self.driver.maximize_window()

    def __repr__(self):
        if self.logged_in:
            return f"Hangouts engine with patience={self.patience}, user logged in ..."
        else:
            return f"Hangouts engine with patience={self.patience}, user not logged in ..."

    def login(self, email=None, password=None, read_from_env=True):
        if self.logged_in:
            return
        if read_from_env:
            email = os.environ.get('HANGOUTS_EMAIL')
            password = os.environ.get('HANGOUTS_PASSWORD')

        if email is None:
            print("email can't be None")
        if password is None:
            print("password can't be None")

        self.driver.get("https://stackoverflow.com/users/login")
        self.driver.implicitly_wait(self.patience) 

        sign_in = self.driver.find_element_by_xpath("//button[@data-provider='google']")
        sign_in.click()
        self.driver.implicitly_wait(self.patience)
        if "https://accounts.google.com/o/oauth2/auth/identifier" not in self.driver.current_url:
            self.login_direct(email, password, read_from_env)
            return

        uid_field = self.driver.find_element_by_xpath("//input[@type='email']")
        self.driver.implicitly_wait(self.patience)
        # uid_field.clear()
        for letter in email:
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

        time.sleep(3)
        self.logged_in = True
        self.driver.get("https://hangouts.google.com/")
        self.driver.implicitly_wait(self.patience)

    def login_direct(self, email=None, password=None, read_from_env=True):
        if self.logged_in:
            return
        if read_from_env:
            email = os.environ.get('YOUTUBE_EMAIL')
            password = os.environ.get('YOUTUBE_PASSWORD')

        if email is None:
            print("email can't be None")
        if password is None:
            print("password can't be None")

        self.driver.maximize_window()
        self.driver.get("https://accounts.google.com/login")

        uid_field = self.driver.find_element_by_xpath("//input[@type='email']")
        self.driver.implicitly_wait(self.patience)
        # uid_field.clear()
        for letter in email:
            time.sleep(0.01*random.randint(3,20))
            uid_field.send_keys(letter)
        uid_field.send_keys(Keys.ENTER)
        self.driver.implicitly_wait(self.patience)

        time.sleep(5)
        password_field = self.driver.find_element_by_xpath("//input[@type='password']")
        self.driver.implicitly_wait(self.patience)

        for letter in password:
            time.sleep(0.01*random.randint(3,20))
            password_field.send_keys(letter)
        password_field.send_keys(Keys.ENTER)
        time.sleep(3)
        
        self.logged_in = True
        self.driver.get("https://youtube.com/")
        self.driver.implicitly_wait(self.patience)    

    def get_chats(self):
        pass
    
    def get_conversations(self):
        pass 

    def get_contacts(self):
        pass

    def send_message(self):
        pass
    # def login(self, email=None, contact=None, password=None, read_from_env=True):
    #     uid = ''
    #     if read_from_env:
    #         email = os.environ.get('HANGOUTS_EMAIL')
    #         contact = os.environ.get('HANGOUTS_CONTACT')
    #         password = os.environ.get('HANGOUTS_PASSWORD')

    #     if email is None:
    #         if contact is None:
    #             print("contact number and email can't both be None")
    #         else:
    #             uid = contact
    #     else:
    #         uid = email
        
    #     self.driver.maximize_window()
    #     self.driver.get("https://stackoverflow.com/users/login")
    #     self.driver.implicitly_wait(self.patience) 

    #     sign_in = self.driver.find_element_by_xpath("//button[@data-provider='google']")
    #     sign_in.click()
    #     self.driver.implicitly_wait(self.patience)
    #     if "https://accounts.google.com/o/oauth2/auth/identifier" not in self.driver.current_url:
    #         self.login(email, contact, password, read_from_env)

    #     uid_field = self.driver.find_element_by_xpath("//input[@type='email']")
    #     self.driver.implicitly_wait(self.patience)
    #     # uid_field.clear()
    #     for letter in uid:
    #         time.sleep(0.01*random.randint(3,20))
    #         uid_field.send_keys(letter)
    #     uid_field.send_keys(Keys.ENTER)
        
    #     self.driver.implicitly_wait(self.patience)
    #     time.sleep(5)

    #     password_field = self.driver.find_element_by_xpath("//input[@type='password']")
    #     self.driver.implicitly_wait(self.patience)
    #     # password_field.clear()
    #     for letter in password:
    #         time.sleep(0.01*random.randint(3,20))
    #         password_field.send_keys(letter)
    #     password_field.send_keys(Keys.ENTER)

    #     time.sleep(5)
    #     self.driver.get("https://hangouts.google.com/")

    def logout(self):
        if self.driver.current_url != "https://hangouts.google.com/":
            self.driver.get("https://hangouts.google.com/")
        sing_out_optns = self.driver.find_element_by_xpath("//a[contains(@href, 'accounts.google.com/SignOutOptions?')]")
        sing_out_optns.click()
        
        time.sleep(0.01*random.randint(20, 50))
        sign_out = self.driver.find_element_by_xpath("//a[contains(@href, 'accounts.google.com/Logout?')]")
        sign_out.click()

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

# chrome_options.add_argument("--disable-extensions")   
# chrome_options.add_argument("--disable-popup-blocking")
# chrome_options.add_argument("--profile-directory=Default")
# chrome_options.add_argument("--ignore-certificate-errors")
# chrome_options.add_argument("--disable-plugins-discovery")
# chrome_options.add_argument("--disbale-web-security")
# chrome_options.add_argument("--user-data-dir")
# chrome_options.add_argument("--allow-running-insecure-content")
# chrome_options.add_argument("--incognito")