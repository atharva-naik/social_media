# social_media
A library for automating several social media actions, such as posting, login, notifications etc. for multiple  social media and scraping data from these social medias. API free (no official social media APIs used), front-end selinium based solutions only.
### Social media platforms supported
<img style="display: inline;" src="https://github.com/atharva-naik/social_media/blob/main/images/facebook.png?raw=true" width="50">
<img style="display: inline;" src="https://github.com/atharva-naik/social_media/blob/main/images/gmail.png?raw=true" width="50">
<img style="display: inline;" src="https://github.com/atharva-naik/social_media/blob/main/images/hangouts.png?raw=true" width="50">
<img style="display: inline;" src="https://github.com/atharva-naik/social_media/blob/main/images/instagram.jpg?raw=true" width="50">
<img style="display: inline;" src="https://github.com/atharva-naik/social_media/blob/main/images/quora.png?raw=true" width="50">
<img style="display: inline;" src="https://github.com/atharva-naik/social_media/blob/main/images/twitter.png?raw=true" width="50">
<img style="display: inline;" src="https://github.com/atharva-naik/social_media/blob/main/images/whatsapp.png?raw=true" width="50">
<img style="display: inline;" src="https://github.com/atharva-naik/social_media/blob/main/images/youtube.png?raw=true" width="50">

### Installation

Will be uploaded to PyPI soon. Some versions will be uploaded to TestPyPI

### Cool updates:
**20th Dec: YOU CAN NOW VIEW YOUR INSTAGRAM FEED ON THE TERMINAL NOW**
<img style="display: inline;" src="https://github.com/atharva-naik/social_media/blob/main/images/instagram_feed1.png?raw=true">
<img style="display: inline;" src="https://github.com/atharva-naik/social_media/blob/main/images/instagram_feed2.png?raw=true">
NOTE: (only tested for linux till now)

### Some random use cases
**USE CASE 1:**
Fetch profile of a twitter user

1. Create twitter engine
```python
from social_media.twitter.base import TwitterEngine
t = TwitterEngine(patience=10) # patience is in seconds
```
or 
```python
from social_media.base import Engine
t = Engine.select('twitter', patience=10)
```
2. Login (optional)
```python 
t.login(read_from_env=True) # read from a .env file
```
or
```python
t.login(username="username", email="email@domain.com", contact="123456789", password="password")
"""pass the username, contact, email and password manually. 
(at least one of username, email or contact number is needed)
password is required"""
```
3. Get the profile of the person
```python
t.get_profile(username="@dannygonzalez") # I am truly greg (@ is optional, not really needed, also username should be exact)
```
4. Logout (optional)
```python
t.logout() 
```
5. Close the browser window 
```python
t.close(wait_for_input=False) # if wait_for_input is true then script will wait for the user to enter q to terminate
```

**USE CASE 2:**
Download a yotube playlist ("Downloading VSauce's Mind Field series")

```python
# example to download youtube playlists
from social_media.youtube.base import YouTubeEngine
y = YouTubeEngine() # init the engine object
y.login() # login to youtube account, needed if you want to add the playlist to your library
first_result = y.get_playlists('Mind Field') # search for playlist and get the first result
# first_result[0].add_playlist() optional step, if you want to add the playlist to your library
first_result[0].populate() # load video objects for all the contents of the playlist (can be skipped)
first_result[0].download() # download all videos in the playlist (internally populates the playlist if it is not populated)
y.logout() # logout from your youtube account
y.close()
```