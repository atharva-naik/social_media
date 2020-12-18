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

class YouTubeEngine(object):
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
        if self.patience <= 0:
            self.patience = 1    
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
        if maximize:
            self.driver.maximize_window()

    def __repr__(self):
        if self.logged_in:
            return f"YouTube engine with patience={self.patience}, user logged in ..."
        else:
            return f"YouTube engine with patience={self.patience}, user not logged in ..."

    def login(self, email=None, password=None, read_from_env=True):
        if self.logged_in:
            return
        if read_from_env:
            email = os.environ.get('YOUTUBE_EMAIL')
            password = os.environ.get('YOUTUBE_PASSWORD')

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
        self.driver.get("https://youtube.com/")
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

    def logout(self):
        if not(self.logged_in):
            return
        self.driver.get("https://youtube.com/")
        self.driver.implicitly_wait(self.patience)
        self.logged_in = False
        profile_pic = self.driver.find_element_by_xpath("//img[@id='img']")
        
        profile_pic.click()
        time.sleep(2)
        sign_out = self.driver.find_element_by_xpath("//a[@href='/logout']")
        sign_out.click()

    def search(self, query="greg", filter_=None):
        # ALLOWED_FILTERS = {'upload date':['last hour', 'today', 'this week', 'this month', 'this year'],
        # 'type':['video', 'channel', 'playlist', 'movie', 'show'],
        # 'duration':['short', 'long'],}
        # filters_table = PrettyTable()
        # filters_table.field_names = list(ALLOWED_FILTERS.keys())
        # filters_table.add_row([""])
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

    def get_videos(self, query=None, limit=20):
        if query:
            self.search(query=query)
            self.driver.implicitly_wait(self.patience)
        
        videos = self.driver.find_elements_by_xpath("//a[@id='video-title' and contains(@href, 'watch?v')]")
        descriptions = self.driver.find_elements_by_xpath("//yt-formatted-string[@id='description-text']")
        # upload_dates = self.driver.find_elements_by_xpath("//div[@id='metadata']//span[contains(text(), 'ago')]")
        # durations = self.driver.find_elements_by_xpath("//ytd-thumbnail-overlay-time-status-renderer")
        output = []

        for video, description in zip(videos, descriptions):
            url = video.get_attribute("href")
            title = video.get_attribute("title")
            # duration = format_time(duration.text)
            views = int(video.get_attribute("aria-label").strip().split()[-2].strip().replace(",",""))
            
            if 'ago' in video.get_attribute("aria-label"):
                creator = ' '.join(video.get_attribute("aria-label").strip().split(' by ')[1].strip().split('ago')[0].strip().split()[:-2])
                upload_date = ' '.join(video.get_attribute("aria-label").strip().split(' by ')[1].strip().split('ago')[0].strip().split()[-2:]) 
                duration = videos[1].get_attribute("aria-label").strip().split(' by ')[1].strip().split('ago')[0].strip().replace('PewDiePie','').strip()
            else:
                duration = 'Live'
                upload_date = 'Live'
                creator = video.get_attribute('aria-label').strip().split(' by ')[1].split()[:-2][0].strip()
            description = description.text
            # text = video.get_attribute("aria-label").replace(",","").strip()
            # template = "<TEXT> by <TEXT> <INT> <TEXT> ago <INT> <TEXT> <INT> <TEXT> <INT> views"
            # split_by_template(text, template)
            next_vid = YouTubeVideo(url=url,
                                    title=title,
                                    views=views,
                                    creator=creator,
                                    duration=duration,
                                    driver=self.driver,
                                    patience=self.patience,
                                    upload_date=upload_date,
                                    description=description)
            output.append(next_vid)

        return output

    def get_playlists(self):
        # the first video ever on YouTube: "Me at the zoo"
        self.driver.get("https://www.youtube.com/")
        self.driver.implicitly_wait(self.patience)
        time.sleep(1.3)

        self.driver.implicitly_wait(self.patience)
        more = self.driver.find_element_by_xpath("//yt-formatted-string[contains(text(), 'Show more')]")
        more.click()

        self.playlists = []
        playlists = self.driver.find_elements_by_xpath("//a[@id='endpoint' and contains(@href,  'playlist?')]")
        for i, playlist in enumerate(playlists):
            self.driver.execute_script("arguments[0].scrollIntoView();", playlist) 
            time.sleep(0.2)
            playlist = self.driver.find_elements_by_xpath("//a[@id='endpoint' and contains(@href,  'playlist?')]")[i]
            title = playlist.text
            url = playlist.get_attribute("href")
            self.playlists.append(YouTubePlaylist(url, self.driver, title, self.patience))

        return self.playlists

    """
    Playlist is generated with only one video, the first video ever on YouTube
    """
    def create_playlist(self, title='Dank Videos', privacy='Private'):
        # the first video ever on YouTube: "Me at the zoo"
        self.driver.get("https://www.youtube.com/watch?v=jNQXAC9IVRw")
        self.driver.implicitly_wait(self.patience)
        
        save = self.driver.find_element_by_xpath("//button[@id='button' and @aria-label='Save to playlist']")
        save.click()
        add = self.driver.find_element_by_xpath("//div[@id='content-icon']")
        add.click()
        self.driver.implicitly_wait(self.patience)
        time.sleep(1)

        name = self.driver.find_element_by_xpath("//iron-input[@slot='input' and @id='input-1']//input")
        mistakes = random.randint(1, min(4, len(title)))
        mistake_indices = random.sample([i for i in range(len(title))], mistakes)
        new_title = []
        mask = []

        j = 0
        for i in range(len(title)+mistakes):
            if i in mistake_indices:
                random_letter = random.sample(ascii_lowercase, 1)
                new_title.append(random_letter[0])
                j += 1
                mask.append(0)
            else:
                new_title.append(title[i-j])
                mask.append(1)

        for i, letter in enumerate(new_title):
            name.send_keys(letter)
            time.sleep(0.01*random.randint(10,15))
            if mask[i] == 0:
                name.send_keys(Keys.BACKSPACE)
                time.sleep(0.01*random.randint(10,15))        

        dropdown = self.driver.find_elements_by_xpath("//iron-icon")[0]
        dropdown.click()
        time.sleep(1)

        btn = self.driver.find_elements_by_xpath("//ytd-privacy-dropdown-item-renderer")
        mode = {'public':0, 'unlisted':1, 'private':2}
        index = mode[privacy.lower()]
        btn[index].click()
        
        time.sleep(0.5)
        create = self.driver.find_element_by_xpath("//paper-button[@aria-label='Create']")
        create.click()

    def get_playlists(self):
        self.driver.get("https://www.youtube.com/")
        self.driver.implicitly_wait(self.patience)
        time.sleep(1.3)
        # menu_btn = self.driver.find_element_by_xpath("//button[@id='button' and @aria-label='Guide']")
        # menu_btn.click()
        self.driver.implicitly_wait(self.patience)
        more = self.driver.find_element_by_xpath("//yt-formatted-string[contains(text(), 'Show more')]")
        more.click()

        self.playlists = []
        playlists = self.driver.find_elements_by_xpath("//a[@id='endpoint' and contains(@href,  'playlist?')]")
        for i, playlist in enumerate(tqdm.tqdm(playlists)):
            self.driver.execute_script("arguments[0].scrollIntoView();", playlist) 
            time.sleep(0.2)
            playlist = self.driver.find_elements_by_xpath("//a[@id='endpoint' and contains(@href,  'playlist?')]")[i]
            title = playlist.text
            url = playlist.get_attribute("href")
            self.playlists.append(YouTubePlaylist(url, self.driver, title, self.patience))
        # time.sleep(1)
        return self.playlists

    def get_subscriptions(self):
        # the first video ever on YouTube: "Me at the zoo"
        self.driver.get("https://www.youtube.com/")
        self.driver.implicitly_wait(self.patience)
        time.sleep(1.3)

        self.driver.implicitly_wait(self.patience)
        more = self.driver.find_elements_by_xpath("//ytd-guide-section-renderer")[1].find_element_by_xpath(".//yt-formatted-string[contains(text(), 'more')]")
        more.click()

        self.subscriptions = []
        subscriptions = self.driver.find_elements_by_xpath("//a[@id='endpoint' and contains(@href,  '/channel/')]")[1:]
        for i, sub in enumerate(tqdm.tqdm(subscriptions)):
            self.driver.execute_script("arguments[0].scrollIntoView();", sub) 
            time.sleep(0.2)
            sub = self.driver.find_elements_by_xpath("//a[@id='endpoint' and contains(@href,  '/channel/')]")[1:][i]
            name = sub.text
            url = sub.get_attribute("href")
            self.subscriptions.append(YouTubeProfile(url, name, self.driver, self.patience))
        # time.sleep(1)
        return self.subscriptions

    # hard profile search, assumes that the profile supplied is an exact name
    def get_profile(self, query='kurtis town', hard=False):
        self.search(query)
        channel = self.driver.find_elements_by_xpath("//a[@id='main-link']")
        if len(channel)>0 and channel[0].text != '':
            link_from_search = channel[0].get_attribute('href')
            videos = channel[0].text.split('•')[1].split('\n')[0].strip()
            
            if hard == False:
                channel[0].click()
                self.driver.implicitly_wait(self.patience)
            else:
                query = query.replace(' ','').strip().lower()
                self.driver.get(f'https://www.youtube.com/user/{query}')
                
            self.driver.implicitly_wait(self.patience)
            time.sleep(2)
            page_title = self.driver.find_element_by_tag_name('title').get_attribute('innerHTML')
            if page_title == '404 Not Found':
                print("No proper channel results found")
                return
            elif "- YouTube" in page_title:
                name = page_title.replace("- YouTube", "").strip()
                if self.driver.current_url != link_from_search:
                    videos = 0
                url = self.driver.current_url
                self.driver.get(url+'/about')

                badge = self.driver.find_elements_by_xpath("//ytd-badge-supported-renderer//div[contains(@class, 'verified')]")
                about = self.driver.find_element_by_xpath("//yt-formatted-string[@id='description']").text
                temp = self.driver.find_element_by_xpath("//yt-formatted-string[text()='Stats']/following-sibling::yt-formatted-string")
                join_date = temp.text.replace("Joined", "").strip()
                views = temp.find_element_by_xpath("./following-sibling::yt-formatted-string").text.replace("views","").replace(",","").strip()

                subscribers = smart_int(self.driver.find_element_by_xpath("//yt-formatted-string[@id='subscriber-count']").text.replace("subscriber","").replace("s","").strip())
                profile_pic = self.driver.find_elements_by_xpath("//yt-img-shadow[@id='avatar']")[1].get_attribute('src')
                isverified = False
                if len(badge)>0:
                    isverified = True
            
            return YouTubeProfile(url=url,
                                name=name,
                                about=about,
                                views=views,
                                videos=videos,
                                driver=self.driver,
                                join_date=join_date,
                                isverified=isverified,
                                patience=self.patience,
                                subscribers=subscribers,
                                profile_pic=profile_pic)

        else:
            if hard == False:
                print("No proper channel results found")
                return
            # if sel

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
