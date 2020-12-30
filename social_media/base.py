import time
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

ENGINE_DICT = {'instagram': InstagramEngine,    
               'facebook' : FacebookEngine,
               'gmail'    : GMailEngine,
               'twitter'  : TwitterEngine}
ALLOWED_METHODS = {k:[] for k in ENGINE_DICT}
ALLOWED_ARGUMENTS = {k:{} for k in ENGINE_DICT}

for key in ENGINE_DICT:
    methods = ENGINE_DICT[key].__dict__
    for method in methods:
        if method not in ['__module__', '__dict__', '__doc__', '__weakref__']:
            ALLOWED_METHODS[key].append(method)
            ALLOWED_ARGUMENTS[key][method] = inspect.getfullargspec(methods[method]) # methods[method].__code__.co_varnames


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

class ChatEngine(object):
    """
    Class to switch between social media engines
    supported social media platforms are:
    facebook, hangouts, quora, twitter, youtube
    gmail is also supported
    """
    def __init__(self, profile):
        self.bot=bot
        self.profile=profile

    def listen(self, duration=-1, rate=0.5):
        if duration == -1:
            while True:
                context = profile.get_messages()
                response = self.bot.respond(context)
                self.profile.message(response)
                time.sleep(duration)
        else:
            iters = int(duration/rate)+1
            for i in range(iters):
                context = profile.get_messages()
                response = self.bot.respond(context)
                self.profile.message(response)
                time.sleep(duration)

    def dump_chat(self):
        pass
# class ScriptEngine(object):
#     """
#     Initialise the state of the interpreter
#     """
#     def __init__(self, engine):
#         self.allowed_commands = inspect.getmembers(engine, predicate=inspect.ismethod)
#         self.platform = engine.type
#         self.instructions = []
#         # self.
#     """
#     Validate command (check whether it is a valid function call)
#     """
#     def add(self, command):
#         method, args = self.parse(command)
#         self.instructions.append((method, args))

#     def parse(self, command):
#         method, arg_str = command.split(':')
#         method, arg_str = method.strip(), arg_str.strip()
#         args = {}
#         for arg in arg_str.strip(','):
#             k,v = arg.split('=')
#             args[k]=v

#         return method, args
    
#     def execute_instr(self, command):
#         pass

#     def execute(self):
#         for instruction in self.instructions:
#             self.execute_instr(instruction[0], instruction[1])

#     def save(self, path):
#         pass

#     def read(self, path):
#         f = open(path, "r")
#         for line in f:
#             if line.startswith('#'):
#                 continue
