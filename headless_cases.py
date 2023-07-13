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

from functools import partial, reduce
from pathlib import Path

import subprocess

import logging
from datetime import datetime

# Logging framework
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
    logger = setup_logger('dynamic_logs.txt')

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

def initialise_headless(path_to_extension,results):
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
        "chrome_runtime_onConnectExternal":runtime_onCE,
        "chrome_runtime_onMessage":runtime_onM,
        "chrome_runtime_onMessageExternal":runtime_onME,
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
    
    # obtain relevant extension information'
    def get_ext_id(path_to_extension):
        abs_path = path.abspath(path_to_extension)
        m = hashlib.sha256()
        m.update(abs_path.encode("utf-8"))
        ext_id = "".join([chr(int(i, base=16) + 97) for i in m.hexdigest()][:32])
        url_path = f"chrome-extension://{ext_id}"
        return url_path, abs_path, ext_id
    
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
    url_path, abs_path, ext_id = get_ext_id(path_to_extension)
    payload = payloads('DYNAMIC_ANALYSIS/dynamic/payloads/small_payload.txt')
    l = interpreter(results)        

    # initialize selenium and load extension
    options = ChromeOptions()
    options.add_experimental_option('detach', True)
    load_ext_arg = "load-extension=" + abs_path
    options.add_argument(load_ext_arg)
    options.add_argument("--enable-logging")
    driver = Chrome(service=Service(), options=options)

    for result in l:
        source = result["message"].split(";")[0][7:]
        # sourcelist[source](driver,ext_id,url_path,payload,result)

    # server_info: list = requests.get("http://127.0.0.1:8000/data").json()["data"][0]
    # payload_server_success = payload_logging("SUCCESS", "window.name", 'cjjdmmmccadnnnfjabpoboknknpiioge', 'h1-replacer(v3)', 'file:///test.html', 'server','<img src=x onerror=alert("server_success")>', '2023-07-09 16:30:20,956', '2023-07-09 16:30:21,55', 'small-payloads.txt', server_info)


##########################
# Case Scenario headless #
##########################

# 1) runtime.onMessage 
def runtime_onM(driver, ext_id, url_path, payload, result):
    scripts = []
    for k in payload:
        dots = '.'
        taintsink = result["sink"]
        obj = {}
        var = ""
        if dots in taintsink:
            sinklist = taintsink.split(dots)
            a = sinklist[-1]
            if ")" in a:
                b = a.find(")")
                sinklist[-1] = a[:b]
            obj = {sinklist[-1]:k}
            obj = json.dumps(obj)
            var = f"obj = JSON.parse('{obj}');"
        else:
            var = f"obj = '{k}';"

        script = f"{var}chrome.runtime.sendMessage(obj)"
        scripts.append(script)
    
    return scripts

# 2) runtime.onConnect
def runtime_onC(driver, ext_id, url_path, payload, result):
    scripts = []
    for i in payload:
        dots = '.'
        taintsink = result["sink"]
        taintsource = result["source"]
        obj = {}
        var = ""
        func = ""
        connect = ""
        try:
            if result["metavars"]["PORT"]:
                port = result["metavars"]["PORT"]
        except:
            port = ""
        try:
            if result["metavars"]["PORTPROPERTY"]:
                portproperty = result["metavars"]["PORTPROPERTY"]
        except:
            portproperty = ""
        try:
            if result["metavars"]["PORTPASSWORD"]:
                portpassword = result["metavars"]["PORTPASSWORD"]
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
        scripts.append(script)
    return scripts

# 3) cookies.get && cookies.getAll
def cookie_get(driver, ext_id, url_path, payload, result):
    scripts = []
    for i in payload:
        dots = '.'
        taintsource = result["source"]
        cookie = ""
        x = ""
        try:
            if result["metavars"]["COOKIE"]:
                cookie = result["metavars"]["COOKIE"]
            if result["metavars"]["X"]:
                x = result["metavars"]["X"]
            if result["metavars"]["Y"]:
                y = result["metavars"]["Y"]
            try:
                if result["metavars"]["yvalue"]:
                    yvalue = result["metavars"]["yvalue"]
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
def location_hash(driver, ext_id, url_path, payload, result):
    script = f"window.location.hash = {payload}"
    return script

# 5) runtime.onMessageExternal
def runtime_onME(driver, ext_id, url_path, payload, result):
    scripts = []
    for i in payload:
        dots = '.'
        taintsink = result["sink"]
        obj = {}
        var = ""
        script = f"chrome.runtime.sendMessage('{ext_id}',)"
        scripts.append(script)

# 6) runtime.onConnectExternal
def runtime_onCE(driver, ext_id, url_path, payload, result):
    scripts = []
    for i in payload:
        dots = '.'
        taintsink = result["sink"]
        taintsource = result["source"]
        obj = {}
        var = ""
        func = ""
        connect = ""
        try:
            if result["metavars"]["PORT"]:
                port = result["metavars"]["PORT"]
        except:
            port = ""
        try:
            if result["metavars"]["PORTPROPERTY"]:
                portproperty = result["metavars"]["PORTPROPERTY"]
        except:
            portproperty = ""
        try:
            if result["metavars"]["PORTPASSWORD"]:
                portpassword = result["metavars"]["PORTPASSWORD"]
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

# 7) Window.name
def window_name_new(driver, ext_id, url_path, payloads, result):
    source = 'window.name'
    url_of_injection_example = 'https://www.example.com'
    url_of_injection_extension = url_path
    payload_file = 'small_payload.txt'

    try:
        # Navigate to example.com
        driver.get('https://www.example.com')
        example = driver.current_window_handle

        # Wait up to 5 seconds for the title to become "Example Domain"
        title_condition = EC.title_is('Example Domain')
        WebDriverWait(driver, 5).until(title_condition)

        # get page source code of example.com
        example_source_code = driver.page_source

        # get extension popup.html
        driver.switch_to.new_window('tab')
        driver.get(url_path)
        extension = driver.current_window_handle

        # get page source code of extension
        extension_source_code = driver.page_source


        for payload in payloads:
            # since window.name is obtained from the website url, we will inject javascript to change the window.name
            driver.switch_to.window(example)

            try:
                driver.execute_script(f'window.name = `{payload}`;')

                # get time of injection
                time_of_injection = datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")

            except Exception as e:
                print(' !!!! PAYLOAD FAILLED !!!!')
                print('Error: ', str(e))
                continue

            # check for alerts in example
            try:
                # wait 2 seconds to see if alert is detected
                WebDriverWait(driver, 2).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert.accept()
                print('[example] + Alert Detected +')

                # get time of success [1) example]
                time_of_success = datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")
                payload_logging("SUCCESS", source, ext_id, 'h1-replacer(v3)', url_of_injection_example, 'normal', payload, time_of_injection, time_of_success, payload_file, 'nil')
            
            except TimeoutException:
                print('[example] = No alerts detected =')
                payload_logging("FAILURE", source, ext_id, 'h1-replacer(v3)', url_of_injection_example, 'normal', payload, time_of_injection, 'nil', payload_file, 'nil')

                

            driver.switch_to.window(extension)
            driver.refresh()


            # check for alerts in extensions
            try:
                # wait 2 seconds to see if alert is detected
                WebDriverWait(driver, 2).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert.accept()

                print('[extension] + Alert Detected +')

                # get time of success [2) extension]
                time_of_success = datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")
                payload_logging("SUCCESS", source, ext_id, 'h1-replacer(v3)', url_of_injection_extension, 'normal', payload, time_of_injection, time_of_success, payload_file, 'nil')

            except TimeoutException:
                print('[extension] = No alerts detected =')
                payload_logging("FAILURE", source, ext_id, 'h1-replacer(v3)', url_of_injection_extension, 'normal', payload, time_of_injection, 'nil', payload_file, 'nil')


            driver.switch_to.window(example)

            # check for alerts in example
            try:
                # wait 2 seconds to see if alert is detected
                WebDriverWait(driver, 2).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert.accept()
                print('[example] + Alert Detected +')

                # get time of success [1) example]
                time_of_success = datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")
                payload_logging("SUCCESS", source, ext_id, 'h1-replacer(v3)', url_of_injection_example, 'normal', payload, time_of_injection, time_of_success, payload_file, 'nil')
            except TimeoutException:
                print('[example] = No alerts detected =')

                payload_logging("FAILURE", source, ext_id, 'h1-replacer(v3)', url_of_injection_example, 'normal', payload, time_of_injection, 'nil', payload_file, 'nil')

            try: 
                # check modifications for example.com
                driver.switch_to.window(example)
                if example_source_code != driver.page_source:
                    driver.get("https://www.example.com")
                    print("Navigated back to 'https://www.example.com' due to page source changes")

            except:
                print('error')

            try: 
                # check modifications for extension
                driver.switch_to.window(extension)
                if extension_source_code != driver.page_source:
                    driver.get(url_path)
                    print(f"Navigated back to '{url_path}' due to extension page source changes")

            except:
                print('error')

    except TimeoutException:
        # Handle TimeoutException when title condition is not met
        print("Timeout: Title was not resolved to 'Example Domain'")

    except Exception as e:
        # Handle any other exceptions that occur
        print("An error occurred:", str(e))

# 8) location.href
def location_href_new(driver, ext_id, url_path, payloads, result):
    try:
        # Navigate to example.com
        driver.get('https://www.example.com')
        # set handler for example.com
        example = driver.current_window_handle

        # Wait up to 5 seconds for the title to become "Example Domain"
        title_condition = EC.title_is('Example Domain')
        WebDriverWait(driver, 5).until(title_condition)

        # get page source code of example.com
        example_source_code = driver.page_source

        # get extension popup.html
        driver.switch_to.new_window('tab')
        extension = driver.current_window_handle
        driver.get(url_path)

        # get page source code of extension
        extension_source_code = driver.page_source
    
        # we can inject a script to change the location.href variable using query parameters or fragment Idenfiers
        for j in range(2):
            for payload in payloads:
                print(payload)
                driver.switch_to.window(extension)
                driver.refresh()
                driver.switch_to.window(example)

                if j == 0:
                    try:
                        driver.execute_script(f"location.href = `https://www.example.com/?p={payload}`")
                    except Exception as e:
                        print(' !!!! PAYLOAD FAILLED !!!!')
                        print('Error: ', str(e))
                        continue
                        
                else:
                    try:
                        driver.execute_script(f"location.href = `https://www.example.com/#{payload}`")
                    except Exception as e:
                        print(' !!!! PAYLOAD FAILLED !!!!')
                        print('Error: ', str(e))
                        continue

                # observe behavior after payload injection

                # 1) Check for alerts in example
                try:
                    # wait 2 seconds to see if alert is detected
                    WebDriverWait(driver, 2).until(EC.alert_is_present())
                    alert = driver.switch_to.alert
                    alert.accept()
                    print('[example] + Alert Detected +')
                except TimeoutException:
                    print('[example] = No alerts detected =')

                # 2) Check for alerts in extensions
                driver.switch_to.window(extension)
                try:
                    # wait 2 seconds to see if alert is detected
                    WebDriverWait(driver, 2).until(EC.alert_is_present())
                    alert = driver.switch_to.alert
                    alert.accept()
                    print('[extension] + Alert Detected +')
                except TimeoutException:
                    print('[extension] = No alerts detected =')

                
                # 3) Check for alerts in example after refreshing extension
                driver.refresh()
                driver.switch_to.window(example)

                try:
                    # wait 2 seconds to see if alert is detected
                    WebDriverWait(driver, 2).until(EC.alert_is_present())
                    alert = driver.switch_to.alert
                    alert.accept()
                    print('[example] + Alert Detected +')
                except TimeoutException:
                    print('[example] = No alerts detected =')


                try: 
                    # check modifications for example.com
                    driver.switch_to.window(example)
                    if example_source_code != driver.page_source:
                        driver.get("https://www.example.com")
                        print("Navigated back to 'https://www.example.com' due to page source changes")

                except:
                    print('error')


                try: 
                    # check modifications for extension
                    driver.switch_to.window(extension)
                    if extension_source_code != driver.page_source:
                        driver.get(url_path)
                        print(f"Navigated back to '{url_path}' due to extension page source changes")

                except:
                    print('error')

    except TimeoutException:
        # Handle TimeoutException when title condition is not met
        print("Timeout: Title was not resolved to 'Example Domain'")

    except Exception as e:
        # Handle any other exceptions that occur
        print("An error occurred:", str(e))

# 9) Context_menu'
def context_menu(driver, ext_id, url_path, payloads, result):
    from pynput.keyboard import Controller, Key
    import urllib.parse
    # entry points:
    # 1) Selection Text
    # 2) Link Url 
    # 3) Src Url
    # 4) frame Url
    # 5) Page Url

    # Selection Text 
    def context_menu_selectionText_new():
        website = "file:///home/showloser/dynamic/miscellaneous/xss_website.html"
        
        try:
            # get test xss website
            driver.get(website)
            # set handler for example.com
            example = driver.current_window_handle

            # Wait up to 5 seconds for the title to become "Xss Website"
            title_condition = EC.title_is('Xss Website')
            WebDriverWait(driver, 5).until(title_condition)

            # get page source code of example.com
            example_source_code = driver.page_source

            # get extension popup.html
            driver.switch_to.new_window('tab')
            extension = driver.current_window_handle
            driver.get(url_path)

            # get page source code of extension
            extension_source_code = driver.page_source


            for payload in payloads:
                
                # change to example tab
                driver.switch_to.window(example)

                try:
                    # using javascript, change the value of selectionText of predefined web element
                    driver.execute_script(f'document.getElementById("h1_element").innerText = `{payload}`')
                except Exception as e:
                    print(' !!!! PAYLOAD FAILLED !!!!')
                    print('Error: ', str(e))
                    continue

                # find h1_element to begin using extension
                target_element = driver.find_element(By.ID, 'h1_element')

                try:
                    # Select the text using JavaScript
                    driver.execute_script("window.getSelection().selectAllChildren(arguments[0]);", target_element)
                except Exception as e:
                    print(' !!!! Error Selecting Text !!!!')
                    print('Error: ', str(e))
                    continue

                
                # usage of context menu
                try:
                    # perform right click to open context menu
                    actions = ActionChains(driver)
                    actions.context_click(target_element).perform()

                    # navigate to extension context menu option
                    keyboard = Controller()
                    for _ in range(6):  
                        # Press the arrow key down
                        keyboard.press(Key.down)
                        # Release the arrow key
                        keyboard.release(Key.down)

                    # Press the Enter key
                    keyboard.press(Key.enter)
                    # Release the Enter key
                    keyboard.release(Key.enter)

                except Exception as e:
                    print(' !!!! Error using Context Menu !!!!')
                    print('Error: ', str(e))
                    continue

                
                # observe behavior after payload injection
                # 1) Check for alerts in example.com
                driver.switch_to.window(example)
                try:
                    # wait 2 seconds to see if alert is detected
                    WebDriverWait(driver, 2).until(EC.alert_is_present())
                    alert = driver.switch_to.alert
                    alert.accept()
                    print('+ Alert Detected +')
                except TimeoutException:
                    print('= No alerts detected =')
                        
                # 2) Check for alerts in extension
                driver.switch_to.window(extension)
                try:
                    # wait 2 seconds to see if alert is detected
                    WebDriverWait(driver, 2).until(EC.alert_is_present())
                    alert = driver.switch_to.alert
                    alert.accept()
                    print('[extension] + Alert Detected +')
                except TimeoutException:
                    print('[extension] = No alerts detected =')
                    
                # 3) Check for alerts in example after refreshing extension
                driver.refresh()
                driver.switch_to.window(example)
                try:
                    # wait 2 seconds to see if alert is detected
                    WebDriverWait(driver, 2).until(EC.alert_is_present())
                    alert = driver.switch_to.alert
                    alert.accept()
                    print('[example] + Alert Detected +')
                except TimeoutException:
                    print('[example] = No alerts detected =')


                # check for any modifications (snapshot back to original)
                try: 
                    # [1] check modifications for example.com
                    driver.switch_to.window(example)
                    if example_source_code != driver.page_source:
                        driver.get(website)
                        print(f"Navigated back to '{website}' due to page source changes")

                except:
                    print('error')


                try: 
                    # [2] check modifications for extension
                    driver.switch_to.window(extension)
                    if extension_source_code != driver.page_source:
                        driver.get(url_path)
                        print(f"Navigated back to '{url_path}' due to extension page source changes")

                except:
                    print('error')

        except TimeoutException:
            # Handle TimeoutException when title condition is not met
            print("Timeout: Title was not resolved to 'Example Domain'")

        except Exception as e:
            # Handle any other exceptions that occur
            print("An error occurred:", str(e))

    # Selection Text [Headless]
    def context_menu_selectionText_headless():
        from pyvirtualdisplay.display import Display
        from os import path
        import hashlib
        import time

        from selenium.webdriver.common.by import By
        from selenium.webdriver import ActionChains, Chrome, ChromeOptions, Keys
        from selenium.webdriver.support.wait import WebDriverWait
        from selenium.webdriver import Chrome, ChromeOptions
        from selenium.webdriver.chrome.service import Service

        import subprocess

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

        def get_ext_id(path_to_extension):
            abs_path = path.abspath(path_to_extension)
            m = hashlib.sha256()
            m.update(abs_path.encode("utf-8"))
            ext_id = "".join([chr(int(i, base=16) + 97) for i in m.hexdigest()][:32])
            url_path = f"chrome-extension://{ext_id}/popup.html"
            return url_path, abs_path
            
        with Display() as disp:

            payloads = payloads('payloads/small_payload.txt')
            url_path, abs_path = get_ext_id('Extensions/h1-replacer/h1-replacer(v3)_context_menu')

            print(disp.is_alive())
            print(disp.display)
            options = ChromeOptions()
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--no-sandbox")
            load_ext_arg = "load-extension=" + abs_path
            options.add_argument(load_ext_arg)
            driver = Chrome(service=Service(), options=options)

            # get www.example.com
            driver.get('file:///home/showloser/localhost/dynamic/miscellaneous/xss_website.html')
            # set handler for example.com
            example = driver.current_window_handle

            # get extension popup.html
            driver.switch_to.new_window('tab')
            extension = driver.current_window_handle
            driver.get(url_path)
            driver.save_screenshot('ss.png')
            time.sleep(2)

            for payload in payloads:
                print(payload)
                # driver.switch_to.window(extension)
                # driver.refresh()

                driver.switch_to.window(example)

                driver.execute_script(f'document.getElementById("h1_element").innerText = `{payload}`')
                target_element = driver.find_element(By.ID, 'h1_element')

                # Select the text using JavaScript
                driver.execute_script("window.getSelection().selectAllChildren(arguments[0]);", target_element)


                actions = ActionChains(driver)
                actions.context_click(target_element).perform()


                driver.save_screenshot('ss.png')
                time.sleep(2)


                for _ in range(6):
                    subprocess.call(['xdotool', 'key', 'Down'])

                # Simulate pressing the "Enter" key
                subprocess.call(['xdotool', 'key', 'Return'])

                try:
                    # wait 2 seconds to see if alert is detected
                    WebDriverWait(driver, 2).until(EC.alert_is_present())
                    alert = driver.switch_to.alert
                    alert.accept()
                    print('+ Alert Detected +')
                except TimeoutException:
                    print('= No alerts detected =')


                driver.switch_to.window(extension)
                driver.save_screenshot('ss.png')
                time.sleep(1)


                driver.switch_to.window(example)
                driver.save_screenshot('ss.png')
                time.sleep(1)

    # Link Url     
    def context_menu_link_url_new():

        website = "file:///home/showloser/dynamic/miscellaneous/xss_website.html"

        try:
            # get test xss website
            driver.get(website)
            # set handler for example.com
            example = driver.current_window_handle

            # Wait up to 5 seconds for the title to become "Xss Website"
            title_condition = EC.title_is('Xss Website')
            WebDriverWait(driver, 5).until(title_condition)

            # get page source code of example.com
            example_source_code = driver.page_source

            # get extension popup.html
            driver.switch_to.new_window('tab')
            extension = driver.current_window_handle
            driver.get(url_path)

            # get page source code of extension
            extension_source_code = driver.page_source

            cases = ['queryParams', 'fragementIdentifier']


            for payload in payloads:

                # there are 2 possible ways to insert paylaod, either directly or using query parameters.
                for i in range(len(cases)):
                    # for link url, inject our payload into the link.
                    driver.switch_to.window(example)

                    # using selenium to find element by ID
                    target_element = driver.find_element(By.ID, 'linkUrl')

                    # Payload Injection (Href)
                    if i == 0:
                        try:
                            # PAYLOAD INJECTION CASE 1 (Directly Injecting)
                            print('Directly Injecting')
                            driver.execute_script(f'var linkElement = document.getElementById("linkUrl"); linkElement.href = `{payload}`')
                        except Exception as e:
                            print(' !!!! PAYLOAD FAILLED !!!!')
                            print('Error: ', str(e))
                            continue
                    elif i == 1:
                        try:
                            print('query params')
                            # PAYLOAD INJECTION CASE 2 (Injecting Query Parameters)
                            driver.execute_script(f'var linkElement = document.getElementById("linkUrl"); linkElement.href = "?q=`{payload}`"')
                        except Exception as e:
                            print(' !!!! PAYLOAD FAILLED !!!!')
                            print('Error: ', str(e))
                            continue
                    else:
                        print('ERROR') # lol this shd nvr happen

                    
                    # Seleting Text using javascript
                    try:
                        # perform text highlight/selection
                        driver.execute_script("window.getSelection().selectAllChildren(arguments[0]);", target_element)


                        # usage of context menu
                        try:
                            # perform right click to open context menu
                            actions = ActionChains(driver)
                            actions.context_click(target_element).perform()

                            # navigate to extension context menu option
                            keyboard = Controller()
                            for _ in range(11):  
                                # Press the arrow key down
                                keyboard.press(Key.down)
                                # Release the arrow key
                                keyboard.release(Key.down)

                            # Press the Enter key
                            keyboard.press(Key.enter)
                            # Release the Enter key
                            keyboard.release(Key.enter)

                        except Exception as e:
                            print(' !!!! Error using Context Menu !!!!')
                            print('Error: ', str(e))
                            continue

                    except Exception as e:
                        print(' !!!! Error Selecting Text !!!!')
                        print('Error: ', str(e))
                        continue
                
                    # observe behavior after payload injection
                    # 1) Check for alerts in example.com
                    driver.switch_to.window(example)
                    try:
                        # wait 2 seconds to see if alert is detected
                        WebDriverWait(driver, 2).until(EC.alert_is_present())
                        alert = driver.switch_to.alert
                        alert.accept()
                        print('+ Alert Detected +')
                    except TimeoutException:
                        print('= No alerts detected =')
                    

                    # 2) Check for alerts in extension
                    driver.switch_to.window(extension)
                    try:
                        # wait 2 seconds to see if alert is detected
                        WebDriverWait(driver, 2).until(EC.alert_is_present())
                        alert = driver.switch_to.alert
                        alert.accept()
                        print('[extension] + Alert Detected +')
                    except TimeoutException:
                        print('[extension] = No alerts detected =')


                    # 3) Check for alerts in example after refreshing extension
                    driver.refresh()
                    driver.switch_to.window(example)
                    try:
                        # wait 2 seconds to see if alert is detected
                        WebDriverWait(driver, 2).until(EC.alert_is_present())
                        alert = driver.switch_to.alert
                        alert.accept()
                        print('[example] + Alert Detected +')
                    except TimeoutException:
                        print('[example] = No alerts detected =')

                    # check for any modifications (snapshot back to original)
                    try: 
                        # [1] check modifications for example.com
                        driver.switch_to.window(example)
                        if example_source_code != driver.page_source:
                            driver.get(website)
                            print(f"Navigated back to '{website}' due to page source changes")

                    except Exception as e:
                        print('Error: ', str(e))


                    try: 
                        # [2] check modifications for extension
                        driver.switch_to.window(extension)
                        if extension_source_code != driver.page_source:
                            driver.get(url_path)
                            print(f"Navigated back to '{url_path}' due to extension page source changes")

                    except Exception as e:
                        print('Error: ', str(e))

        except TimeoutException:
            # Handle TimeoutException when title condition is not met
            print("Timeout: Title was not resolved to 'Example Domain'")

        except Exception as e:
            # Handle any other exceptions that occur
            print("An error occurred:", str(e))

    # Src Url [GUI]
    def context_menu_src_url():
        # get www.example.com
        driver.get('file:////home/showloser/localhost/dynamic/test.html')
        # set handler for example.com
        example = driver.current_window_handle

        # get extension popup.html
        driver.switch_to.new_window('tab')
        extension = driver.current_window_handle
        driver.get(url_path)
    

        for payload in payloads:

            driver.switch_to.window(example)
            target_element = driver.find_element(By.ID, 'srcUrl')
            # driver.execute_script("var range = document.createRange(); range.selectNode(arguments[0]); console.log(range);window.getSelection().addRange(range);", target_element)

            driver.execute_script(f"document.getElementById('srcUrl').src = `{payload}`")

            # # perform right click to open context menu
            actions = ActionChains(driver)

            actions.drag_and_drop_by_offset(actions.move_to_element_with_offset(target_element,50,0).release().perform(), -80,0).context_click().perform()

            # navigate to extension context menu option
            time.sleep(1)
            keyboard = Controller()
            for _ in range(7):  
                # Press the arrow key down
                keyboard.press(Key.down)
                # Release the arrow key
                keyboard.release(Key.down)

            # Press the Enter key
            keyboard.press(Key.enter)
            # Release the Enter key
            keyboard.release(Key.enter)
            
            try:
                # wait 2 seconds to see if alert is detected
                WebDriverWait(driver, 2).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert.accept()
                print('+ Alert Detected +')
            except TimeoutException:
                print('= No alerts detected =')
            
            driver.switch_to.window(extension)
            time.sleep(2)

    # Frame Url 
    def context_menu_frame_url_new():
        
        website = "file:///home/showloser/dynamic/miscellaneous/xss_website.html"

        try:
            # get test xss website
            driver.get(website)
            # set handler for example.com
            example = driver.current_window_handle

            # Wait up to 5 seconds for the title to become "Xss Website"
            title_condition = EC.title_is('Xss Website')
            WebDriverWait(driver, 5).until(title_condition)

            # get page source code of example.com
            example_source_code = driver.page_source

            # get extension popup.html
            driver.switch_to.new_window('tab')
            extension = driver.current_window_handle
            driver.get(url_path)

            # get page source code of extension
            extension_source_code = driver.page_source

            cases = ['queryParams', 'fragementIdentifier']

            for payload in payloads:
                for i in range(len(cases)):
                    driver.switch_to.window(example)

                    # using selenium to find element by ID
                    iframeElement = driver.find_element(By.ID, 'frameUrl')

                    if i == 0:
                        try:
                            print('QueryParams')
                            driver.execute_script(f'var frameElement = document.getElementById("frameUrl"); frameElement.src = `https://www.example_xss.com/XSS?q={payload}`')
                        except Exception as e:
                            print(' !!!! PAYLOAD FAILLED !!!!')
                            print('Error: ', str(e))
                            continue
                    elif i == 1:
                        try:
                            print('RragmentIdentifier')
                            driver.execute_script(f'var frameElement = document.getElementById("frameUrl"); frameElement.src = `https://www.example_xss.com/XSS#{payload}`')
                        except Exception as e:
                            print(' !!!! PAYLOAD FAILLED !!!!')
                            print('Error: ', str(e))
                            continue
                    else:
                        print('ERROR')

                    # usage of context menu
                    try:
                        # # perform right click to open context menu
                        actions = ActionChains(driver)
                        actions.move_to_element(iframeElement)
                        actions.context_click().perform()

                        # navigate to extension context menu option
                        keyboard = Controller()
                        for _ in range(8):  
                            # Press the arrow key down
                            keyboard.press(Key.down)
                            # Release the arrow key
                            keyboard.release(Key.down)

                        # Press the Enter key
                        keyboard.press(Key.enter)
                        # Release the Enter key
                        keyboard.release(Key.enter)

                    except Exception as e:
                        print(' !!!! Error using Context Menu !!!!')
                        print('Error: ', str(e))
                        continue

                    
                    # observe behavior after payload injection
                    # 1) Check for alerts in example.com
                    driver.switch_to.window(example)
                    try:
                        # wait 2 seconds to see if alert is detected
                        WebDriverWait(driver, 2).until(EC.alert_is_present())
                        alert = driver.switch_to.alert
                        alert.accept()
                        print('+ Alert Detected +')
                    except TimeoutException:
                        print('= No alerts detected =')

                    # 2) Check for alerts in extension
                    driver.switch_to.window(extension)
                    try:
                        # wait 2 seconds to see if alert is detected
                        WebDriverWait(driver, 2).until(EC.alert_is_present())
                        alert = driver.switch_to.alert
                        alert.accept()
                        print('[extension] + Alert Detected +')
                    except TimeoutException:
                        print('[extension] = No alerts detected =')

                    # 3) Check for alerts in example after refreshing extension
                    driver.refresh()
                    driver.switch_to.window(example)
                    try:
                        # wait 2 seconds to see if alert is detected
                        WebDriverWait(driver, 2).until(EC.alert_is_present())
                        alert = driver.switch_to.alert
                        alert.accept()
                        print('[example] + Alert Detected +')
                    except TimeoutException:
                        print('[example] = No alerts detected =')


                    # check for any modifications (snapshot back to original)
                    try: 
                        # [1] check modifications for example.com
                        driver.switch_to.window(example)
                        if example_source_code != driver.page_source:
                            driver.get(website)
                            print(f"Navigated back to '{website}' due to page source changes")

                    except Exception as e:
                        print('Error: ', str(e))


                    try: 
                        # [2] check modifications for extension
                        driver.switch_to.window(extension)
                        if extension_source_code != driver.page_source:
                            driver.get(url_path)
                            print(f"Navigated back to '{url_path}' due to extension page source changes")

                    except Exception as e:
                        print('Error: ', str(e))

        except TimeoutException:
            # Handle TimeoutException when title condition is not met
            print("Timeout: Title was not resolved to 'Example Domain'")

        except Exception as e:
            # Handle any other exceptions that occur
            print("An error occurred:", str(e))

    # PageUrl 
    def context_menu_page_url_new():
        website = "file:///home/showloser/dynamic/miscellaneous/xss_website.html"
        
        # Maximum wait time of 5 seconds
        wait = WebDriverWait(driver,5)

        try:
            # get test xss website
            driver.get(website)
            # set handler for example.com
            example = driver.current_window_handle

            # Wait up to 5 seconds for the title to become "Xss Website"
            title_condition = EC.title_is('Xss Website')
            WebDriverWait(driver, 5).until(title_condition)

            # get page source code of example.com
            example_source_code = driver.page_source

            # get extension popup.html
            driver.switch_to.new_window('tab')
            extension = driver.current_window_handle
            driver.get(url_path)

            # get page source code of extension
            extension_source_code = driver.page_source

            cases = ['queryParams', 'fragementIdentifier']

            for payload in payloads:
                for i in range(len(cases)):
                    driver.switch_to.window(example)

                    # url encode xss payload 
                    encoded_payload = urllib.parse.quote(payload)


                    if i == 0:
                        try:    
                            print('QueryParams')
                            driver.execute_script(f"window.history.replaceState(null, null, `{website}?qureyParam={encoded_payload}`)")
                        except Exception as e:
                            print(' !!!! PAYLOAD FAILLED !!!!')
                            print('Error: ', str(e))
                            continue
                    elif i == 1:
                        try:
                            print('FragmentIdentifier')
                            driver.execute_script(f"window.history.replaceState(null, null, `{website}#{encoded_payload}`)")
                        except Exception as e:
                            print(' !!!! PAYLOAD FAILLED !!!!')
                            print('Error: ', str(e))
                            continue
                    else:
                        print("ERROR")

                    PageUrlElement = wait.until(EC.presence_of_element_located((By.ID, 'pageUrl')))

                    # usage of context menu
                    try:
                        # # perform right click to open context menu
                        actions = ActionChains(driver)
                        actions.move_to_element(PageUrlElement)
                        actions.context_click().perform()


                        # navigate to extension context menu option
                        keyboard = Controller()
                        for _ in range(8):  
                            # Press the arrow key down
                            keyboard.press(Key.down)
                            # Release the arrow key
                            keyboard.release(Key.down)

                        # Press the Enter key
                        keyboard.press(Key.enter)
                        # Release the Enter key
                        keyboard.release(Key.enter)

                    except Exception as e:
                        print(' !!!! Error using Context Menu !!!!')
                        print('Error: ', str(e))
                        continue


                    # observe behavior after payload injection
                    # 1) Check for alerts in example.com
                    driver.switch_to.window(example)
                    try:
                        # wait 2 seconds to see if alert is detected
                        WebDriverWait(driver, 2).until(EC.alert_is_present())
                        alert = driver.switch_to.alert
                        alert.accept()
                        print('+ Alert Detected +')
                    except TimeoutException:
                        print('= No alerts detected =')

                    # 2) Check for alerts in extension
                    driver.switch_to.window(extension)
                    try:
                        # wait 2 seconds to see if alert is detected
                        WebDriverWait(driver, 2).until(EC.alert_is_present())
                        alert = driver.switch_to.alert
                        alert.accept()
                        print('[extension] + Alert Detected +')
                    except TimeoutException:
                        print('[extension] = No alerts detected =')

                    # 3) Check for alerts in example after refreshing extension
                    driver.refresh()
                    driver.switch_to.window(example)
                    try:
                        # wait 2 seconds to see if alert is detected
                        WebDriverWait(driver, 2).until(EC.alert_is_present())
                        alert = driver.switch_to.alert
                        alert.accept()
                        print('[example] + Alert Detected +')
                    except TimeoutException:
                        print('[example] = No alerts detected =')

                    # check for any modifications (snapshot back to original)
                    try: 
                        # [1] check modifications for example.com
                        driver.switch_to.window(example)
                        if example_source_code != driver.page_source:
                            driver.get(website)
                            print(f"Navigated back to '{website}' due to page source changes")

                    except Exception as e:
                        print('Error: ', str(e))

                    try: 
                        # [2] check modifications for extension
                        driver.switch_to.window(extension)
                        if extension_source_code != driver.page_source:
                            driver.get(url_path)
                            print(f"Navigated back to '{url_path}' due to extension page source changes")

                    except Exception as e:
                        print('Error: ', str(e))


        except TimeoutException:
            # Handle TimeoutException when title condition is not met
            print("Timeout: Title was not resolved to 'Example Domain'")

        except Exception as e:
            # Handle any other exceptions that occur
            print("An error occurred:", str(e))
 
# 10) chromeTabsQuery
def chromeTabsQuery(driver,ext_id, url_path, payloads, result):
    properties = ['favIconUrl', 'sessionId', 'title', 'url']

    def chromeTabQuery_title():
        # Case Secnario for chromeTabQuery_Title

        # get www.example.com
        driver.get('https://www.example.com')
        # set handler for example.com
        example = driver.current_window_handle

        # get extension popup.html
        driver.switch_to.new_window('tab')
        extension = driver.current_window_handle
        driver.get(url_path)


        for payload in payloads:
            
            # change to example.com to change document.title property
            driver.switch_to.window(example)
            driver.refresh()
            driver.execute_script(f'document.title = `{payload}`;')

            # change to extension:
            driver.switch_to.window(extension)
            driver.refresh()

            driver.execute_script("document.getElementById('entryPoint').value = '2';")
            driver.execute_script("document.getElementById('submit').click();")

            driver.switch_to.window(example)
            try:
                # wait 5 seconds to see if alert is detected
                WebDriverWait(driver, 5).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert.accept()
                print('+ Alert Detected +')
            except TimeoutException:
                print('= No alerts detected =')

    def chromeTabQuery_url():
        # Case Secnario for chromeTabQuery_Title

        # get www.example.com
        driver.get('https://www.example.com')
        # set handler for example.com
        example = driver.current_window_handle

        # get extension popup.html
        driver.switch_to.new_window('tab')
        extension = driver.current_window_handle
        driver.get(url_path)


        for payload in payloads:
            payload = payload.strip()
            
            # change to example.com to change url property
            driver.switch_to.window(example)
            # driver.execute_script(f"location.href = 'https://www.example.com/?p{payload}'")
            driver.execute_script(f"location.href = 'https://www.example.com/?p={payload}'")


            # change to extension:
            driver.switch_to.window(extension)
            driver.refresh()

            driver.execute_script("document.getElementById('entryPoint').value = '3';")
            driver.execute_script("document.getElementById('submit').click();")

            driver.switch_to.window(example)
            try:
                # wait 5 seconds to see if alert is detected
                WebDriverWait(driver, 5).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert.accept()
                print('+ Alert Detected +')
            except TimeoutException:
                print('= No alerts detected =')

    def chromeTabQuery_favIconUrl():

        def payload_generation(payloads):
            favIconUrl_payloads = []

            def check_line(line):
                # ISSUE
                # ISSUE: because of url encoding, if our file has ', it might not be able to access it!
                # ISSUE
                # forbidden_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|', "'"]
                forbidden_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']

                return all(char not in line for char in forbidden_chars)

            def find_lines_without_chars(filename):
                with open(filename, 'r') as file:
                    lines = file.readlines()
                    lines_without_chars = [line.rstrip('\n') for line in lines if check_line(line)]
                    return lines_without_chars

            filename = 'payloads/payloads.txt'
            lines_without_chars = find_lines_without_chars(filename)
            for line in lines_without_chars:
                favIconUrl_payloads.append(line)
            
            return favIconUrl_payloads

        favIconUrl_payloads = payload_generation(payloads)

        def rename_file_with_payloads(favIconUrl_payloads):

            folder_path = "miscellaneous/favIconUrl_payload"
            files = os.listdir(folder_path)
            if len(files) == 0:
                print("No files found in the test folder.")
                return
            elif len(files) > 1:
                print("Multiple files found in the test folder. Please ensure there is only one file.")
                return

            old_filename = os.path.join(folder_path, files[0])



            new_filename = os.path.join(folder_path, favIconUrl_payloads + ".jpg")
            os.rename(old_filename, new_filename)
            print(f"File renamed to: {new_filename}, ")
            old_filename = new_filename

        def changeFavIconUrl(driver, payload):
            # remove current favIconUrl
            driver.execute_script("""
            var linkElement = document.querySelector('link[rel="icon"]');
            if (linkElement) {
            linkElement.parentNode.removeChild(linkElement);
            }
            """)

            # set new favIconUrl
            driver.execute_script(f"""
            var link = document.createElement('link');
            link.type = 'image/jpg';
            link.rel = 'icon';
            link.href = 'favIconUrl_payload/{payload}.jpg';
            document.head.appendChild(link);
            """)


        # get www.example.com
        driver.get('file:///home/showloser/localhost/dynamic/miscellaneous/xss_website.html')
        # set handler for example.com
        example = driver.current_window_handle
        # add a default favIconUrl
        driver.execute_script("""
        var link = document.createElement('link');
        link.type = 'image/jpg';
        link.rel = 'icon';
        link.href = 'default.jpg';
        document.head.appendChild(link);
        """)

        # get extension popup.html
        driver.switch_to.new_window('tab')
        extension = driver.current_window_handle
        driver.get(url_path)

        for i in favIconUrl_payloads:
            time.sleep(1)
            driver.switch_to.window(example)

            # change filename to payloads
            rename_file_with_payloads(i)

            # use filename as payload in ext
            changeFavIconUrl(driver, i)

            try:
                # wait 2 seconds to see if alert is detected
                WebDriverWait(driver, 2).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert.accept()
                print('[FALSE] Alert Detected [FALSE]')
            except TimeoutException:
                print('[FALSE] No alerts detected [FALSE]')

                
            driver.switch_to.window(extension)

            # use the extension
            driver.execute_script("document.getElementById('entryPoint').value = '0';")
            driver.execute_script("document.getElementById('submit').click();")

            driver.switch_to.window(example)
            try:
                # wait 2 seconds to see if alert is detected
                WebDriverWait(driver, 2).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert.accept()
                print('+ Alert Detected +')
            except TimeoutException:
                print('= No alerts detected =')

# 11) locationSearch
def locationSearch(driver, ext_id, url_path, payloads, result):

    # get www.example.com
    driver.get('https://www.example.com')
    # set handler for example.com
    example = driver.current_window_handle

    # get extension popup.html
    driver.switch_to.new_window('tab')
    extension = driver.current_window_handle
    driver.get(url_path)

    for payload in payloads:

        # define a query parameter
        driver.switch_to.window(example)
        driver.execute_script(f'window.location.search=`?q={payload}`')

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

# 12) window.addEventLister.msg
def windowAddEventListenerMessage(driver, ext_id, url_path, payloads, result):
    # PAYLOAD: 
    # postMessage({ message: "<img src=x onerror=alert(1)>" }, "*")
    
    # get xss test website
    driver.get('file:////home/showloser/localhost/dynamic/test.html')
    # set handler for example.com
    example = driver.current_window_handle

    # get extension popup.html
    driver.switch_to.new_window('tab')
    extension = driver.current_window_handle
    driver.get(url_path)

    # pre-configure
    buttons = driver.find_elements(By.TAG_NAME,"button")
    for button in buttons:
        button.click()

    # implement tommorow 

    regex_results = ['data', 'log', 'cocksuker123', '123skd', 'message']
    # regex_results = []

    xss_payload = '<img src=x onerror=alert(1)>'

    driver.switch_to.window(example)

    # check if regex scan found anything
    # if regex able to find scan results, send payload as json object
    if len(regex_results) > 0:
        object_payload = {key: xss_payload for key in regex_results}
        driver.execute_script(f"window.postMessage({object_payload},'*')")

        try:
            # wait 2 seconds to see if alert is detected
            WebDriverWait(driver, 2).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert.accept()
            print('+ Alert Detected +')
        except TimeoutException:
            print('= No alerts detected =')

    # else, send payload as string
    else:
        driver.execute_script(f"window.postMessage(`{xss_payload}`,'*')")

        try:
            # wait 2 seconds to see if alert is detected
            WebDriverWait(driver, 2).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert.accept()
            print('+ Alert Detected +')
        except TimeoutException:
            print('= No alerts detected =')

# html inputs and buttons
def button_input_paradox():
    from bs4 import BeautifulSoup
    def hierarchy_method():
        # basically tries to associate which button is for the input by using the hierarchy as a guide (same parent)

        id_of_button = 'replaceButton'
        id_of_input = 'replacementInput'
        id_of_fakeButton = 'fakeButton'


        buttons = [id_of_button,id_of_fakeButton]
        buttons = [id_of_fakeButton,id_of_button]

        # input = [id_of_input]

        def find_associated_button(input, buttons, html_source):

            # Locate the input field using BeautifulSoup
            soup = BeautifulSoup(html_source, 'html.parser')
        
            for button_id in buttons:
                button = soup.find('button', id=button_id)
                if has_common_parent(input, button_id, html_source):
                    button_id = button.get('id')
                    return button_id
                
            # No associated button found
            return None

        def has_common_parent(input_field, button, html_source):
            soup = BeautifulSoup(html_source, 'html.parser')
            input_element = soup.find(id=input_field)
            button_element = soup.find(id=button)

            if (input_element.parent == button_element.parent):
                return True
            
            return False


        with open('Extensions/h1-replacer/h1-replacer_testing/popup.html', 'r') as file:
            html_source = file.read()

    
        associated_button_id = find_associated_button(id_of_input, buttons, html_source)
        print(associated_button_id)

    def button_proximity():
        # basically tries to associate which button is for the input by finding the nearest button to the input

        # Assuming 'html_source_code' contains the HTML source code
        with open('Extensions/h1-replacer/h1-replacer_testing/popup.html', 'r') as file:
            html_source = file.read()
        soup = BeautifulSoup(html_source, 'html.parser')

        # Assuming 'input_field_id' contains the ID of the input field
        input_field = soup.find('input', id='replacementInput')

        # Assuming 'button1_id' and 'button2_id' contain the IDs of the two buttons
        button1 = soup.find('button', id='fakeButton')
        button2 = soup.find('button', id='replaceButton')

        # Get the position of the input field and each button in the HTML document
        input_field_position = input_field.sourceline
        button1_position = button1.sourceline
        button2_position = button2.sourceline

        # Calculate the distance between the input field and each button based on their positions
        distance_button1 = abs(button1_position - input_field_position)
        distance_button2 = abs(button2_position - input_field_position)

        # Determine the nearest button
        nearest_button = button1 if distance_button1 < distance_button2 else button2

        # Print the ID of the nearest button
        print("Nearest Button:", nearest_button['id'])

    def prefix_comparison():
        # basically tries to associate which button is for which input by finding similarity in id names

        # Assuming 'html_source_code' contains the HTML source code
        with open('Extensions/h1-replacer/h1-replacer_testing/popup.html', 'r') as file:
            html_source = file.read()
        soup = BeautifulSoup(html_source, 'html.parser')

        input_id = "replacementInput" 
        button_ids = ["replaceButton", "fakeButton"]
        button_ids = ["fakeButton", "replaceButton"]

        # Create a dictionary to store the common prefix lengths for each button
        common_prefix_lengths = {}



        # Compare the prefix of input ID with the button IDs
        for button_id in button_ids:
            # Find the common prefix between the input ID and button ID
            common_prefix = ''
            for a, b in zip(input_id, button_id):
                if a != b:
                    break
                common_prefix += a

            # Store the length of the common prefix for each button
            common_prefix_lengths[button_id] = len(common_prefix)

        # Find the button ID with the highest common prefix length
        button_with_highest_prefix = max(common_prefix_lengths, key=common_prefix_lengths.get)
        print("button_with_highest_prefix: " + button_with_highest_prefix)


        # # [Verbose mode]#

        # # Sort the button IDs based on the common prefix length in descending order
        # sorted_button_ids = sorted(common_prefix_lengths, key=common_prefix_lengths.get, reverse=True)

        # # Print the sorted button IDs along with their common prefix lengths (rankings)
        # for rank, button_id in enumerate(sorted_button_ids, start=1):
        #     common_prefix_length = common_prefix_lengths[button_id]
        #     print(f"Rank {rank}: Button ID {button_id} (Common Prefix Length: {common_prefix_length})")


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
                            line = line.replace(a, "active: false")
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
def main(extension_path, semgrep_results):
    # Run program
    with Display() as disp:
        print(disp.is_alive())

        initialise_headless(extension_path,semgrep_results)
