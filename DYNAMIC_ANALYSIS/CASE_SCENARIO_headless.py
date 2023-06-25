import json
import pprint
import time

f = open('s.json')

results = json.load(f)

data = []

for i in results["results"]:
    data.append(i)

print(data.__len__())

tainted = []
other_vars = []

for i in data:
    if "html-inputs-and-buttons" not in i["check_id"]:
        taint = {}
        taint_sink = i["extra"]["dataflow_trace"]["taint_sink"][1][1]
        taint_source = i["extra"]["dataflow_trace"]["taint_source"][1][1]
        metavars = []
        for j in i["extra"]["dataflow_trace"]["intermediate_vars"]:
            metavars.append(j["content"])
        other_vars.append({"content":metavars})
        message = i["extra"]["message"]
        # print(f'Message: {message}')
        # pprint.pprint(f'Source: {taint_source}')
        # print(f'Sink: {taint_sink}')
        # time.sleep(3)
        taint["message"] = message
        taint["source"] = taint_source
        taint["sink"] = taint_sink
        tainted.append(taint)

def f(extid, payload, ssm, msgvar):

    htmltag = '$('
    dots = '.'
    underscore = '_'
    message = ssm["message"]
    if dots in message:
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
            source = taintsink[varindex,endvarindex-1]
            if dots in source:
                sourcel = source.split(dots)
                obj = {sourcel[1]:payload}
            else:
                obj = {payload}
        else:
            endvarindex = taintsink.find(")",msgindex)
            source = taintsink[varindex,endvarindex-1]
            if dots in source:
                sourcel = source.split(dots)
                obj = {sourcel[1]:payload}
            else:
                obj = {payload}
    
    script = f'chrome.runtime.sendMessage({extid},{obj})'

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
