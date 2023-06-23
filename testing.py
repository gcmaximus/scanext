import json
import pprint
import time

f = open('s.json')

results = json.load(f)

data = []

for i in results["results"]:
    data.append(i)

tainted = []

for i in data:
    if "html-inputs-and-buttons" not in i["check_id"]:
        taint = {}
        taint_sink = i["extra"]["dataflow_trace"]["taint_sink"][1][1]
        taint_source = i["extra"]["dataflow_trace"]["taint_source"][1][1]
        message = i["extra"]["message"]
        print(f'Message: {message}')
        pprint.pprint(f'Source: {taint_source}')
        print(f'Sink: {taint_sink}')
        time.sleep(3)
        taint["message"] = message
        taint["source"] = taint_source
        taint["sink"] = taint_sink
        tainted.append(taint)

message = {}

def f(extid, payload, msgvar):


    script = f'chrome.runtime.sendMessage({extid},)'