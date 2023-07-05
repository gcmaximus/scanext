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
from multiprocessing import Pool
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import json

from functools import partial
from pathlib import Path

def initialize_headless(path_to_extension,jsonfile):
    # Getting the results from the json file
    def json_results(path,json_file):
        f = open(json_file)
        results = json.load(f)
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

    #differentiating data
    def diff_data(data):
        tainted = []
        other_vars = []
        scripts = []
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

    data, popup = json_results(path_to_extension,jsonfile)
    url_path, abs_path = get_ext_id(path_to_extension,popup)
    payloads = payloads('DYNAMIC_ANALYSIS/dynamic/payloads/small_payload.txt')

    # initialize selenium and load extension
    options = ChromeOptions()
    options.add_experimental_option('detach', True)
    load_ext_arg = "load-extension=" + abs_path
    options.add_argument(load_ext_arg)
    options.add_argument("--enable-logging")
    driver = Chrome(service=Service(), options=options)


    # case 1:
    # window_name(driver, url_path, payloads)

    # case 2:
    # location_href(driver, url_path, payloads)

    # context_menu(driver, url_path, payloads)

    



#####################
# Case Scenario gui #
#####################

# 1) Window_name Entry Point
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

# 1) onMessage 
def runtime_onM(extid, payload, ssm, msgvar):
    scripts = []
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

    return scripts

# 2) onConnect
def runtime_onC(extid, payload, ssm, msgvar):
    scripts = []
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
    return scripts

# 3) get cookies


# 4) location.hash
def location_hash(payload):
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

        print(script)
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

def main():
    # preconfiguration (set active to false)
    preconfigure('ad')

    # Run program
    with Display() as disp:
        print(disp.is_alive())
        initialize_headless('EXTENSIONS/h1-replacer(v3)contextMenu')

if __name__ == '__main__':
    main()

