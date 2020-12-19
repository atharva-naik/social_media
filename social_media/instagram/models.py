import os
import time
import requests
import subprocess
from colors import color
from prettytable import PrettyTable
from social_media.utils import install_tiv

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
    def __init__(self, url, driver, patience, title=None, meta=None, by=None, timestamp=None, caption=None, images=[], likes=None, comments=None):
        self.url=url
        self.driver=driver
        self.patience=patience
        self.title=title
        self.meta=meta
        self.by=by 
        self.timestamp=timestamp
        self.caption=caption
        self.image=image
        self.likes=likes
        self.comments=comments
    
    def to_dict(self):
        post={}
    
        post['url']=self.url
        post['title']=self.title
        post['meta']=self.meta
        post['by']=self.by
        post['date']=self.timestamp
        post['caption']=self.caption
        post['image']=self.images
        post['likes']=self.likes
        post['comments']=self.comments

        return post

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