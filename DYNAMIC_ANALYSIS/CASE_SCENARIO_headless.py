import json

with open("e.json") as f:
    results = json.load(f)

data = []
for i in results["results"]:
    data.append(i)

tainted = []
other_vars = []
scripts = []

def runtime_onC(extid, payload, ssm):
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
            if i["vars"]["OBJ"]:
                x = i["vars"]["OBJ"]
        except:
            x = i["vars"]["X"]
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

def runtime_onM(extid, payload, ssm):
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
        for i in k["vars"]["content"]:
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

def cookie_get(extid, payload, ssm):
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
            if i["vars"]["COOKIE"]:
                cookie = i["vars"]["COOKIE"]
            if i["vars"]["DETAILS"]:
                details = i["vars"]["DETAILS"]
            if i["vars"]["FUNC"]:
                function = i["vars"]["FUNC"]
        except:
            function = False
        try:
            if i["vars"]["X"]:
                x = i["vars"]["X"]
            if i["vars"]["W"]:
                w = i["vars"]["W"]
        except:
            w = False
        try:
            if i["vars"]["Y"]:
                y = i["vars"]["Y"]
            try:
                if i["vars"]["yvalue"]:
                    yvalue = i["vars"]["yvalue"]
            except:
                yvalue = False
        except:
            y = False
        
        if cookie in taintsource and taintsource == x:
            if dots in x:
                var = x.split(dots)
                if var[1] == "name":
                    obj = f'{payload}=value;'
                elif var[1] == "value":
                    obj = f'cookie={payload};'                
        elif cookie in taintsource and taintsource == y:
            if dots in y:
                var = x.split(dots)
                if var[1] == "name":
                    obj = f'{payload}=value;'
                elif var[1] == "value":
                    obj = f'cookie={payload};'
        elif cookie in taintsource and taintsource == yvalue:
            if dots in yvalue:
                var = x.split(dots)
                if var[1] == "name":
                    obj = f'{payload}=value;'
                elif var[1] == "value":
                    obj = f'cookie={payload};'
        
        script = f'document.cookie = {obj} + document.cookie'
        scripts.append(script)

def location_hash(payload):
    script = f"window.location.hash = {payload}"
    scripts.append(script)

def interpreter(data,sourcelist):
    for i in data:
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
        try:
            if i["extra"]["metavars"]["$OBJ"]:
                metavars["OBJ"] = i["extra"]["metavars"]["$OBJ"]["abstract_content"]
        except:
            print('no obj')
        metavar = []
        try:
            for j in i["extra"]["dataflow_trace"]["intermediate_vars"]:
                metavar.append(j["content"])
            metavars["content"] = metavar
            taint["vars"] = metavars
        except:
            taint["vars"] = metavars
        message = i["extra"]["message"]
        taint["message"] = message
        taint["source"] = taint_source
        taint["sink"] = taint_sink
        tainted.append(taint)
        
# runtime_onM("extid","<img src=x onerror=alert(1)>",tainted,other_vars)

# for i in scripts:
#     print(i)

sourcelist = {
    "chrome_contextMenu_create":"yeet",
    "chrome_contextMenu_onClicked_addListener":"yeet",
    "chrome_contextMenu_update":"yeet",
    "chrome_cookies_get":cookie_get,
    "chrome_cookies_getAll":"yeet",
    "chrome_debugger_getTargets":"yeet",
    "chrome_runtime_onConnect":runtime_onC,
    "chrome_runtime_onConnectExternal":"yeet",
    "chrome_runtime_onMessage":runtime_onM,
    "chrome_runtime_onMessageExternal":"yeet",
    "chrome_tabs_get":"yeet",
    "chrome_tabs_getCurrent":"yeet",
    "chrome_tabs_query":"yeet",
    "location_hash":location_hash,
    "location_href":"yeet",
    "location_search":"yeet",
    "window_addEventListener_message":"yeet",
    "window_name":"yeet",
    "html-inputs-and-buttons":"yeet"
}

b = "Source:chrome_runtime_onConnect;Sink:outerHTML"
c = b.split("Source:")
d = c[1].split(";")
e = d[0]
print(sourcelist)
for key,value in sourcelist.items():
    print(key)
match e:
    case e:
        a = sourcelist[e]
        print(a)

    