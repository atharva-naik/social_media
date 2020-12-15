from social_media.base import Engine
from social_media.simulation import RandomBehaviour

engine = Engine.select('hangouts')
rb = RandomBehaviour(engine)
engine.login(read_from_env=True)
rb.pause(10, silent=False)
rb.stay_on_page(duration=10)
rb.driver.get("https://icons8.com/icons/set/git-fork")
engine.close()
# engine.search('#depressed')
# engine.close()

# https://accounts.google.com/signin/v2/challenge/pwd?client_id=717762328687-iludtf96g1hinl76e4lc1b9a82g457nn.apps.googleusercontent.com&scope=profile%20email&redirect_uri=https%3A%2F%2Fstackauth.com%2Fauth%2Foauth2%2Fgoogle&state=%7B%22sid%22%3A1%2C%22st%22%3A%2259%3A3%3Abbc%2C16%3A3c60000c422334c4%2C10%3A1607940343%2C16%3A9339051b07c96fa3%2Ce4092560ed66dc7f4ec9bb1d15bcb14131b84c95ce8d3563f395ff420cebefc5%22%2C%22cdl%22%3Anull%2C%22cid%22%3A%22717762328687-iludtf96g1hinl76e4lc1b9a82g457nn.apps.googleusercontent.com%22%2C%22k%22%3A%22Google%22%2C%22ses%22%3A%224d3946016a514c3d92d40a0b3d2cd710%22%7D&response_type=code&flowName=GeneralOAuthFlow&cid=1&navigationDirection=forward&TL=AM3QAYbgMphag_gxeZoVjWhQtHZ6nPW8ET4wbPRJVUMlP1MFUXtX-H__hXxW3YPB