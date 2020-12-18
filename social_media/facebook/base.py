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

class FacebookEngine(object):
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
        self.driver.maximize_window()
        self.driver.get("https://www.facebook.com/")
        self.driver.implicitly_wait(self.patience)
        time.sleep(1)

        uid = ''
        if read_from_env:
            email = os.environ.get('FACEBOOK_EMAIL')
            contact = os.environ.get('FACEBOOK_CONTACT')
            password = os.environ.get('FACEBOOK_PASSWORD')

        if email is None:
            if contact is None:
                print("contact number and email can't both be None")
            else:
                uid = contact
        else:
            uid = email

        uid_field = self.driver.find_element_by_xpath("//input[@data-testid='royal_email']")
        for letter in uid:
            time.sleep(0.01*random.randint(3,20))
            uid_field.send_keys(letter)

        password_field = self.driver.find_element_by_xpath("//input[@data-testid='royal_pass']")
        for letter in password:
            time.sleep(0.01*random.randint(3,20))
            password_field.send_keys(letter)
        password_field.send_keys(Keys.ENTER)
        self.driver.implicitly_wait(self.patience)
        time.sleep(2)

    def logout(self):
        account = self.driver.find_element_by_xpath("//div[@aria-label='Account']")
        account.click()
        time.sleep(1.5)

        log_out = self.driver.find_element_by_xpath("//span[text()='Log Out']")
        log_out.click()

    def search(self, query="atharva naik IIT"):
        search_bar = self.driver.find_element_by_xpath("//input[@type='search']")
        # clear the search bar like a human being
        for i in range(len(search_bar.get_attribute("value"))):
            search_bar.send_keys(Keys.BACKSPACE)
            time.sleep(0.01*random.randint(10,20))

        mistakes = random.randint(1,min(4, len(query)))
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
            time.sleep(0.01*random.randint(15,20))
        
            if mask[i] == 0:
                search_bar.send_keys(Keys.BACKSPACE)
                time.sleep(0.01*random.randint(15,20))
        
        search_bar.send_keys(Keys.ENTER)
        self.driver.implicitly_wait(self.patience)
        time.sleep(1)

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


        