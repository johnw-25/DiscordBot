from games import *
import asyncio, aiohttp, datetime, discord, json, os, time, sys
from pprint import pprint

class bootle_patch():
    # our own very patch bot :D

    def __init__(self):
        self.game_list = []
        self.add_games()

    def add_games(self):
        self.game_list.append(Dbd())