import os
import fileinput
import time
from selenium.webdriver import ActionChains, Chrome, ChromeOptions, Keys
from selenium.webdriver.common.by import By
from os import path
import hashlib
from selenium.webdriver.support.wait import WebDriverWait
from pyvirtualdisplay.display import Display
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
import logging
from multiprocessing import Pool, Process
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import json

from server import main as server
import requests

from functools import partial
from pathlib import Path

import logging

def initialise_headless(path_to_extension,jsonfile):
    # preconfiguration (set active to false)
    preconfigure(path_to_extension)

    # Getting the source list
    sourcelist = {
        "chrome_contextMenu_create":".",
        "chrome_contextMenu_onClicked_addListener":".",
        "chrome_contextMenu_update":".",
        "chrome_cookies_get":cookie_get,
        "chrome_cookies_getAll":".",
        "chrome_debugger_getTargets":".",
        "chrome_runtime_onConnect":runtime_onC,
        "chrome_runtime_onConnectExternal":".",
        "chrome_runtime_onMessage":runtime_onM,
        "chrome_runtime_onMessageExternal":".",
        "chrome_tabs_get":".",
        "chrome_tabs_getCurrent":".",
        "chrome_tabs_query":".",
        "location_hash":location_hash,
        "location_href":".",
        "location_search":".",
        "window_addEventListener_message":".",
        "window_name":".",
        "html-inputs-and-buttons":"."
    }
    
    # Getting the results from the json file
    def json_results(path,json_file):
        f = open(json_file)
        results = json.load(f)
        popup = ''
        data = []
        for i in results["results"]:
            data.append(i)
        for i in results["paths"]["scanned"]:
            if "popup.html" in i:
                if path in i:
                    i = i[path.__len__():]
                    if i[0] != "/":
                        popup = "/" + i
        
        return data, popup
    
    # obtain relevant extension information'
    def get_ext_id(path_to_extension, p):
        abs_path = path.abspath(path_to_extension)
        m = hashlib.sha256()
        m.update(abs_path.encode("utf-8"))
        ext_id = "".join([chr(int(i, base=16) + 97) for i in m.hexdigest()][:32])
        url_path = f"chrome-extension://{ext_id}" + p
        return url_path, abs_path
    
    # definind payloads
    def payloads(path_to_payload):
        payload_array = []
        try:
            with open(path_to_payload, 'r') as file:
                # Read the contents of the file
                for line in file:
                    payload_array.append(line)
        except FileNotFoundError:
            print("File not found.")
        except IOError:
            print("An error occurred while reading the file.")
        
        return payload_array

    localserver = Process(target=server)
    localserver.start()
    data, popup = json_results(path_to_extension,jsonfile)
    url_path, abs_path = get_ext_id(path_to_extension,popup)
    payload = payloads('DYNAMIC_ANALYSIS/dynamic/payloads/small_payload.txt')
    l = interpreter(data)        

    # initialize selenium and load extension
    options = ChromeOptions()
    options.add_experimental_option('detach', True)
    load_ext_arg = "load-extension=" + abs_path
    options.add_argument(load_ext_arg)
    options.add_argument("--enable-logging")
    driver = Chrome(service=Service(), options=options)

    for result in l:
        a = result["message"].split("Source:")
        b = a[1].split(";")
        c = sourcelist[b[0]]
        c(payload,result)

    # logging for server
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

    def payload_logging(outcome, source, extension_id, extension_name, url_of_website, payload_type, payload, time_of_injection, time_of_alert, payload_filename, packet_info):
        # Convert sets to lists
        payload = str(payload)
        # packet_info = str(packet_info)
        logger = setup_logger('penetration_logv2_GUI.txt')

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

    server_info: list = requests.get("http://127.0.0.1:8000/data").json()["data"][0]
    payload_server_success = payload_logging("SUCCESS", "window.name", 'cjjdmmmccadnnnfjabpoboknknpiioge', 'h1-replacer(v3)', 'file:///test.html', 'server','<img src=x onerror=alert("server_success")>', '2023-07-09 16:30:20,956', '2023-07-09 16:30:21,55', 'small-payloads.txt', server_info)

    

#####################
# Case Scenario gui #
#####################

# 1) window.name
def window_name(driver, url_path, payloads):

    # get www.example.com
    driver.get('https://www.example.com')
    # set handler for example.com
    example = driver.current_window_handle

    # get extension popup.html
    driver.switch_to.new_window('tab')
    extension = driver.current_window_handle
    driver.get(url_path)


    for payload in payloads:
        # since window.name is obtained from the website url, we will inject javascript to change the window.name
        driver.switch_to.window(extension)
        driver.refresh()
        driver.switch_to.window(example)

        print(payload)

        driver.execute_script(f'window.name = `{payload}`;')

        try:
            # wait 2 seconds to see if alert is detected
            WebDriverWait(driver, 2).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert.accept()
            print('+ Alert Detected +')
        except TimeoutException:
            print('= No alerts detected =')

# 2) Location_href
def location_href(driver, url_path, payloads):
    # get www.example.com
    driver.get('https://www.example.com')
    # set handler for example.com
    example = driver.current_window_handle

    # get extension popup.html
    driver.switch_to.new_window('tab')
    extension = driver.current_window_handle
    driver.get(url_path)

    for payload in payloads:
        # we can inject a script to change the location.href variable using query parameters
        driver.switch_to.window(extension)
        driver.refresh()
        driver.switch_to.window(example)

        # print(payload)


        try:
            # driver.execute_script(f"location.href = 'https://www.example.com/?p'{payload}")
            driver.execute_script(f"location.href = 'https://www.example.com/?p'{payload}")

            time.sleep(1)
            try:
                # wait 2 seconds to see if alert is detected
                WebDriverWait(driver, 2).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert.accept()
                print('+ Alert Detected +')
            except TimeoutException:
                print('= No alerts detected =')

        except:
            print('Payload failed')

# 3) Context_Menu
def context_menu(driver, url_path, payloads):
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys



    # get www.example.com
    driver.get('file:///home/yijing/chrome-ext-scanner/DYNAMIC_ANALYSIS/xss_website_creation/xss_website.html')

    
    # set handler for example.com
    example = driver.current_window_handle

    # get extension popup.html
    driver.switch_to.new_window('tab')
    extension = driver.current_window_handle
    driver.get(url_path)

    for payload in payloads:
        # driver.switch_to.window(extension)
        # driver.refresh()

        driver.switch_to.window(example)

        driver.execute_script(f'document.getElementById("h1_element").innerText = `{payload}`')

        # driver.execute_script(f'document.getElementById("h1_element").innerHTML = `{payload}`')

        target_element = driver.find_element(By.ID, 'h1_element')

        # Select the text using JavaScript
        driver.execute_script("window.getSelection().selectAllChildren(arguments[0]);", target_element)



        actions = ActionChains(driver)

        actions.context_click(target_element).perform()

        import keyboard
        keyboard.press('down')







        # # COPY THE CURRENT SELECTED TEXT AND PRINT IT TO TERMINAL#
        # # COPY THE CURRENT SELECTED TEXT AND PRINT IT TO TERMINAL#
        # # Get the selected text using JavaScript
        # selected_text = driver.execute_script("return window.getSelection().toString();")
        # import pyperclip
        # # Copy the selected text to the clipboard using pyperclip
        # pyperclip.copy(selected_text)
        # print(selected_text)
        # # COPY THE CURRENT SELECTED TEXT AND PRINT IT TO TERMINAL#
        # # COPY THE CURRENT SELECTED TEXT AND PRINT IT TO TERMINAL#


        input()

##########################
# Case Scenario headless #
##########################

# 1) runtime.onMessage 
def runtime_onM(payload, ssm):
    scripts = []
    for k in ssm:
        dots = '.'
        taintsink = k["sink"]
        
        obj = {}
        var = ""
        #source is here
        if dots in taintsink:
            sinklist = taintsink.split(dots)
            a = sinklist[-1]
            if ")" in a:
                b = a.find(")")
                sinklist[-1] = a[:b]
            obj = {sinklist[-1]:payload}
            obj = json.dumps(obj)
            var = f"obj = JSON.parse('{obj}');"
        else:
            var = f"obj = '{payload}';"

        script = f"{var}chrome.runtime.sendMessage(obj)"
        scripts.append(script)
    
    return scripts

# 2) runtime.onConnect
def runtime_onC(payload, ssm):
    scripts = []
    for i in payload:
        dots = '.'
        taintsink = ssm["sink"]
        taintsource = ssm["source"]
        obj = {}
        var = ""
        func = ""
        connect = ""
        try:
            if ssm["metavars"]["PORT"]:
                port = ssm["metavars"]["PORT"]
        except:
            port = ""
        try:
            if ssm["metavars"]["PORTPROPERTY"]:
                portproperty = ssm["metavars"]["PORTPROPERTY"]
        except:
            portproperty = ""
        try:
            if ssm["metavars"]["PORTPASSWORD"]:
                portpassword = ssm["metavars"]["PORTPASSWORD"]
        except:
            portpassword = ""
        if dots in taintsink:
            tsink = taintsink.split(dots)
            obj = {tsink[-1]:i}
            obj = json.dumps(obj)
        else:
            obj = {taintsource:i}
            obj = json.dumps(obj)

        if port!="" and portproperty!="" and portpassword!="":
            connect = {portproperty:portpassword}
            connect = json.dumps(connect)

        var = f"obj = JSON.parse('{obj}');"
        func = f".postMessage(obj)"

        script = f"{var}chrome.runtime.connect({connect}){func}"
        print(script)
        scripts.append(script)
    return scripts

# 3) cookies.get
def cookie_get(payload, ssm):
    scripts = []
    for i in payload:
        dots = '.'
        taintsource = ssm["source"]
        cookie = ""
        x = ""
        try:
            if ssm["metavars"]["COOKIE"]:
                cookie = ssm["metavars"]["COOKIE"]
            if ssm["metavars"]["X"]:
                x = ssm["metavars"]["X"]
            if ssm["metavars"]["Y"]:
                y = ssm["metavars"]["Y"]
            try:
                if ssm["metavars"]["yvalue"]:
                    yvalue = ssm["metavars"]["yvalue"]
            except:
                yvalue = ""
        except:
            y = ""
        
        obj = ""
        if cookie in taintsource and taintsource == x:
            if dots in x:
                var = x.split(dots)
                if var[1] == "name":
                    obj = f'{i}=value;'
                elif var[1] == "value":
                    obj = f'cookie={i};'                
        elif cookie in taintsource and taintsource == y:
            if dots in y:
                var = x.split(dots)
                if var[1] == "name":
                    obj = f'{i}=value;'
                elif var[1] == "value":
                    obj = f'cookie={i};'
        elif cookie in taintsource and taintsource == yvalue:
            if dots in yvalue:
                var = x.split(dots)
                if var[1] == "name":
                    obj = f'{i}=value;'
                elif var[1] == "value":
                    obj = f'cookie={i};'
        
        script = f'document.cookie = {obj} + document.cookie'
        scripts.append(script) 
    return scripts

# 4) location.hash
def location_hash(payload, ssm):
    script = f"window.location.hash = {payload}"
    return script



# running the driver
def headless_driver(driver, url_path, scripts):
    # get www.example.com
    driver.get('https://www.example.com')
    # set handler for example.com
    example = driver.current_window_handle

    # get extension popup.html
    driver.switch_to.new_window('tab')
    extension = driver.current_window_handle
    driver.get(url_path)
    driver.switch_to.window(example)

    for script in scripts:

        # print(script)
        driver.execute_script(script)

        driver.switch_to.window(extension)
        driver.refresh()
        driver.switch_to.window(example)

        try:
            # wait 2 seconds to see if alert is detected
            WebDriverWait(driver, 2).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert.accept()
            print('+ Alert Detected +')
        except TimeoutException:
            print('= No alerts detected =')
        
        driver.refresh()

#preconfiguration
def preconfigure(dir):
    # Specify the folder path containing the JavaScript files
    folder_path = dir
    a = ""

    for root, dirs, files in os.walk(folder_path):
        # Perform the find and replace operation on each JavaScript file in the folder
        for filename in files:
            if filename.endswith(".js"):
                file_path = os.path.join(root, filename)

                # Perform the find and replace operation
                with fileinput.FileInput(file_path, inplace=True,) as file:
                    for line in file:
                        # Replace "active: true" with "active: false"
                        if "active: !0" in line:
                            a = "active: !0"
                        elif "active: true" in line:
                            a = "active: true"
                        
                        line = line.replace(a, "active: false")
                        print(line, end="")

#interpreter
def interpreter(data):
    tainted = []
    for i in data:
        taint = {}
        taint_sink = i["extra"]["dataflow_trace"]["taint_sink"][1][1]
        taint_source = i["extra"]["dataflow_trace"]["taint_source"][1][1]
        metavars = {}
        try:
            if i["extra"]["metavars"]["$PORT"]:
                metavars["PORT"] = i["extra"]["metavars"]["$PORT"]["abstract_content"]
            try:
                if i["extra"]["metavars"]["$PORTPASSWORD"]:
                    metavars["PORTPASSWORD"] = i["extra"]["metavars"]["$PORTPASSWORD"]["abstract_content"]
                if i["extra"]["metavars"]["$PORTPROPERTY"]:
                    metavars["PORTPROPERTY"] = i["extra"]["metavars"]["$PORTPROPERTY"]["abstract_content"]
            except:
                print('no port property/password')
        except:
            print('no port')
        try:
            if i["extra"]["metavars"]["$COOKIE"]:
                metavars["COOKIE"] = i["extra"]["metavars"]["$COOKIE"]["abstract_content"]
            if i["extra"]["metavars"]["$DETAILS"]:
                metavars["DETAILS"] = i["extra"]["metavars"]["$DETAILS"]["abstract_content"]
            if i["extra"]["metavars"]["$FUNC"]:
                metavars["FUNC"] = i["extra"]["metavars"]["$FUNC"]["abstract_content"]
        except:
            print("no cookie/details/function")
        try:
            if i["extra"]["metavars"]["$X"]:
                metavars["X"] = i["extra"]["metavars"]["$X"]["abstract_content"]
            if i["extra"]["metavars"]["$W"]:
                metavars["W"] = i["extra"]["metavars"]["$W"]["abstract_content"]
        except:
            print("no x/w")
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
            taint["metavars"] = metavars
        except:
            taint["metavars"] = metavars
        # added this
        line_start = i["extra"]["dataflow_trace"]["taint_source"][1][0]['start']['line']
        line_end = i["extra"]["dataflow_trace"]["taint_sink"][1][0]['end']['line']
        # added this
        message = i["extra"]["message"]
        taint["message"] = message
        taint["source"] = taint_source
        taint["sink"] = taint_sink
        # added this
        taint["line_start"] = line_start 
        taint["line_end"] = line_end 
        # added this
        tainted.append(taint)
    return tainted

#main
def main(extension_path, semgrep_results_path):
    # Can remove when done this main integrated with whole main.py
    extension_path = 'EXTENSIONS/h1-replacer(v3)contextMenu'
    semgrep_results_path = 'e.json'
    # Run program
    with Display() as disp:
        print(disp.is_alive())

        initialise_headless(extension_path,semgrep_results_path)

if __name__ == '__main__':
    main('a','s')

