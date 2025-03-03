import zlib
import sys
import json
import os
import base64
import copy
InstructionDB = {
    "CONST":{
        "signal-A" : 1,
        "Opperand" : "constant",
    },
    "MEML":{
        "signal-A" : 2,
        "Opperand" : "var",
    },
    "MEMS":{
        "signal-A" : 3,
        "Opperand" : "var",
    },
    "SWAP":{
        "signal-A" : 4,
        "Opperand" : "none",
    },
    "SLP":{
        "signal-A" : 5,
        "Opperand" : "var",
    },
    "CALL":{
        "signal-A" : 6,
        "Opperand" : "func",
    },
    "RET":{
        "signal-A" : 7,
        "Opperand" : "none",
    },
    "REVSWAP":{
        "signal-A" : 8,
        "Opperand" : "none",
    },
    "CLRD":{
        "signal-A" : 9,
        "signal-O" : -2,
        "Opperand" : "predef",
    },
    "SETD":{
        "signal-A" : 9,
        "signal-O" : 2,
        "Opperand" : "predef",
    },
    "CLRU":{
        "signal-A" : 9,
        "signal-O" : -1,
        "Opperand" : "predef",
    },
    "SETU":{
        "signal-A" : 9,
        "signal-O" : 1,
        "Opperand" : "predef",
    },
    "MUL":{
        "signal-A" : 10,
        "Opperand" : "none",
    },
    "DIV":{
        "signal-A" : 11,
        "Opperand" : "none",
    },
    "MOD":{
        "signal-A" : 12,
        "Opperand" : "none",
    },
    "ADD":{
        "signal-A" : 13,
        "Opperand" : "none",
    },
    "SUB":{
        "signal-A" : 14,
        "Opperand" : "none",
    },
    "AND":{
        "signal-A" : 15,
        "Opperand" : "none",
    },
    "OR":{
        "signal-A" : 16,
        "Opperand" : "none",
    },
    "XOR":{
        "signal-A" : 17,
        "Opperand" : "none",
    },
    "POW":{
        "signal-A" : 18,
        "Opperand" : "none",
    },
    "CNVR":{
        "signal-A" : 19,
        "Opperand" : "none",
    },
    "JUMP":{
        "signal-A" : 20,
        "Opperand" : "jump",
    },
    "JMPE":{
        "signal-A" : 21,
        "Opperand" : "jump",
    },
    "JMPG":{
        "signal-A" : 22,
        "Opperand" : "jump",
    },
    "JMPL":{
        "signal-A" : 23,
        "Opperand" : "jump",
    },
    "JMPB":{
        "signal-A" : 24,
        "Opperand" : "jump",
    },
    "JMPU":{
        "signal-A" : 25,
        "Opperand" : "jump",
    },
    "JMPD":{
        "signal-A" : 26,
        "Opperand" : "jump",
    },
    "JMPQ":{
        "signal-A" : 27,
        "Opperand" : "jump",
    },
    "JMPO":{
        "signal-A" : 28,
        "Opperand" : "jump",
    },
    "ARRL":{
        "signal-A" : 30,
        "Opperand" : "none",
    },
    "ARRS":{
        "signal-A" : 31,
        "Opperand" : "none",
    },
    "ARRC":{
        "signal-A" : 32,
        "Opperand" : "none",
    },
    "ITSET":{
        "signal-A" : 33,
        "Opperand" : "none",
    },
    "ITNEXT":{
        "signal-A" : 34,
        "Opperand" : "none",
    },
    "PORTR":{
        "signal-A" : 40,
        "Opperand" : "var",
    },
    "PORTS":{
        "signal-A" : 41,
        "Opperand" : "var",
    },
    "ROBOC":{
        "signal-A" : 42,
        "Opperand" : "none",
    },
    "ROBOR":{
        "signal-A" : 43,
        "Opperand" : "none",
    },
    "NETS":{
        "signal-A" : 44,
        "Opperand" : "none",
    },
    "NETR":{
        "signal-A" : 45,
        "Opperand" : "none",
    },
    "DRAW":{
        "signal-A" : 46,
        "Opperand" : "none",
    },
    "CLRSCR":{
        "signal-A" : 47,
        "Opperand" : "none",
    },
    "HIGH":{
        "signal-A" : 50,
        "Opperand" : "none",
    },
    "LOW":{
        "signal-A" : 51,
        "Opperand" : "none",
    },
    "COUNT":{
        "signal-A" : 52,
        "Opperand" : "none",
    },
    "RAND":{
        "signal-A" : 53,
        "Opperand" : "none",
    },
    "STACK":{
        "signal-A" : 54,
        "Opperand" : "none",
    },
    "ROCKET":{
        "signal-A" : 55,
        "Opperand" : "none",
    },
    "QSET":{
        "signal-A" : 56,
        "Opperand" : "quality",
    },
    "QFILTER":{
        "signal-A" : 57,
        "Opperand" : "quality",
    },
}
qualitymap = {
"common": 1,
"uncommon": 2,
"rare": 3,
"epic": 4,
"legendary": 5
}
InstSkipLine = ["FUNC","LABEL","NOTE"]
functionLabels = {}
jumpLabels = {}
constants = {}
constantMode = True
Instructions = {}
starter_fillersignal = {
"index": 2,
"name": "iron-plate",
"quality": "normal",
"comparator": "=",
"count": 500
}
sample_electricpole = {
"entity_number": 5,
"name": "medium-electric-pole",
"position": {
    "x": -136.5,
    "y": -55.5
}
}
starter_constantcomb = ' {"entity_number": 2,"name": "constant-combinator","position": {"x": -119.5,"y": -54.5},"direction": 12,"control_behavior": {"sections": {"sections": [{"index": 1,"filters": [{"index": 1,"type": "virtual","name": "signal-A","quality": "normal","comparator": "=","count": 4}]}]}}}'
dict_constantcomb = json.loads(starter_constantcomb)
starter_decider = ' {"entity_number": 1,"name": "decider-combinator","position": {"x": -121,"y": -54.5},"direction": 12,"control_behavior": {"decider_conditions": {"conditions": [{"first_signal": {"type": "virtual","name": "signal-I"},"constant": 11,"comparator": "=","first_signal_networks": {"red": false,"green": true}}],"outputs": [{"signal": {"type": "virtual","name": "signal-everything"},"networks": {"red": true,"green": false}}]}}}'
dict_decider = json.loads(starter_decider)
starter_json = '{ "blueprint": {"icons": [{"signal": {"name": "constant-combinator"},"index": 1}],"entities": [],"wires": [],"item": "blueprint","version": 562949954928640}}'
blueprint = json.loads(starter_json)

def cleanupstring(line : str):
    newline = line.strip()
    newline = "".join(newline.split())

    return newline

def json_to_blueprint(json_data):
    compressed = zlib.compress(json.dumps(json_data).encode('utf-8'), level=9)
    return '0' + base64.b64encode(compressed).decode('utf-8')
linenum = 1
try:

    with open("./code.fac", "r") as f:

        lines = f.readlines()

        for line in lines:
            
            if constantMode:
                line = cleanupstring(line) 
                if line == ".code": #If they want to move out of constant mode
                    constantMode = False
                elif line.startswith(".name"):
                    newline = line[5:]
                    blueprint["blueprint"]["label"] = newline
                else:
                    newline2 = line.split("=")
                    constants[newline2[0]] = {}
                    key = newline2[0]

                    for kpair in newline2[1].split(","):
                        vkpair = kpair.split(":")
                        if len(vkpair) == 1:
                            raise Exception("\nInvalid Constant Decleration " + newline2[0] + " Cannot have null constant declaration")
                        vkpair[0] = vkpair[0].replace("_","-")
                        constants[key][vkpair[0]] = int(vkpair[1])
            else:
                #Setting up Labels and function handles
                line = line.strip()
                parts = line.split(" ")
                if parts[0] == "LABEL":
                    jumpLabels[parts[1]] = linenum
                if parts[0] == "FUNC":
                    functionLabels[parts[1]] = linenum
                if not parts[0] in InstSkipLine:
                    linenum = linenum + 1


        constantMode = True
        linenum = 1
        #Loop through the file again setting up the instruction dict to later be turned into JSON data
        for line in lines:
            if constantMode:
                line = cleanupstring(line) 
                if line == ".code": #If they want to move out of constant mode
                    constantMode = False
            else:
                line = line.strip()
                parts = line.split(" ")
                if not parts[0] in InstructionDB.keys():
                    if not parts[0] in InstSkipLine:
                        raise Exception("\nInvalid Command " + parts[0] + " Not Found ")
                if not parts[0] in InstSkipLine:
                    instData = InstructionDB[parts[0]]
                    if instData["Opperand"] == "constant":
                        constantAdd = constants[parts[1]]
                        Instructions[linenum] = {"signal-A":instData["signal-A"],**constantAdd}
                    elif instData["Opperand"] == "none":
                        Instructions[linenum] = {"signal-A":instData["signal-A"]}
                    elif instData["Opperand"] == "var":
                        Instructions[linenum] = {"signal-A":instData["signal-A"],"signal-O":parts[1]}
                    elif instData["Opperand"] == "quality":
                        qualitytest = parts[1].lower()
                        if not qualitytest in qualitymap:
                            raise Exception("\nInvalid Argument " + parts[1] + " Is not a Valid quality \nValid qualities are: common , uncommon , rare , epic , legendary ")   
                        Instructions[linenum] = {"signal-A":instData["signal-A"],"signal-O":qualitymap[qualitytest]}
                    elif instData["Opperand"] == "predef":   
                        Instructions[linenum] = {"signal-A":instData["signal-A"],"signal-O":instData["signal-O"]}
                    elif instData["Opperand"] == "jump":
                        if not parts[1] in jumpLabels:
                            raise Exception("\nInvalid Jump Command " + parts[1] + " Is not a defined Label ")   
                        Instructions[linenum] = {"signal-A":instData["signal-A"],"signal-O":jumpLabels[parts[1]]}
                    elif instData["Opperand"] == "func":   
                        if not parts[1] in functionLabels:
                            raise Exception("\nInvalid Call Command " + parts[1] + " Is not a defined Function ")   
                        Instructions[linenum] = {"signal-A":instData["signal-A"],"signal-O":functionLabels[parts[1]]}
                    linenum = linenum + 1

except Exception as e:

    print(e)

f.close()
#Now that ive grabbed all the data and setup my instruction dict let's get the JSON data and output file ready
entitynum = 1
DefaultX = -135
DefaultY = -59.5
for instructionNum, values in Instructions.items():
    new_decider = dict_decider
    new_decider["entity_number"] = entitynum
    new_decider["control_behavior"]["decider_conditions"]["conditions"][0]["constant"] = instructionNum
    new_decider["position"]["x"] = DefaultX - 1.5
    new_decider["position"]["y"] = DefaultY + (instructionNum - 1)
    blueprint["blueprint"]["entities"].append(copy.deepcopy(new_decider))

    entitynum = entitynum + 1

    new_constantcomb = dict_constantcomb
    new_constantcomb["entity_number"] = entitynum
    new_constantcomb["position"]["x"] = DefaultX
    new_constantcomb["position"]["y"] = DefaultY + (instructionNum - 1)
    new_constantcomb["control_behavior"]["sections"]["sections"][0]["filters"] = []
    signalIndex = 1
    for singalType , signalAmt in values.items():
        new_filtersignal = starter_fillersignal.copy()
        if singalType.startswith("signal"):
            new_filtersignal["type"] = "virtual"
        if singalType.endswith("biter") or singalType.endswith("spitter") or singalType.endswith("spawner") or singalType.endswith("pentapod") or singalType.endswith("worm-turret"):
            new_filtersignal["type"] = "entity"
        new_filtersignal["index"] = signalIndex
        new_filtersignal["name"] = singalType
        new_filtersignal["count"] = signalAmt
        new_constantcomb["control_behavior"]["sections"]["sections"][0]["filters"].append(new_filtersignal)
        signalIndex = signalIndex + 1
    blueprint["blueprint"]["entities"].append(copy.deepcopy(new_constantcomb))

    #TIME TO DO WIRES YIPPPIEIEEE 
    new_wires = []
    new_wires.append(entitynum - 1)
    new_wires.append(1)
    new_wires.append(entitynum)
    new_wires.append(1)
    blueprint["blueprint"]["wires"].append(copy.deepcopy(new_wires))
    if entitynum > 2:
        new_wires = []
        new_wires.append(entitynum - 3)
        new_wires.append(2)
        new_wires.append(entitynum - 1)
        new_wires.append(2)
        blueprint["blueprint"]["wires"].append(copy.deepcopy(new_wires))
        new_wires = []
        new_wires.append(entitynum - 3)
        new_wires.append(3)
        new_wires.append(entitynum - 1)
        new_wires.append(3)
        blueprint["blueprint"]["wires"].append(copy.deepcopy(new_wires))
        pass #CONNECTING THE COMBINATORS TOGETHER


    entitynum = entitynum + 1

sample_electricpole["entity_number"] = entitynum
sample_electricpole["position"]["y"] = DefaultY + (instructionNum + 3)
sample_electricpole["position"]["x"] = DefaultX - 3
blueprint["blueprint"]["entities"].append(sample_electricpole)
new_wires = []
new_wires.append(entitynum - 2)
new_wires.append(2)
new_wires.append(entitynum)
new_wires.append(2)
blueprint["blueprint"]["wires"].append(copy.deepcopy(new_wires))
new_wires = []
new_wires.append(entitynum - 2)
new_wires.append(3)
new_wires.append(entitynum)
new_wires.append(1)
blueprint["blueprint"]["description"] = "Factorio Cpu Code[virtual-signal=signal-green]\nMade by dragon1797"
blueprint["blueprint"]["wires"].append(copy.deepcopy(new_wires))
f = open("blueprint.txt","w")
f.write(json_to_blueprint(blueprint))
f.close()




