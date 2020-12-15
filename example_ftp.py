import pandas as pd
from social_media.base import Engine

t = Engine.select("twitter", patience=5)
# t.login(read_from_env=True)
queries = ['dannygonzalez', 'kurtis', 'testbot1797', 'drewisgooden', 'elonmusk', 'danny', 'philip', 'albert', 'michael']

profiles = []
for query in queries:
    profile = t.get_profile(query)
    profiles.append(profile.to_dict())
    print(profile)
profiles = pd.DataFrame(profiles)
profiles.to_csv("profiles.csv")

# t.logout()
t.close(wait_for_input=True)