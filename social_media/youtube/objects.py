import colors 
from colors import color

class YouTubeVideo(object):
    def __init__(self, url, title, duration, creator, upload_date, views, description, likes=None, dislikes=None, comments=None):
        self.url = url
        self.title = title
        self.duration = duration
        self.creator = creator
        self.upload_date = upload_date
        self.views = views
        self.description = description
        self.likes = likes
        self.dislikes = dislikes
        self.comments = comments

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

        return video

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
    def __init__(self, url, name, views, subscribers, join_date, isverified=False, videos=0, profile_pic=None, about=None):
        self.url=url
        self.name=name
        self.about=about
        self.views=views
        self.videos=videos
        self.join_date=join_date
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