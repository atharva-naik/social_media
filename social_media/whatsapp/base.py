import colors
import selenium
import pandas as pd
from .utils import *
from .objects import *
import os, time, random
from colors import color
import tqdm, logging, calendar
from selenium import webdriver
from string import ascii_lowercase
from datetime import datetime, timedelta
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options  
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, ElementClickInterceptedException

class WhatsAppEngine(object):
    def __init__(self, patience=5):
        super().__init__()