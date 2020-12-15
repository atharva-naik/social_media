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
    def __init__(self, patience=5):
        super().__init__()
        # self.current_user = None
        self.patience = patience
        self.current_user = None
        if self.patience <= 0:
            self.patience = 1     
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        self.driver = webdriver.Chrome( ChromeDriverManager().install(), chrome_options=chrome_options)      
        
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
        self.driver.get("https://hangouts.google.com/")
        # self.driver.implicitly_wait(self.patience) 

        # sign_in = self.driver.find_element_by_xpath("//a[contains(@href, 'accounts.google.com/ServiceLogin?')]")
        # sign_in.click()

    def logout(self):
        if self.driver.current_url != "https://hangouts.google.com/":
            self.driver.get("https://hangouts.google.com/")
        sing_out_optns = self.driver.find_element_by_xpath("//a[contains(@href, 'accounts.google.com/SignOutOptions?')]")
        sing_out_optns.click()
        
        time.sleep(0.01*random.randint(20, 50))
        sign_out = self.driver.find_element_by_xpath("//a[contains(@href, 'accounts.google.com/Logout?')]")
        sign_out.click()

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

# chrome_options.add_argument("--disable-extensions")   
# chrome_options.add_argument("--disable-popup-blocking")
# chrome_options.add_argument("--profile-directory=Default")
# chrome_options.add_argument("--ignore-certificate-errors")
# chrome_options.add_argument("--disable-plugins-discovery")
# chrome_options.add_argument("--disbale-web-security")
# chrome_options.add_argument("--user-data-dir")
# chrome_options.add_argument("--allow-running-insecure-content")
# chrome_options.add_argument("--incognito")