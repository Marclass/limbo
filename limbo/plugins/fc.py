"""!fc <corp|alliance>{,<corp|alliance>}* Generates a report on a corp or alliance that attempts to list pilots by threat/ leadership ability. FCs or pilots capable of FCing tend to rank highly in the report."""
from eveIntel.dataprocessinginterface import dataProcessingInterface
import re




data = dataProcessingInterface()


def parse(msg):
    
    response = ""
    

    req = msg.split(",")

    reports=[]
    
    for i in range(min(5,len(req))):
        
        reports.append(data.genLeadershipReport(req[i].strip()))

    for i in reports:
        response = response +i
    return response



def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"(?i)!fc (.*)", text)
    if not match:
        return

    searchterm = match[0]
    report =""
    report=parse(searchterm.encode("utf8"))
    notice="messing with some db stuff, reports might be skewed for the next few hrs\n"

    #notice="something with my kills table in the DB is fucked, this command temp disabled"
    notice=""
    return "```"+notice+report+"```"
