"""!wh <Wormhole Type>{,<Wormhole Type>}* return information on what type of space a WH leads to. NOTE: masses for connections to/from k space may be wrong"""

import re
import sqlite3
from eveIntel import sqlinterface
from tabulate import tabulate

#"Name", "Type", "From", "To", "Lifetime", "Mass/Jump", "Max mass +-10%"]
holes={"z647":["z647", "static", "C2", "C1", "16 hrs", "20Gg", "500Gg"],
       "p060":["p060", "static", "C4", "C1", "16 hrs", "20Gg", "500Gg"],
       "y790":["y790", "static", "C5", "C1", "16 hrs", "20Gg", "500Gg"],       
       "q317":["q317", "static", "C6", "C1", "16 hrs", "20Gg", "500Gg"],
       "h121":["h121", "wandering", "C1", "C1", "16 hrs", "20Gg", "500Gg"],
       "v301":["v301", "wandering", "C3", "C1", "16 hrs", "20Gg", "500Gg"],
       "z971":["z971", "wandering", "KSpace", "C1", "16 hrs", "20Gg", "100Gg"],

       "d382":["d382", "static", "C2", "C2", "16 hrs", "300Gg", "2000Gg"],
       "n766":["n766", "static", "C4", "C2", "16 hrs", "300Gg", "2000Gg"],
       "d364":["d364", "static", "C5", "C2", "16 hrs", "300Gg", "2000Gg"],
       "g024":["g024", "static", "C6", "C2", "16 hrs", "300Gg", "2000Gg"],
       "c125":["c125", "wandering", "C1", "C2", "16 hrs", "20Gg", "1000Gg"],
       "i182":["i182", "wandering", "C3", "C2", "16 hrs", "300Gg", "2000Gg"],
       "r943":["r943", "wandering", "KSpace", "C2", "16 hrs", "300Gg", "750Gg"],

       "o477":["o477", "static", "C2", "C3", "16 hrs", "300Gg", "2000Gg"],
       "c247":["c247", "static", "C4", "C3", "16 hrs", "300Gg", "2000Gg"],
       "m267":["m267", "static", "C5", "C3", "16 hrs", "300Gg", "1000Gg"],
       "l477":["l477", "static", "C6", "C3", "16 hrs", "300Gg", "2000Gg"],
       "o883":["o883", "wandering", "C1", "C3", "16 hrs", "20Gg", "1000Gg"],
       "n968":["n968", "wandering", "C3", "C3", "16 hrs", "300Gg", "2000Gg"],
       "x702":["x702", "wandering", "KSpace", "C3", "16 hrs", "300Gg", "1000Gg"],

       "y683":["y683", "static", "C2", "C4", "16 hrs", "300Gg", "2000Gg"],
       "x877":["x877", "static", "C4", "C4", "16 hrs", "300Gg", "2000Gg"],
       "e175":["e175", "static", "C5", "C4", "16 hrs", "300Gg", "2000Gg"],
       "z457":["z457", "static", "C6", "C4", "16 hrs", "300Gg", "2000Gg"],
       "m609":["m609", "wandering", "C1", "C4", "16 hrs", "20Gg", "1000Gg"],
       "t405":["t405", "wandering", "C3", "C4", "16 hrs", "300Gg", "2000Gg"],
       "o128":["o128", "wandering", "KSpace", "C4", "24 hrs", "300Gg", "1000Gg"],

       "n062":["n062", "static", "C2", "C5", "24 hrs", "300Gg", "3000Gg"],
       "h900":["h900", "static", "C4", "C5", "24 hrs", "300Gg", "3000Gg"],
       "h296":["h296", "static", "C5", "C5", "24 hrs", "1350Gg", "3000Gg"],
       "v911":["v911", "static", "C6", "C5", "24 hrs", "1350Gg", "3000Gg"],
       "l614":["l614", "wandering", "C1", "C5", "24 hrs", "20Gg", "1000Gg"],
       "n770":["n770", "wandering", "C3", "C5", "24 hrs", "300Gg", "3000Gg"],
       "m555":["m555", "wandering", "HS", "C5", "48 hrs", "300Gg", "3000Gg"],
       "n432":["n432", "wandering", "LS/NS", "C5", "48 hrs", "1350Gg", "3000Gg"],

       "r474":["r474", "static", "C2", "C6", "24 hrs", "300Gg", "3000Gg"],
       "u574":["u574", "static", "C4", "C6", "24 hrs", "300Gg", "3000Gg"],
       "v753":["v753", "static", "C5", "C6", "24 hrs", "1350Gg", "3000Gg"],
       "w237":["w237", "static", "C6", "C6", "24 hrs", "1350Gg", "3000Gg"],
       "s804":["s804", "wandering", "C1", "C6", "24 hrs", "300Gg", "1000Gg"],
       "a982":["a982", "wandering", "C3", "C6", "24 hrs", "300Gg", "3000Gg"],
       "b041":["b041", "wandering", "HS", "C6", "48 hrs", "300Gg", "5000Gg"],
       "u319":["u319", "wandering", "?", "C6", "48 hrs", "1350Gg", "3000Gg"],

       "n110":["n110", "static", "C1", "HS", "24 hrs", "20Gg", "1000Gg"],
       "b274":["b274", "static", "C2", "HS", "24 hrs", "300Gg", "2000Gg"],
       "d845":["d845", "static", "C3", "HS", "24 hrs", "300Gg", "5000Gg"],
       "d792":["d792", "wandering", "C5/C6", "HS", "24 hrs", "100Gg", "3000Gg"],
       "a641":["a641", "wandering", "HS", "HS", "16 hrs", "100Gg", "2000Gg"],
       "b449":["b449", "wandering", "HS", "HS", "16 hrs", "100Gg", "2000Gg"],
       "s047":["s047", "wandering", "?", "HS", "24 hrs", "300Gg", "3000Gg"],
       "b520":["b520", "wandering", "?", "HS", "24 hrs", "300Gg", "5000Gg"],

       "j244":["j244", "static", "C1", "LS", "24 hrs", "20Gg", "1000Gg"],
       "a239":["a239", "static", "C2", "LS", "24 hrs", "300Gg", "2000Gg"],
       "u210":["u210", "static", "C3", "LS", "24 hrs", "300Gg", "3000Gg"],
       "c140":["c140", "wandering", "C5/C6", "LS", "24 hrs", "1350Gg", "3000Gg"],
       "r051":["r051", "wandering", "HS", "LS", "16 hrs", "1000Gg", "3000Gg"],
       "n944":["n944", "wandering", "LS/NS", "LS", "24 hrs", "1350Gg", "3000Gg"],
       "n290":["n290", "wandering", "?", "LS", "24 hrs", "1350Gg", "3000Gg"],
       "c391":["c391", "wandering", "?", "LS", "24 hrs", "1800Gg", "5000Gg"],

       "z060":["z060", "static", "C1", "NS", "24 hrs", "20Gg", "1000Gg"],
       "e545":["e545", "static", "C2", "NS", "24 hrs", "300Gg", "2000Gg"],
       "k346":["k346", "static", "C3", "NS", "24 hrs", "300Gg", "3000Gg"],
       "z142":["z142", "wandering", "C5/C6", "NS", "24 hrs", "1350Gg", "3000Gg"],
       "v283":["v283", "wandering", "HS", "NS", "24 hrs", "1000Gg", "3000Gg"],
       "s199":["s199", "wandering", "NS", "NS", "24 hrs", "1350Gg", "3000Gg"],
       "c248":["c248", "wandering", "?", "NS", "24 hrs", "1800Gg", "5000Gg"],
       "k329":["k329", "wandering", "?", "NS", "24 hrs", "1800Gg", "5000Gg"],

       "k162":["k162", "EndPoint", "?", "?", "?", "?", "?"]
       }

def parse(msg):
    req = msg.split(",")


    head = ["Name", "Type", "From", "To", "Lifetime", "Mass/Jump", "Max mass +-10%"]
    blankRow = []
    for i in range(len(head)):
        blankRow.append("")
    response =[] #"I said this wasn't implemented yet"
    for i in req:
        hole = lookUpWH(i.strip().lower())
        if hole is not None:
            response.append(hole)
        else:
            temp = blankRow
            temp[0] = "WH:"
            temp[1]=str(i)
            temp[2]="invalid"
            response.append(temp)

    return "```"+tabulate(response, headers = head)+"```"


#sql = slqinterface.sqlConnection()
#sql.connect()

def on_message(msg, server):
    #print(msg)
    
    text = msg.get("text", "")
    match = re.findall(r"(?i)!wh (.*)", text)
    if not match:
        return

    searchterm = match[0]
    return parse(searchterm.encode("utf8"))



def lookUpWH(name):
    if name.lower() in holes.keys():
        return holes[name.lower()]
    return None



