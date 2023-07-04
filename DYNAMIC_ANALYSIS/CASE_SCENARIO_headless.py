import json

f = open('j.json')

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
            if msgvar[i][1]:
                x = msgvar[i][1]
        except:
            x = msgvar[i][0]
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
    for k in ssm:
        html = 'rHTML'
        dots = '.'
        underscore = '_'
        message = k["message"]
        if html in message:
            sink_split = message.split('Sink:')
            sink = sink_split[-1]
        elif dots in message:
            sink_split = message.split(dots)
            sink = sink_split[-1]
        elif underscore in message:
            sink_split = message.split(underscore)
            sink = sink_split[-1]
        
        taintsink = k["sink"]
        
        varindex = taintsink.find(sink+"(") + sink.__len__() + 1
        for i in msgvar[ssm.index(k)]["content"]:
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
                    obj = json.dumps(obj)
                    var = f"obj = JSON.parse('{obj}');"
                else:
                    var = f"obj = '{payload}';"
            else:
                endvarindex = taintsink.find(")",msgindex)
                if endvarindex == -1:
                    endvarindex = 0
                source = taintsink[msgindex:endvarindex]
                if dots in source:
                    sourcel = source.split(dots)
                    obj = {sourcel[1]:payload}
                    obj = json.dumps(obj)
                    var = f"obj = JSON.parse('{obj}');"
                else:
                    var = f"obj = '{payload}';"
        
        script = f"{var}chrome.runtime.sendMessage({extid},obj)"
        scripts.append(script)

def cookie_get(extid, payload, ssm, msgvar):
    for i in ssm:
        html = 'rHTML'
        dots = '.'
        underscore = '_'
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
            if msgvar[ssm.index(i)]["COOKIE"]:
                cookie = msgvar[ssm.index(i)]["COOKIE"]
            if msgvar[ssm.index(i)]["DETAILS"]:
                details = msgvar[ssm.index(i)]["DETAILS"]
            if msgvar[ssm.index(i)]["FUNC"]:
                function = msgvar[ssm.index(i)]["FUNC"]
        except:
            function = False
        try:
            if msgvar[ssm.index(i)]["X"]:
                x = msgvar[ssm.index(i)]["X"]
            if msgvar[ssm.index(i)]["W"]:
                w = msgvar[ssm.index(i)]["W"]
        except:
            w = False
        try:
            if msgvar[ssm.index(i)]["Y"]:
                y = msgvar[ssm.index(i)]["Y"]
            try:
                if msgvar[ssm.index(i)]["yvalue"]:
                    yvalue = msgvar[ssm.index(i)]["yvalue"]
            except:
                yvalue = False
        except:
            y = False
        
        if cookie in taintsource and taintsource == x:
            if dots in x:
                var = x.split(dots)
                obj = f''                
        elif cookie in taintsource and taintsource == y:
            y
        elif cookie in taintsource and taintsource == yvalue:
            yvalue
        
        script = f'document.cookie = {obj}'
        scripts.append(script)

def location_hash(payload):
    script = f"window.location.hash = {payload}"
    scripts.append(script)

for i in data:
    if "chrome_runtime_onMessage." in i["check_id"]:
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

    if "chrome_runtime_onConnect." in i["check_id"]:
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
        other_vars.append(metavars)
        message = i["extra"]["message"]
        taint["message"] = message
        taint["source"] = taint_source
        taint["sink"] = taint_sink
        tainted.append(taint)
    
    if 'chrome_cookies_get.' in i["check_id"]:
        taint = {}
        taint_sink = i["extra"]["dataflow_trace"]["taint_sink"][1][1]
        taint_source = i["extra"]["dataflow_trace"]["taint_source"][1][1]
        metavars = {}
        try:
            if i["extra"]["metavars"]["$COOKIE"]:
                metavars["COOKIE"] = i["extra"]["metavars"]["$COOKIE"]["abstract_content"]
            if i["extra"]["metavars"]["$DETAILS"]:
                metavars["DETAILS"] = i["extra"]["metavars"]["$DETAILS"]["abstract_content"]
            if i["extra"]["metavars"]["$FUNC"]:
                metavars["FUNC"] = i["extra"]["metavars"]["$FUNC"]["abstract_content"]
        except:
            print("no function")
        try:
            if i["extra"]["metavars"]["$X"]:
                metavars["X"] = i["extra"]["metavars"]["$X"]["abstract_content"]
            if i["extra"]["metavars"]["$W"]:
                metavars["W"] = i["extra"]["metavars"]["$W"]["abstract_content"]
        except:
            print("no w")
        try:
            if i["extra"]["metavars"]["$Y"]:
                metavars["Y"] = i["extra"]["metavars"]["$Y"]["abstract_content"]
            try:
                if i["extra"]["metavars"]["$Y"]["propagated_value"]:
                    metavars["yvalue"] = i["extra"]["metavars"]["$Y"]["propagated_value"]["svalue_abstract_content"]
            except:
                print("no y value")
        except:
            print("no y")
        
        other_vars.append(metavars)
        message = i["extra"]["message"]
        taint["message"] = message
        taint["source"] = taint_source
        taint["sink"] = taint_sink
        tainted.append(taint)

    if 'location_hash.' in i["check_id"]:
        location_hash()


# runtime_onM("extid","<img src=x onerror=alert(1)>",tainted,other_vars)

for i in scripts:
    print(i)