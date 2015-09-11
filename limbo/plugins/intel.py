"""!intel <Entity|WHsystem>{,<Entity|WHsystem>}* Generates reports on entities from killmail data pulled from https://zkillboard.com"""


from eveIntel.reportinterface import reportInterface

import re
from tabulate import tabulate

r = reportInterface()

def parse(msg):
    
    response = ""
    

    req = msg.split(",")

    reports=[]
    
    for i in range(min(5,len(req))):

        #getHomeReport() and getSolReport() are the same          
        reports.append(r.getHomeReport(req[i].strip()))

    for i in reports:
        response = response +i
    return response


    



def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"(?i)!intel (.*)", text)
    if not match:
        return

    searchterm = match[0]
    report =""
    report=parse(searchterm.encode("utf8"))
    notice="messing with some db stuff, reports might be skewed for the next few hrs\n"

    #notice="something with my kills table in the DB is fucked, this command temp disabled"
    notice=""
    return "```"+notice+report+"```"
