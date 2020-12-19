# example to download youtube playlists
from social_media.youtube.base import YouTubeEngine
y = YouTubeEngine()
y.login()
first_result = y.get_playlists('Mind Field')
first_result[0]
first_result[0].populate()
first_result[0].download()
y.logout()
y.close()
