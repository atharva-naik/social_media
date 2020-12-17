import colors
import selenium
import prettytable
import pandas as pd
# from .utils import *
from .objects import *
from colors import color
import tqdm, logging, calendar
from selenium import webdriver
import os, re, time, random, copy
from string import ascii_lowercase
from prettytable import PrettyTable
from datetime import datetime, timedelta
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options  
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, ElementClickInterceptedException

# eg template: "<TEXT> by <TEXT> <INT> <TEXT> ago <INT> <TEXT> <INT> <TEXT> <INT> views"
def split_by_template(text, template):
    separators = template.replace("<TEXT>", "").replace("<INT>", "").strip().split()
    curr_txt = copy.deepcopy(text)
    curr_tmp = copy.deepcopy(template)
    res = []
    
    for separator in separators:
        txt = curr_txt.split(separator)[0].strip()
        tmp = curr_tmp.split(separator)[0].strip()

        integers = []
        for i in range(tmp.count('<INT>')):
            integers.append(int(re.findall(r"([0-9]+)", txt)[i].strip()))
        txt = re.sub(r"([0-9]+)", "<INT>", txt).strip().split("<INT>")
        texts = [item.strip() for item in txt if item is not '']
        
        int_ctr=0
        text_ctr=0
        for temp in tmp.split():
            if temp == '<TEXT>':
                res.append(texts[text_ctr])
                text_ctr += 1
            elif temp == '<INT>':
                res.append(integers[int_ctr])
                int_ctr += 1
        #         print(tmp)
        curr_txt = curr_txt.split(separator)[-1].strip()
        curr_tmp = curr_tmp.split(separator)[-1].strip()
    
    return res

def format_time(time_str):
    if time_str.count(':') == 1:
        time_str = '00:'+time_str
    return time_str

def smart_int(string):
    string = string.replace(",","").strip()
    if 'K' in string:
        string = float(string.replace("K",""))*1e+3
    elif 'M' in string:
        string = float(string.replace("M",""))*1e+6
    elif 'B' in string:
        string = float(string.replace("B",""))*1e+9

    return int(string)

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
        # ALLOWED_FILTERS = {'upload date':['last hour', 'today', 'this week', 'this month', 'this year'],
        # 'type':['video', 'channel', 'playlist', 'movie', 'show'],
        # 'duration':['short', 'long'],}
        # filters_table = PrettyTable()
        # filters_table.field_names = list(ALLOWED_FILTERS.keys())
        # filters_table.add_row([""])
        self.driver.get('https://youtube.com/')
        self.driver.implicitly_wait(self.patience)
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
                                    upload_date=upload_date,
                                    description=description)
            output.append(next_vid)

        return output

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
                                join_date=join_date,
                                isverified=isverified,
                                subscribers=subscribers,
                                profile_pic=profile_pic)

        else:
            if hard == False:
                print("No proper channel results found")
                return
            # if sel

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