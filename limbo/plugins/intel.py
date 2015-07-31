"""!intel <Entity|WHsystem>{,<Entity|WHsystem>}* Generates reports on entities from killmail data pulled from https://zkillboard.com"""

##from eveIntel.zkillinterface import zKillInterface
from eveIntel.dataprocessinginterface import dataProcessingInterface
##from eveIntel.sdeinterface import SDEInterface
##from eveIntel.evelinkinterface import evelinkinterface
import re
##from tabulate import tabulate

data = dataProcessingInterface()

def parse(msg):
    
    response = ""
    

    req = msg.split(",")

    reports=[]
    
    for i in range(min(5,len(req))):
        
        reports.append(data.genReport(req[i].strip()))

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

    
    notice=""
    return notice+report
