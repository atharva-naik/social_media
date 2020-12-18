import time
import tqdm
import colors
import pytube 
import random
import requests
import selenium
import prettytable
from colors import color
from pytube import YouTube
from string import ascii_lowercase
from prettytable import PrettyTable
from selenium.webdriver.common.keys import Keys
from social_media.utils import format_time, camel_case_split, smart_int

# def camel_case_split(str): 
#     words = [[str[0]]] 
  
#     for c in str[1:]: 
#         if (words[-1][-1].islower() and c.isupper()) or (words[-1][-1].islower() and c.isdigit()): 
#             words.append(list(c)) 
#         else: 
#             words[-1].append(c) 
  
#     return [''.join(word) for word in words] 

# def smart_int(string):
#     string = string.replace(",","").strip()
#     if 'K' in string:
#         string = float(string.replace("K",""))*1e+3
#     elif 'M' in string:
#         string = float(string.replace("M",""))*1e+6
#     elif 'B' in string:
#         string = float(string.replace("B",""))*1e+9

#     return int(string)

class VideoURLCantBeInferred(Exception):
    """
    Exception raised if video url can't be attained
    from the passed argument
    """    
    def __init__(self, passed_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.passed_type = passed_type

    def __str__(self):
        return color(f"url can't be extracted from a {self.passed_type} type object, it needs to be of str or YouTubeVideo type", fg="red", bg="#000")

class UserNotLoggedIn(Exception):
    """
    Exception raised if there is no engine for a particular 
    social media platform
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return color('user is not logged in !', fg="red", bg="#000")

class YouTubeVideo(object):
    def __init__(self, url, driver, patience, title, duration=None, creator=None, upload_date=None, views=None, description=None, likes=None, dislikes=None, thumbnail=None, comments=None):
        self.url=url
        self.title=title
        self.duration=duration
        self.creator=creator
        self.driver=driver
        self.patience=patience
        self.upload_date=upload_date
        self.views=views
        self.description=description
        self.likes=likes
        self.dislikes=dislikes
        self.comments=comments
        self.thumbnail=thumbnail
        self.liked=False
        self.disliked=False

    def to_dict(self):
        video={}

        video['url']=self.url
        video['title']=self.title
        video['duration']=self.duration
        video['creator']=self.creator
        video['upload date']=self.upload_date
        video['view count']=self.views
        video['likes']=self.likes
        video['dislikes']=self.dislikes
        video['description']=self.description
        video['comments']=self.comments
        video['thumbnail']=self.thumbnail

        return video

    # get all detials from the url
    def get_details(self, fetch_comments=False, limit=20):
        self.driver.get(self.url)
        self.driver.implicitly_wait(self.patience)
        self.description = self.driver.find_element_by_id("description").text
        self.thumbnail = self.driver.find_element_by_xpath("//link[@itemprop='thumbnailUrl']").get_attribute('href')
        self.upload_date = self.driver.find_element_by_xpath("//div[@id='date']").text[1:].strip()

        if not(self.title):
            self.title = self.driver.find_element_by_tag_name("h1")
        if not(self.creator):
            self.creator = self.driver.find_element_by_xpath("//div[@id='primary']//div[contains(@class, 'channel-name')]//a").get_attribute("innerHTML")
        if not(self.views):
            self.views = int(self.driver.find_element_by_xpath("//div[@id='primary']//span[contains(text(), 'view')]").text.replace("view","").replace("s","").replace(",","").strip())
        
        dislike_btn = self.driver.find_element_by_xpath("//button[@id='button' and contains(@aria-label, 'dislike this')]")
        self.dislikes = int(dislike_btn.get_attribute('aria-label').replace(',', '').split('with')[-1].split()[0].strip())
        self.disliked = dislike_btn.get_attribute('aria-pressed')

        like_btn = self.driver.find_element_by_xpath("//button[@id='button' and contains(@aria-label, 'like this')]")
        self.likes = int(like_btn.get_attribute('aria-label').replace(',', '').split('with')[-1].split()[0].strip())        
        self.liked = like_btn.get_attribute('aria-pressed')

        scroll = 1000
        for i in range(7):
            try:
                self.comments = int(self.driver.find_element_by_xpath("//div[@id='primary']//yt-formatted-string[contains(text(), 'Comment')]").text.replace("Comment","").replace("s","").replace(",","").strip())
                break
            except:
                self.driver.execute_script(f"window.scrollTo(0, {scroll})")    
                scroll += 1300
        

        # if fetch_comments:
        #     self.get_comments(limit=limit)

    def download(self):
        YouTube(self.url).streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()

    def download_thumbnail(self, path='{}.jpg'):
        if path == '{}.jpg':
            path = path.format(self.url.split('?v=')[-1])
        if self.thumbnail:
            open(path, "wb").write(requests.get(self.thumbnail).content)
        else:
            try:
                url = f"https://i.ytimg.com/vi/{self.url.split('?v=')[-1]}/maxresdefault.jpg"
                open(path, "wb").write(requests.get(self.thumbnail).content)
            except:
                print(color("404: thumbnail url not found!", fg='red'))

    def get_comments(self, limit=20):
        if self.driver.current_url != self.url:
            self.driver.get(self.url)
            self.driver.implicitly_wait(self.patience)

    def like(self):
        if self.driver.current_url != self.url:
            self.driver.get(self.url)
            self.driver.implicitly_wait(self.patience)
        self.liked=True
        self.disliked=False

        like_btn = self.driver.find_element_by_xpath("//button[@id='button' and contains(@aria-label, 'like this')]")
        if like_btn.get_attribute('aria-pressed') == 'false':
            like_btn.click()
        self.likes = int(like_btn.get_attribute('aria-label').replace(',', '').split('with')[-1].split()[0].strip())

    def unlike(self):
        if self.driver.current_url != self.url:
            self.driver.get(self.url)
            self.driver.implicitly_wait(self.patience)
        self.liked=False

        like_btn = self.driver.find_element_by_xpath("//button[@id='button' and contains(@aria-label, 'like this')]")
        if like_btn.get_attribute('aria-pressed') == 'true':
            like_btn.click()
        self.likes = int(like_btn.get_attribute('aria-label').replace(',', '').split('with')[-1].split()[0].strip())

    def dislike(self):
        if self.driver.current_url != self.url:
            self.driver.get(self.url)
            self.driver.implicitly_wait(self.patience)
        self.liked=False
        self.disliked=True

        dislike_btn = self.driver.find_element_by_xpath("//button[@id='button' and contains(@aria-label, 'dislike this')]")
        if dislike_btn.get_attribute('aria-pressed') == 'false':
            dislike_btn.click()
        self.dislikes = int(dislike_btn.get_attribute('aria-label').replace(',', '').split('with')[-1].split()[0].strip())

    def undislike(self):
        if self.driver.current_url != self.url:
            self.driver.get(self.url)
            self.driver.implicitly_wait(self.patience)
        self.disliked=False

        dislike_btn = self.driver.find_element_by_xpath("//button[@id='button' and contains(@aria-label, 'dislike this')]")
        if dislike_btn.get_attribute('aria-pressed') == 'true':
            dislike_btn.click()
        self.dislikes = int(dislike_btn.get_attribute('aria-label').replace(',', '').split('with')[-1].split()[0].strip())

    def comment(self, text="Hello World!, repo: https://github.com/atharva-naik/social_media"):
        if self.driver.current_url != self.url:
            self.driver.get(self.url)
            self.driver.implicitly_wait(self.patience)
        time.sleep(3)
        self.driver.execute_script("window.scrollTo(0, 1000)")
        time.sleep(3)

        comment_area = self.driver.find_element_by_xpath("//yt-formatted-string[@id='simplebox-placeholder']")
        comment_area.click()
        time.sleep(1)
        comment_area = self.driver.find_element_by_xpath("//div[@contenteditable='true' and @aria-label='Add a public comment...']")
        
        mistakes = random.randint(1,4)
        mistake_indices = random.sample([i for i in range(len(text))], mistakes)
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
            comment_area.send_keys(letter)
            time.sleep(0.01*random.randint(10,15))
            if mask[i] == 0:
                comment_area.send_keys(Keys.BACKSPACE)
                time.sleep(0.01*random.randint(10,15))
        
        comment_btn = self.driver.find_element_by_xpath("//paper-button[@id='button' and @aria-label='Comment']")
        comment_btn.click()
        self.driver.implicitly_wait(self.patience)
        time.sleep(1)

    def __str__(self):
        op = f"{self.title}\n"
        op += color(f"{self.views} views", fg='grey')
        op += color(f" • {self.upload_date} ago\n", fg='grey')
        op += f"{self.creator}\n"
        op += f"{self.description}"

        return op

    def __repr__(self):
        return f"{self.title} by {self.creator}, uploaded {self.upload_date}, viewed by {self.views} people ..."

class YouTubeProfile(object):
    def __init__(self, url, name, driver, patience, views=None, subscribers=None, join_date=None, isverified=False, videos=0, profile_pic=None, about=None):
        self.url=url
        self.name=name
        self.about=about
        self.views=views
        self.driver=driver
        self.videos=videos
        self.patience=patience
        self.join_date=join_date
        # self.logged_in=logged_in
        self.isverified=isverified
        self.subscribers=subscribers
        self.profile_photo=profile_pic

    def to_dict(self):
        profile={}

        profile['url']=self.url
        profile['name']=self.name
        profile['about']=self.about
        profile['views']=self.views
        profile['videos']=self.videos
        profile['join date']=self.join_date
        profile['is verified']=self.isverified
        profile['profile photo']=self.profile_photo
        profile['subscriber count']=self.subscribers

        return profile

    def subscribe(self):
        if self.logged_in:
            pass
    
    def unsubscribe(self):
        if self.logged_in:
            pass

    def __str__(self):
        op = f"{self.name}"
        if self.isverified:
            op += f"  {color('✓', fg='blue')}"
        op += f"\n{self.subscribers} subscribers {self.videos} videos\n"
        op += "Description\n"
        op += f"{self.about}\n"
        op += f"Stats\n"
        op += f"Joined {self.join_date}\n"
        op += f"{self.views} views"

        return op

    def __repr__(self):
        return f"{self.name} joined on {self.join_date}, has {self.videos} videos, {self.views} and {self.subscribers} subscribers ..."


class YouTubePlaylist(object):
    def __init__(self, url, driver, title, patience, visibility=None, views=None, videos={}, last_updated=None, description=None, num_videos=0):
        self.url=url
        self.driver=driver
        self.patience=patience
        self.title=title
        self.visibility=visibility
        self.videos=videos
        self.views=views
        self.last_updated=last_updated
        self.description=description
        self.num_videos=num_videos

    def get_details(self):
        self.driver.get(self.url)
        self.driver.implicitly_wait(self.patience)
        
        stats = self.driver.find_element_by_xpath("//div[@id='stats']").text
        self.num_videos, self.views, self.last_updated = camel_case_split(stats)
        self.views = self.views.replace("s","").replace("view","").strip()
        self.num_videos = smart_int(self.num_videos.replace("video","").replace("s","").strip())
        self.visibility = self.driver.find_element_by_xpath("//div[@id='privacy-stats']").text
        
        for i in range(5):
            try:
                self.description = self.driver.find_element_by_xpath("//div[@id='description-form']").text
                break
            except:
                pass
        if self.views == 'No':
            self.views = 0
        else:
            self.views = smart_int(self.views)

    def scroll_playlist(self):
        # SCROLL_PAUSE_TIME = pause_time
        scroll_height = 10000
        while len(self.driver.find_elements_by_xpath("//yt-formatted-string[@id='index']")) < self.num_videos:
            self.driver.execute_script(f"window.scrollTo(0, {scroll_height});")
            scroll_height += 10000

    #NOTE: Doesn't work properly
    def populate(self):
        if not(self.visibility):
            self.get_details()
        self.driver.get(self.url)
        self.driver.implicitly_wait(self.patience)
        self.scroll_playlist()
        self.driver.implicitly_wait(self.patience)
        time.sleep(2)

        videos = self.driver.find_elements_by_xpath("//ytd-playlist-video-renderer")

        for i in tqdm.tqdm(range(self.num_videos)):
            url = videos[i].find_element_by_xpath(".//a[@id='thumbnail']").get_attribute('href')
            title = videos[i].find_element_by_xpath(".//span[@id='video-title']").text
            # creator = videos[i].find_element_by_xpath(".//a[contains(@href, '/user/')]").text
            # if title not in ['[Private video]', '[Deleted video]']:
            #     duration = format_time(videos[i].find_element_by_xpath(".//span[contains(text(), ':')]").text)
            # else:
            #     duration = None
            self.videos[title] = url

    def add(self, video):
        current_url = self.driver.current_url
        if str(type(video)) == "<class 'social_media.youtube.models.YouTubeVideo'>":
            url = video.url
        elif type(video) == str:
            url = video
        else:
            raise(VideoURLCantBeInferred)
        # the first video ever on YouTube: "Me at the zoo"
        self.driver.get(url)
        self.driver.implicitly_wait(self.patience)
        # time.sleep(1.3)

        save = self.driver.find_element_by_xpath("//button[@id='button' and @aria-label='Save to playlist']")
        save.click()
        self.driver.implicitly_wait(self.patience)
        # time.sleep(1)
        # savelist = self.driver.find_element_by_xpath("//ytd-add-to-playlist-renderer/..")
        # play_list = savelist.text.split('\n')[2:-1]
        playlist = self.driver.find_element_by_xpath(f"//ytd-add-to-playlist-renderer//yt-formatted-string[contains(text(), '{self.title}')]")
        playlist.click()
        self.driver.get(current_url)
        self.driver.implicitly_wait(self.patience)

    def __str__(self):
        op = PrettyTable()
        op.field_names = [f"{self.title}"]
        op.add_row([color(f"{self.num_videos} videos • {self.views} views • {self.last_updated}", fg="grey", style="bold")])
        if self.visibility:
            if self.visibility == 'Private':
                op.add_row([color("Private 🔒", fg="grey", style="bold")])
            elif self.visibility == 'Public':
                op.add_row([color("Public 🌍", fg="grey", style="bold")])
            else:
                op.add_row([color("Unlisted 🔗", fg="grey", style="bold")])
        op.add_row([f"{self.description}"])

        return op.get_string()

    def __repr__(self):
        op = f"{self.title} has "
        if self.num_videos:
            op += f"{len(self.num_videos)} videos and is "
        else:
            op += "? videos and is "
        if self.visibility:
            op += f"{self.visibility}"
        else:
            op += "? visibility"        
        
        return op
