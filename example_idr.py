# to get instagram dms and reply to them
from social_media.instagram.base import InstagramEngine
i = InstagramEngine()
i.login()

profile = i.get_profile('a_the_rva', hard=True)
profile.mount()
messages = profile.get_messages()

for message in messages:
    message.reply("I love you!")