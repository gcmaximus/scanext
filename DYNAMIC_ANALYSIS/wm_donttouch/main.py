import json
import logging

def setup_logger(log_file):
    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Create a file handler and set the log level
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)

    # Create a formatter and add it to the handlers
    log_format = '%(message)s'
    formatter = logging.Formatter(log_format)
    file_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)

    return logger

logger = setup_logger('penetration_logv2_GUI.txt')


def payload_logging(outcome, source, extension_id, extension_name, url_of_website, payload_type, payload, time_of_injection, time_of_alert, payload_filename, packet_info):
    # Convert sets to lists
    payload = str(payload)
    # packet_info = str(packet_info)

    payload_log = {
        "outcome": outcome,
        "source": source,
        "extensionId": extension_id,
        "extensionName": extension_name,
        "Url": url_of_website,
        "payloadType": payload_type,
        "payload": payload,
        "timeOfInjection": time_of_injection,
        "timeOfAlert": time_of_alert,
        "payload_fileName": payload_filename,
        "packetInfo": packet_info
    }

    log_message = json.dumps(payload_log)
    logger.info(log_message)


import requests
server_info: list = requests.get("http://127.0.0.1:8000/data").json()["data"][0]

# server_info = json.loads(server_info)
# payload_normal_success = payload_logging("SUCCESS", "window.name", 'cjjdmmmccadnnnfjabpoboknknpiioge', 'h1-replacer(v3)', 'file:///test.html', 'normal','<img src=x onerror=alert("normal_success")>', '2023-07-09 16:30:20,956', '2023-07-09 16:30:21,55', 'shit_ass_payload_file.txt', 'nil')
# payload_normal_failure = payload_logging("FAILURE", "window.name", 'cjjdmmmccadnnnfjabpoboknknpiioge', 'h1-replacer(v3)', 'file:///test.html', 'normal','<img src=x onerror=alert("normal_failure")>', '2023-07-09 16:30:20,956', '2023-07-09 16:30:21,55', 'shit_ass_payload_file.txt', 'nil')
payload_server_success = payload_logging("SUCCESS", "window.name", 'cjjdmmmccadnnnfjabpoboknknpiioge', 'h1-replacer(v3)', 'file:///test.html', 'server','<img src=x onerror=alert("server_success")>', '2023-07-09 16:30:20,956', '2023-07-09 16:30:21,55', 'shit_ass_payload_file.txt', server_info)
# payload_server_failure = payload_logging(f"FAILURE", "window.name", 'cjjdmmmccadnnnfjabpoboknknpiioge', 'h1-replacer(v3)', 'file:///test.html', 'server','<img src=x onerror=alert("server_failure")>', '2023-07-09 16:30:20,956', '2023-07-09 16:30:21,55', 'shit_ass_payload_file.txt', 'nil')






# def payload_logging(outcome, source, extension_id, extension_name, url_of_website, payload, time_of_injection, time_of_alert, payload_filename):

#   if outcome == "SUCCESS":
#     logger.info(f"outcome: {outcome}, source: {source}, extensionId: {extension_id}, extensionName: {extension_name}, Url: {url_of_website}, payload: {payload}, timeOfInjection: {time_of_injection}, timeOfAlert: {time_of_alert}, payload_fileName: {payload_filename}")
#   elif outcome == "FAILURE":
#     logger.info(f"outcome: {outcome}, source: {source}, extensionId: {extension_id}, extensionName: {extension_name}, Url: {url_of_website}, payload: {payload}, timeOfInjection: {time_of_injection}, timeOfAlert: {time_of_alert}, payload_fileName: {payload_filename}")


# payload_logging("SUCCESS", "window.name", 'cjjdmmmccadnnnfjabpoboknknpiioge', 'h1-replacer(v3)', 'file:///test.html', '<img src=x onerror=alert("123")>', '2023-07-09 16:30:20,956', '2023-07-09 16:30:21,55', 'shit_ass_payload_file.txt')
# payload_logging("FAILURE", "window.name", 'cjjdmmmccadnnnfjabpoboknknpiioge', 'h1-replacer(v3)', 'file:///test.html', '<img src=x onerror=alert("123")>', '2023-07-09 16:30:20,956', '2023-07-09 16:30:21,55', 'shit_ass_payload_file.txt')




def interpreter(data):
    tainted = []
    other_vars = []
    for i in data:
        taint = {}
        taint_sink = i["extra"]["dataflow_trace"]["taint_sink"][1][1]
        taint_source = i["extra"]["dataflow_trace"]["taint_source"][1][1]
        metavars = {}
        lines = {}
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
        var = ""
        try:
            for j in i["extra"]["dataflow_trace"]["intermediate_vars"]:
                metavar.append(j["content"])
            try:
                if metavar[1]:
                    var = metavar[1]
            except:
                var = metavar[0]
            metavars["content"] = var
            other_vars.append(metavars)
        except:
            other_vars.append(metavars)


        # get lines
        line_start = i["extra"]["dataflow_trace"]["taint_source"][1][0]['start']['line']
        line_end = i["extra"]["dataflow_trace"]["taint_sink"][1][0]['end']['line']


            
        message = i["extra"]["message"]
        taint["message"] = message
        taint["source"] = taint_source
        taint["sink"] = taint_sink
        taint["line_start"] = line_start 
        taint["line_end"] = line_end 

        tainted.append(taint)

    return tainted 

def main(semgrep_scan_result_json):

    # use interpreter
    with open(semgrep_scan_result_json) as file:
        data = []
        scan_data = json.load(file)
        # index results
        scan_results = scan_data['results']
        for i in scan_results:
            data.append(i)

    interpretered_results = interpreter(data)


    # obtain source name
    for i in interpretered_results:
        split_by_semi = i['message'].split(';')[0]
        split_by_source = split_by_semi.split(':')
        source = split_by_source[1]

        match source:            
            case 'chrome_contextMenu_create':
                print('chrome_contextMenu_create')
            case 'chrome_contextMenu_onClicked_addListener':
                print('chrome_contextMenu_onClicked_addListener')
            case 'chrome_contextMenu_update':
                print('chrome_contextMenu_update')
            case 'chrome_cookies_get':
                print('chrome_cookies_get')
            case 'chrome_cookies_getAll':
                print('chrome_cookies_getAll')
            case 'chrome_debugger_getTargets':
                print('chrome_debugger_getTargets')
            case 'chrome_runtime_onConnect':
                print('chrome_runtime_onConnect')
            case 'chrome_runtime_onConnectExternal':
                print('chrome_runtime_onConnectExternal')
            case 'chrome_runtime_onMessage':
                print('chrome_runtime_onMessage')
            case 'chrome_runtime_onMessageExternal':
                print('chrome_runtime_onMessageExternal')
            case 'chrome_tabs_get':
                print('chrome_tabs_get')
            case 'chrome_tabs_getCurrent':
                print('chrome_tabs_getCurrent')
            case 'chrome_tabs_query':
                print('chrome_tabs_query')
            case 'location_hash':
                print('location_hash')
            case 'location_href':
                print('location_href')
            case 'location_search':
                print('location_search')
            case 'window_addEventListener_message':
                print('window_addEventListener_message')
            case 'window_name':
                print('window_name')
            case 'html-inputs-and-buttons':
                print('html-inputs-and-buttons')


# main('postMessageResultv2.json')