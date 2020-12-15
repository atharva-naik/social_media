import time 
import tqdm
import random
import numpy as np
from .base import Engine

def pause(duration, silent=True):
    if silent:
        time.sleep(duration)
    else:
        if duration > 1:
            if duration != int(duration):
                duration = int(duration)+1
            for i in tqdm.tqdm(range(duration)):
                time.sleep(1)
        else:
            duration = duration/5
            for i in tqdm.tqdm(range(5)):
                time.sleep(duration)

class RandomBehaviour(Engine):
    def __init__(self, engine):
        super(RandomBehaviour, self).__init__()
        self.engine = engine
        self.driver = engine.driver
    """
    pause 
    """
    def pause(self, duration, silent=True):
        pause(duration, silent)
    """
    Frequency is in times per minute
    """
    async def stay_on_page(self, duration=3, frequency=10, url=None):
        if url is None:
            url = self.driver.current_url
        start = time.time()
        time_period = 1/frequency
        iterations = int(duration/time_period)+1
        for i in range(iterations):
            if self.driver.current_url != url:
                self.driver.get(url)
            time.sleep(duration)

    def click_behaviour(self, duration):
        pass

class Human(object):
    def __init__(self):
        pass
    def build_pipeline(self):
        pass