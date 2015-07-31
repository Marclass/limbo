"""!status will respond with a msg indicating the bot is still alive and listening"""

import re
#import sqlite3
#from tabulate import tabulate
from random import random


def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"(?i)!status(.*)", text)
    if not match:
        return

    searchterm = match[0]
    rand = random()
    if(rand<.15):
        return "Shut up"
    return "I'm alive"
