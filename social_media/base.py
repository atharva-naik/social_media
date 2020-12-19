import inspect
from social_media.gmail.models import *
from social_media.twitter.models import *
from social_media.youtube.models import *
from social_media.instagram.models import *
from social_media.facebook.base import FacebookEngine
from social_media.gmail.base import GMailEngine
from social_media.hangouts.base import HangoutsEngine
from social_media.quora.base import QuoraEngine
from social_media.twitter.base import TwitterEngine
from social_media.youtube.base import YouTubeEngine
from social_media.instagram.base import InstagramEngine

class PlatformNotSupported(Exception):
    """
    Exception raised if there is no engine for a particular 
    social media platform
    """
    def __init__(self, requested_platform, supported_platforms, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.req_platforms = requested_platform
        self.sup_platforms = supported_platforms

    def __str__(self):
        return f"{self.req_platforms} is not among supported platforms: {', '.join(list(self.sup_platforms))}"

class IllegalCommand(Exception):
    """
    Exception raised if there is no function corresponding 
    to the command requested in the platform engine
    """
    def __init__(self, command, engine, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.command = command
        self.platform = str(type(engine)).split('.')[-1][:-2]

    def __str__(self):
        return f"{self.command} is not a member function of {self.platform}"

class Engine(object):
    """
    Class to switch between social media engines
    supported social media platforms are:
    facebook, hangouts, quora, twitter, youtube
    gmail is also supported
    """
    def __init__(self, patience=5):
        super().__init__()
        self.patience = patience
        self.F = FacebookEngine
        self.G = GMailEngine
        self.H = HangoutsEngine
        self.Q = QuoraEngine
        self.T = TwitterEngine
        self.Y = YouTubeEngine
        self.supported = {'facebook':self.F,
        'gmail':self.G,
        'hangouts':self.H,
        'quora':self.Q,
        'twitter':self.T,
        'youtube':self.Y}

    @classmethod
    def select(cls, request, patience=5):
        cls.patience = patience
        cls.F = FacebookEngine
        cls.G = GMailEngine
        cls.H = HangoutsEngine
        cls.Q = QuoraEngine
        cls.T = TwitterEngine
        cls.Y = YouTubeEngine
        cls.supported = {'facebook':cls.F,
        'gmail':cls.G,
        'hangouts':cls.H,
        'quora':cls.Q,
        'twitter':cls.T,
        'youtube':cls.Y}
        
        if request in cls.supported:
            engine = cls.supported[request](patience=cls.patience)
            return engine
        else:
            raise(PlatformNotSupported(request, cls.supported.keys()))


class Script(object):
    def __init__(self, engine):
        self.allowed_commands = inspect.getmembers(engine, predicate=inspect.ismethod)

    def add(self, command):
        pass

    def execute(self):
        pass

    def save(self, path):
        pass

    def read(self, path):
        pass