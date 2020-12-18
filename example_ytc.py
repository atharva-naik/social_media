# to comment on a youtube video
from social_media.base import Engine

y = Engine.select("youtube")
y.login(read_from_env=True)
videos = y.get_videos("kurtis connor")
videos[0].comment("This comment was made by my python script :)")
y.close(wait_for_input=True)
