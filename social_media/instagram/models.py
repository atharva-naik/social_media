import os
import requests
import subprocess
from colors import color
from prettytable import PrettyTable
from social_media.utils import install_tiv

class InstagramProfile(object):
    def __init__(self, url, name, username, driver, patience, isverified=False, posts=None, followers=None, following=None, bio=None, profile_photo=None):
        super().__init__()  
        self.url=url
        self.name=name
        self.username=username
        self.isverified=isverified
        self.posts=posts
        self.followers=followers
        self.following=following
        self.bio=bio
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
        profile['profile photo']=self.profile_photo

        return profile

    def posts(self, limit=20):
        pass

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
    