import os
import time
import random
import hashlib
import requests
import subprocess
from colors import color
from string import ascii_lowercase
from prettytable import PrettyTable
from social_media.utils import install_tiv
from selenium.webdriver.common.keys import Keys

class InstagramProfile(object):
    def __init__(self, url, name, username, driver, patience, isverified=False, posts=None, followers=None, following=None, bio=None, link=None, profile_photo=None):
        super().__init__()  
        self.url=url
        self.name=name
        self.username=username
        self.isverified=isverified
        self.posts=posts
        self.followers=followers
        self.following=following
        self.bio=bio
        self.link=link
        self.profile_photo=profile_photo
        self.driver=driver
        self.patience=patience

    def to_dict(self):
        profile={}

        profile['url']=self.url
        profile['name']=self.name
        profile['username']=self.username
        profile['is verified']=self.isverified
        profile['posts']=self.posts
        profile['followers']=self.followers
        profile['following']=self.following
        profile['bio']=self.bio 
        profile['link']=self.link
        profile['profile photo']=self.profile_photo

        return profile

    def posts(self, limit=20):
        pass

    def follow(self):
        self.driver.get(self.url)
        self.driver.implicitly_wait(self.patience)
        time.sleep(1)
        
        try:
            follow = self.driver.find_element_by_xpath("//button[text()='Follow']")
            follow.click()
        except:
            return

    def unfollow(self):
        self.driver.get(self.url)
        self.driver.implicitly_wait(self.patience)
        time.sleep(1)

        try:
            following = self.driver.find_element_by_xpath("//span[@aria-label='Following']")
            following.click()
            self.driver.implicitly_wait(self.patience)
            
            while True:
                try:
                    unfollow = self.driver.find_element_by_xpath("//button[text()='Unfollow']")
                    unfollow.click()
                    break
                except:
                    time.sleep(0.5)
        except:
            return

    def mount(self):
        self.driver.get(self.url)
        self.driver.implicitly_wait(self.patience)
        time.sleep(1)

        message_btn = self.driver.find_element_by_xpath("//button[text()='Message']")
        message_btn.click()
        self.driver.implicitly_wait(self.patience)
        time.sleep(1)

    def get_messages(self, limit=10):
        chat_threads = self.driver.find_elements_by_xpath("//div[contains(text(), ':')]")
        messages = []
        
        for chat_thread in chat_threads:
            timestamp = chat_thread.text
            chat = chat_thread.find_element_by_xpath("./../../following-sibling::div")
            while ':' not in chat: 
                element = chat
                text = element.text
                messages.append(InstagramMessage(text=text, 
                                                element=element, 
                                                driver=self.driver,
                                                timestamp=timestamp, 
                                                patience=self.patience))
                chat = chat.find_element_by_xpath("./../../following-sibling::div")
            
        return messages

    def message(self, message="send bobs and vagene"):
        self.driver.find_element_by_xpath(f"//div[text()='{self.username}']")
        text_area = self.driver.find_element_by_xpath("//textarea[@placeholder='Message...']")
        mistakes = random.randint(1, min(4, len(message)))
        mistake_indices = random.sample([i for i in range(len(message))], mistakes)
        new_query = []
        mask = []

        j = 0
        for i in range(len(message)+mistakes):
            if i in mistake_indices:
                random_letter = random.sample(ascii_lowercase, 1)
                new_query.append(random_letter[0])
                j += 1
                mask.append(0)
            else:
                new_query.append(message[i-j])
                mask.append(1)

        for i, letter in enumerate(new_query):
            text_area.send_keys(letter)
            time.sleep(0.01*random.randint(7,20))
            if mask[i] == 0:
                text_area.send_keys(Keys.BACKSPACE)
                time.sleep(0.01*random.randint(7,20))
        text_area.send_keys(Keys.ENTER)

    def unmount(self):
        self.driver.get("https://www.instagram.com/")
        self.driver.implicitly_wait(self.patience)
        time.sleep(1)

    def download_image(self, path='{}.jpg'):
        if path == '{}.jpg':
            path = path.format(time.time())
        open(path, "wb").write(requests.get(self.profile_photo).content)

    def __str__(self):
        if self.profile_photo:
            open("DELETE.jpg", "wb").write(requests.get(self.profile_photo).content)
            try:
                subprocess.run(["tiv", "DELETE.jpg"])
            except NotADirectoryError:
                install_tiv()
            os.system("rm DELETE.jpg")

        op = PrettyTable()
        if self.isverified:
            op.field_names = [f"{self.username} ✓"]
        else:
            op.field_names = [f"{self.username}"]
        op.align[op.field_names[0]]="l"
        op.add_row([f"{self.posts} posts    {self.followers} followers    {self.following} following"])
        op.add_row([f"{self.name}"])
        op.add_row([f"{self.bio}"])
        
        return color(op, fg='#000', bg='#f0f0f0')

    def __repr__(self):
        return f"{self.username} ({self.name}) has {self.posts} posts, {self.followers} followers and {self.following} following ..."
    
class InstagramPost(object):
    def __init__(self, url, driver, patience, geo=None, geo_link=None, meta=None, by=None, timestamp=None, caption=None, images=[], likes=None, comments=None):
        self.url=url
        self.driver=driver
        self.patience=patience
        self.geo=geo
        self.geo_link=geo_link
        self.meta=meta
        self.by=by 
        self.timestamp=timestamp
        self.caption=caption
        self.images=images
        self.likes=likes
        self.comments=comments
    
    def to_dict(self):
        post={}
    
        post['url']=self.url
        post['geo']=self.geo
        post['geo link']=self.geo_link
        post['meta']=self.meta
        post['by']=self.by
        post['date']=self.timestamp
        post['caption']=self.caption
        post['images']=self.images
        post['likes']=self.likes
        post['comments']=self.comments

        return post

    def __str__(self):
        if self.images:
            open("DELETE.jpg", "wb").write(requests.get(self.images[0]).content)
            try:
                subprocess.run(["tiv", "DELETE.jpg"])
            except NotADirectoryError:
                install_tiv()
            os.system("rm DELETE.jpg")

        op = PrettyTable()
        op.field_names = [color(f"{self.by}", style='bold')]
        op.align[op.field_names[0]]="l"
        if self.geo:
            op.add_row([color(self.geo)])
        op.add_row(["❤️ 🗨 ✉"])
        op.add_row([color(f"{self.likes} likes", style='bold')])
        op.add_row([color(self.by, style='bold') + ' ' + color(f"{' '.join(self.caption.split()[1:])}") ])
        op.add_row([color(f"View all {self.comments} comments", fg='gray')])
        op.add_row([color(self.timestamp.strftime("%-d %B %Y, %-I:%-M %p"), fg='gray')])

        return op.get_string()

    def __repr__(self):
        return f"posted by {self.by} on {self.timestamp.strftime('%-d %B %Y, %-I:%-M %p')}, {self.likes} likes, {self.comments} comments"

    def comment(self, text='beep boop'):
        self.driver.get(url)
        self.driver.implicitly_wait(self.patience)
        time.sleep(2)

    def get_comments(self):
        self.driver.get(url)
        self.driver.implicitly_wait(self.patience)
        time.sleep(2)

    def like(self):
        self.driver.get(url)
        self.driver.implicitly_wait(self.patience)
        time.sleep(2)

        like_btn = self.driver.find_elements_by_tag_name("svg")[1]
        if like_btn.get_attribute('aria-label') == 'Like':
            like_btn.click()
        else:
            return


    def unlike(self):
        self.driver.get(url)
        self.driver.implicitly_wait(self.patience)
        time.sleep(2)

        like_btn = self.driver.find_elements_by_tag_name("svg")[1]
        if like_btn.get_attribute('aria-label') == 'Unlike':
            like_btn.click()
        else:
            return

    def download_images(self, path="{}"):
        if path == '{}':
            path = path.format(time.time())
        os.mkdir(path)
        for i, image in enumerate(self.images):
            open(path+'/'+f'{i+1}.jpg', "wb").write(requests.get(image).content)

class InstagramMessage(object):
    def __init__(self, text, element, driver, patience, timestamp, id=None):
        super().__init__()
        self.text=text
        self.driver=driver
        self.element=element
        self.patience=patience
        self.timestamp=timestamp
        self.id=hashlib.sha256((text.strip()+f'-{timestamp}').encode()).hexdigest()

    def equals(self, obj): 
        if isinstance(obj, InstagramMessage):
            return self.id == obj.id
        else:
            return False

    def filter(self, objects, inplace=False):
        if inplace:
            objects = list(filter(self.equals, objects)) 
        else:
            return list(filter(self.equals, objects))

    def like(self):
        self.element.click()
        self.driver.implicitly_wait(self.patience)
        
        dot_btn = self.element.find_element_by_xpath(".//button")
        dot_btn.click()
        self.driver.implicitly_wait(self.patience)
        
        try:
            like_btn = self.driver.find_element_by_xpath(".//button[text()='Like']")
            like_btn.click()
            self.driver.implicitly_wait(self.patience)
        except:
            pass

    def unlike(self):
        self.element.click()
        self.driver.implicitly_wait(self.patience)

        dot_btn = self.element.find_element_by_xpath(".//button")
        dot_btn.click()
        self.driver.implicitly_wait(self.patience)
        
        try:
            unlike_btn = self.driver.find_element_by_xpath(".//button[text()='Unlike']")
            unlike_btn.click()
            self.driver.implicitly_wait(self.patience)
        except:
            pass
    
    def reply(self, text="I'm a nice guy *kisses you in your sleep*"):
        self.element.click()
        self.driver.implicitly_wait(self.patience)
    # def reply(self, text):
    #     self.element.click()
