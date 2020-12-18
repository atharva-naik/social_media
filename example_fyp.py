# example to fetch youtube playlists
import tqdm
from social_media.youtube.base import YouTubeEngine

y = YouTubeEngine()
y.login()
y.get_playlists()

# for plist in tqdm.tqdm(y.playlists):
#     plist.get_details()
#     print(plist)
y.playlists[3].populate()

# y.logout()
y.close()
