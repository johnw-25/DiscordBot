import urllib
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup

class Dbd():
    def __init__(self):
        self.name = "Dead By Daylight"

    def get_patch_notes(self):
        # get the patch notes for dbd here, create file with ability to fetch data from specific url
        return -1 # placeholder