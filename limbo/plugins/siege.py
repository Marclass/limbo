"""!siege generates a report on who is sieging who today/ yesterday"""

from eveIntel.dataprocessinginterface import dataProcessingInterface
import re
from tabulate import tabulate

data = dataProcessingInterface()


def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"(?i)!siege(.*)", text)
    if not match:
        return

    searchterm = match[0]
    report =""
    report=data.genSiegeReport()
    notice="messing with some db stuff, reports might be skewed for the next few hrs\n"

    #notice="something with my kills table in the DB is fucked, this command temp disabled"
    notice=""
    return "```"+notice+report+"```"
