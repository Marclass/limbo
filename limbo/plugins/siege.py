"""!siege generates a report on who is sieging who today/ yesterday"""

from eveIntel.reportinterface import reportInterface
import re
from tabulate import tabulate

r = reportInterface()


def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"(?i)!siege(.*)", text)
    if not match:
        return

    searchterm = match[0]
    report =""
    report=r.getSiegeReport()
    notice="messing with some db stuff, reports might be skewed for the next few hrs\n"

    #notice="something with my kills table in the DB is fucked, this command temp disabled"
    notice=""
    return "```"+notice+report+"```"
