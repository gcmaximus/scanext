import json
import logging
import os
import shutil
import subprocess
import time
import urllib.parse
from datetime import datetime as dt
from functools import reduce
from pathlib import Path

import requests
from selenium.common.exceptions import NoAlertPresentException, TimeoutException
from selenium.webdriver import ActionChains, Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# from main import payload_logging

# Chrome Extension Entry points
# 1) window.name
# 2) location.href
# 3) location.search
# 4) location.hash
# 5) contextMenu
# 6) onMessage
# 7) onConnect
# 8) chrome.tabs.query
# 9) chrome.tabs.get
# 10) chrome.getCurrent
# 11) window.addEventListerner.message
# 12) chrome.runtime.onConnectExternal
# 13) chrome.debugger.getTargets
# 14) chrome.runtime.onMessageExternal 
# logging framework

# magic function (name to be changed)
def nomagic(chain, payload, msg):
    keys = chain.split('.')[1:]
    msg.update(reduce(lambda x, y: {y: x}, reversed(keys), payload))
    obj = json.dumps(msg)
    return obj

#####################
# Logging Framework #
#####################

def setup_logger(logger_name, log_file, log_level=logging.ERROR):
    logger = logging.getLogger(logger_name)
    handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s - [%(name)s] - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(log_level)
    return logger

# Setup the logger for the other file
error_logger = setup_logger('error_logger', 'DYNAMIC_ANALYSIS/Logs/error_log.log', logging.ERROR)


def error_logging(source, error, max_chars=200):
    # Remove newline characters from the error message
    error = error.replace('\n', ' ')

    # Truncate the error message to the specified maximum characters
    error = error[:max_chars]

    # Actual Logging
    error_logger.error(f"[{source}] - {error}")


def payload_logging(outcome, source, extension_id, extension_name, url_of_website, payload_type, payload, script, time_of_injection, time_of_alert, payload_filename, packet_info):
    # payload logs
    return {
        "outcome": outcome,
        "source": source,
        "extensionId": extension_id,
        "extensionName": extension_name,
        "Url": url_of_website,
        "payloadType": payload_type,
        "payload": payload,
        "script": script,
        "timeOfInjection": time_of_injection,
        "timeOfAlert": time_of_alert,
        "payload_fileName": payload_filename,
        "packetInfo": packet_info
    }


##########################
# Case Scenario headless #
##########################
#   Updated functions    #
####################################################################################

def handle_multiple_alerts(driver):
    while True:
        try:
            # Check if an alert is present
            alert = driver.switch_to.alert
            # If an alert is present, accept it
            alert.accept()
        except NoAlertPresentException:
            # If no alert is present, exit the loop
            break

# 1) runtime.onMessage
def runtime_onM(args_tuple):
    progress_bar, order, option, payloads, url_path, ext_id, ext_name, payload_file, result, server_payloads = args_tuple
    logs = []
    scripts = []
    payload = {}
    source = 'chrome.runtime.onMessage'
    url_of_injection_example = 'https://www.example.com'
    

    for payload_no, i in enumerate(payloads):
        dots = '.'
        taintsink = result["sink"]
        obj = {}
        var = ""
        try:
            if result["metavars"]["MESSAGEPROPERTY"]:
                msgproperty = result["metavars"]["MESSAGEPROPERTY"]
        except:
            msgproperty = ""
        try:
            if result["metavars"]["MESSAGEPASSWORD"]:
                msgpassword = result["metavars"]["MESSAGEPASSWORD"]
        except:
            msgpassword = ""
        if msgpassword!="" and msgproperty!="":
            obj[msgproperty] = msgpassword
        if dots in taintsink:
            obj = nomagic(taintsink,i,obj)
            var = f"obj = JSON.parse('{obj}');"
        else:
            var = f"obj = '{i}';"

        script = f"{var}chrome.runtime.sendMessage(obj)"
        scripts.append(script)
        payload[payload_no] = i
    
    driver = Chrome(service=Service(), options=option)

    try:
        # Navigate to example.com
        driver.get(url_of_injection_example)
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

        for num, script in enumerate(scripts):
            # update progress bar
            progress_bar.update(1)
            # for runtime.onMessage, scripts shall be executed in the chrome extension popup
            try:
                driver.execute_script(script)
                time_of_injection = dt.utcnow()

            except Exception as e:
                # print(' !!!! PAYLOAD FAILLED !!!!')
                # print('Error: ', str(e))
                driver.refresh()
                continue
            # check for alerts in example
            driver.switch_to.window(example)
            try:
                # wait 2 seconds to see if alert is detected
                WebDriverWait(driver, 2).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert.accept()

                # get time of success [2) extension]
                time_of_success = dt.utcnow()
                logs.append(payload_logging("SUCCESS", source, ext_id, ext_name, url_of_injection_example, 'normal', payload[num], script, time_of_injection, time_of_success, payload_file, 'nil'))
            except TimeoutException:
                # log for failed payloads
                logs.append(payload_logging("FAILURE", source, ext_id, ext_name, url_of_injection_example, 'normal', payload[num], script, time_of_injection, 'nil', payload_file, 'nil'))

            try: 
                # check modifications for example.com
                driver.switch_to.window(example)
                if example_source_code != driver.page_source:
                    driver.get("https://www.example.com")
            except:
                driver.refresh()

            try: 
                # check modifications for extension
                driver.switch_to.window(extension)
                if extension_source_code != driver.page_source:
                    driver.get(url_path)
            except:
                driver.refresh()

    except TimeoutException:
        # Handle TimeoutException when title condition is not met
        pass
    except Exception as e:
        # Handle any other exceptions that occur
        pass
    return logs

# 2) runtime.onConnect
def runtime_onC(args_tuple):
    progress_bar, order, option, payloads, url_path, ext_id, ext_name, payload_file, result, server_payloads = args_tuple
    logs = []
    scripts = []
    payload = {}
    source = 'chrome.runtime.onConnect'
    url_of_injection_example = 'https://www.example.com'
    

    for payload_no, i in enumerate(payloads):
        dots = '.'
        taintsink = result["sink"]
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
            obj = nomagic(taintsink,i,obj)
            var = f"obj = JSON.parse('{obj}');"
        else:
            obj = i
            var = f"obj = '{obj}'"

        if port!="" and portproperty!="" and portpassword!="":
            connect = {portproperty:portpassword}
            connect = json.dumps(connect)

        func = f".postMessage(obj)"
        script = f"{var}chrome.runtime.connect({connect}){func}"
        scripts.append(script)
        payload[payload_no] = i

    driver = Chrome(service=Service(), options=option)
    try:
        # Navigate to example.com
        driver.get(url_of_injection_example)
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

        for num, script in enumerate(scripts):
            # update progress bar
            progress_bar.update(1)
            # for runtime.onConnect, scripts shall be executed in the chrome extension popup
            try:
                driver.execute_script(script)
                time_of_injection = dt.utcnow()
            except Exception as e:
                # print(' !!!! PAYLOAD FAILLED !!!!')
                driver.refresh()
                continue
            # check for alerts in example
            driver.switch_to.window(example)
            try:
                # wait 2 seconds to see if alert is detected
                WebDriverWait(driver, 2).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert.accept()

                # get time of success [2) extension]
                time_of_success = dt.utcnow()
                logs.append(payload_logging("SUCCESS", source, ext_id, ext_name, url_of_injection_example, 'normal', payload[num], script, time_of_injection, time_of_success, payload_file, 'nil'))
            except TimeoutException:
                logs.append(payload_logging("FAILURE", source, ext_id, ext_name, url_of_injection_example, 'normal', payload[num], script, time_of_injection, 'nil', payload_file, 'nil'))

            try: 
                # check modifications for example.com
                driver.switch_to.window(example)
                if example_source_code != driver.page_source:
                    driver.get("https://www.example.com")
            except:
                driver.refresh()

            try: 
                # check modifications for extension
                driver.switch_to.window(extension)
                if extension_source_code != driver.page_source:
                    driver.get(url_path)
            except:
                driver.refresh()
    except TimeoutException:
        # Handle TimeoutException when title condition is not met
        pass
    except Exception as e:
        # Handle any other exceptions that occur
        pass
    return logs

# 3) cookies.get && cookies.getAll
def cookie_get(args_tuple):
    progress_bar, order, option, payloads, url_path, ext_id, ext_name, payload_file, result, server_payloads = args_tuple
    logs = []
    scripts = []
    payload = {}
    source = 'cookies.get/cookies.getAll'
    url_of_injection_example = 'https://www.example.com'
    
    for payload_no, i in enumerate(payloads):
        dots = '.'
        taintsource = result["taintsource"]
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
                    obj = f'"{i}"="value";'
                elif var[1] == "value":
                    obj = f'"cookie"="{i}";'                
        elif cookie in taintsource and taintsource == y:
            if dots in y:
                var = x.split(dots)
                if var[1] == "name":
                    obj = f'"{i}"="value";'
                elif var[1] == "value":
                    obj = f'"cookie"="{i}";'
        elif cookie in taintsource and taintsource == yvalue:
            if dots in yvalue:
                var = x.split(dots)
                if var[1] == "name":
                    obj = f'"{i}"="value";'
                elif var[1] == "value":
                    obj = f'"cookie"="{i}";'
        
        script = f'document.cookie = {obj} + document.cookie'
        scripts.append(script)
        payload[payload_no] = i 

    driver = Chrome(service=Service(), options=option)
    try:
        # Navigate to example.com
        driver.get(url_of_injection_example)
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

        for num, script in enumerate(scripts):
            # update progress bar
            progress_bar.update(1)
            # cookie case scenario will start from injecting script into example.com
            driver.switch_to.window(example)
            try:
                driver.execute_script(script)

                # get time of injection
                time_of_injection = dt.utcnow()
            except Exception as e:
                driver.refresh()
                # print(' !!!! PAYLOAD FAILLED !!!!')
                continue

            # check for alerts in example
            try:
                # wait 2 seconds to see if alert is detected
                WebDriverWait(driver, 2).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert.accept()
                
                # get time of success [1) example]
                time_of_success = dt.utcnow()
                logs.append(payload_logging("SUCCESS", source, ext_id, ext_name, url_of_injection_example, 'normal', payload[num], script, time_of_injection, time_of_success, payload_file, 'nil'))
                
            except TimeoutException:
                driver.switch_to.window(extension)
                driver.refresh()
                driver.switch_to.window(example)

                # check for alerts in example again (for example, payload then extension)
                try:
                    # wait 2 seconds to see if alert is detected
                    WebDriverWait(driver, 2).until(EC.alert_is_present())
                    alert = driver.switch_to.alert
                    alert.accept()
                    # print('[example] + Alert Detected +')

                    # get time of success [3) example]
                    time_of_success = dt.utcnow()
                    logs.append(payload_logging("SUCCESS", source, ext_id, ext_name, url_of_injection_example, 'normal', payload[num], script, time_of_injection, time_of_success, payload_file, 'nil'))
                except TimeoutException:
                    # print('[example] = No alerts detected =')
                    logs.append(payload_logging("FAILURE", source, ext_id, ext_name, url_of_injection_example, 'normal', payload[num], script, time_of_injection, 'nil', payload_file, 'nil'))

            try: 
                # check modifications for example.com
                driver.switch_to.window(example)
                if example_source_code != driver.page_source:
                    driver.get("https://www.example.com")
                    # print("Navigated back to 'https://www.example.com' due to page source changes")
            except:
                driver.refresh()

            try: 
                # check modifications for extension
                driver.switch_to.window(extension)
                if extension_source_code != driver.page_source:
                    driver.get(url_path)
                    # print(f"Navigated back to '{url_path}' due to extension page source changes")
            except:
                driver.refresh()

    except TimeoutException:
        # Handle TimeoutException when title condition is not met
        # print("Timeout: Title was not resolved to 'Example Domain'")
        pass

    except Exception as e:
        # Handle any other exceptions that occur
        # print("An error occurred:", str(e))
        pass

    return logs

# 4) location.hash
def location_hash(args_tuple):
    progress_bar, order, option, payloads, url_path, ext_id, ext_name, payload_file, result, server_payloads = args_tuple
    logs = []
    scripts = []
    payload = {}
    source = 'location.hash'
    url_of_injection_example = 'https://www.example.com'
    

    for payload_no, i in enumerate(payloads):
        script = f"window.location.hash = '{i}'"
        scripts.append(script)
        payload[payload_no] = i
    driver = Chrome(service=Service(), options=option)
    try:
        # Navigate to example.com
        driver.get(url_of_injection_example)
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

        for num, script in enumerate(scripts):
            # update progress bar
            progress_bar.update(1)
            # location.hash case scenario will start from injecting script into example.com
            driver.switch_to.window(example)
            try:
                driver.execute_script(script)

                # get time of injection
                time_of_injection = dt.utcnow()

            except Exception as e:
                # print(' !!!! PAYLOAD FAILLED !!!!')
                # print('Error: ', str(e))
                driver.refresh()
                continue

            # check for alerts in example (for extension, example then payload)
            try:
                # wait 2 seconds to see if alert is detected
                WebDriverWait(driver, 2).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert.accept()
                # print('[example] + Alert Detected +')
                # get time of success [1) example]
                time_of_success = dt.utcnow()
                logs.append(payload_logging("SUCCESS", source, ext_id, ext_name, url_of_injection_example, 'normal', payload[num], script, time_of_injection, time_of_success, payload_file, 'nil'))
            
            except TimeoutException:
                driver.switch_to.window(extension)
                driver.refresh()
                driver.switch_to.window(example)

                # check for alerts in example again (for example, payload then extension)
                try:
                    # wait 2 seconds to see if alert is detected
                    WebDriverWait(driver, 2).until(EC.alert_is_present())
                    alert = driver.switch_to.alert
                    alert.accept()
                    # print('[example] + Alert Detected +')

                    # get time of success [3) example]
                    time_of_success = dt.utcnow()
                    logs.append(payload_logging("SUCCESS", source, ext_id, ext_name, url_of_injection_example, 'normal', payload[num], script, time_of_injection, time_of_success, payload_file, 'nil'))
                except TimeoutException:
                    # print('[example] = No alerts detected =')
                    logs.append(payload_logging("FAILURE", source, ext_id, ext_name, url_of_injection_example, 'normal', payload[num], script, time_of_injection, 'nil', payload_file, 'nil'))

            try: 
                # check modifications for example.com
                driver.switch_to.window(example)
                if example_source_code != driver.page_source:
                    driver.get("https://www.example.com")
                    # print("Navigated back to 'https://www.example.com' due to page source changes")
            except:
                driver.refresh()

            try: 
                # check modifications for extension
                driver.switch_to.window(extension)
                if extension_source_code != driver.page_source:
                    driver.get(url_path)
                    # print(f"Navigated back to '{url_path}' due to extension page source changes")
            except:
                driver.refresh()

    except TimeoutException:
        # Handle TimeoutException when title condition is not met
        # print("Timeout: Title was not resolved to 'Example Domain'")
        pass

    except Exception as e:
        # Handle any other exceptions that occur
        # print("An error occurred:", str(e))
        pass

    return logs

#  5) runtime.onMessageExternal
def runtime_onME(args_tuple):
    progress_bar, order, option, payloads, url_path, ext_id, ext_name, payload_file, result, server_payloads = args_tuple
    logs = []
    scripts = []
    payload = {}
    source = 'chrome.runtime.onMessageExternal'
    url_of_injection_example = 'https://www.example.com'
    

    for payload_no, i in enumerate(payloads):
        dots = '.'
        taintsink = result["sink"]
        obj = ""
        var = "" 
        if dots in taintsink:
            obj = nomagic(taintsink,i,obj)
            var = f"obj = JSON.parse('{obj}');"
            script = f"{var}chrome.runtime.sendMessage('{ext_id}',obj)"
        else:
            obj = i
            script = f"chrome.runtime.sendMessage('{ext_id}','{obj}')"
        scripts.append(script)
        payload[payload_no] = i
    driver = Chrome(service=Service(), options=option)
    try:
        # Navigate to example.com
        driver.get(url_of_injection_example)
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

        for num, script in enumerate(scripts):
            # update progress bar
            progress_bar.update(1)
            # onMessageExternal case scenario will start from injecting script into example.com
            driver.switch_to.window(example)
            try:
                driver.execute_script(script)

                # get time of injection
                time_of_injection = dt.utcnow()

            except Exception as e:
                # print(' !!!! PAYLOAD FAILLED !!!!')
                # print('Error: ', str(e))
                driver.refresh()
                continue

            # check for alerts in example (for extension, example then payload)
            try:
                # wait 2 seconds to see if alert is detected
                WebDriverWait(driver, 2).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert.accept()
                # print('[example] + Alert Detected +')
                # get time of success [1) example]
                time_of_success = dt.utcnow()
                logs.append(payload_logging("SUCCESS", source, ext_id, ext_name, url_of_injection_example, 'normal', payload[num], script, time_of_injection, time_of_success, payload_file, 'nil'))
            
            except TimeoutException:
                driver.switch_to.window(extension)
                driver.refresh()
                driver.switch_to.window(example)

                # check for alerts in example again (for example, payload then extension)
                try:
                    # wait 2 seconds to see if alert is detected
                    WebDriverWait(driver, 2).until(EC.alert_is_present())
                    alert = driver.switch_to.alert
                    alert.accept()
                    # print('[example] + Alert Detected +')

                    # get time of success [3) example]
                    time_of_success = dt.utcnow()
                    logs.append(payload_logging("SUCCESS", source, ext_id, ext_name, url_of_injection_example, 'normal', payload[num], script, time_of_injection, time_of_success, payload_file, 'nil'))
                except TimeoutException:
                    # print('[example] = No alerts detected =')
                    logs.append(payload_logging("FAILURE", source, ext_id, ext_name, url_of_injection_example, 'normal', payload[num], script, time_of_injection, 'nil', payload_file, 'nil'))

            try: 
                # check modifications for example.com
                driver.switch_to.window(example)
                if example_source_code != driver.page_source:
                    driver.get("https://www.example.com")
                    print("Navigated back to 'https://www.example.com' due to page source changes")
            except:
                driver.refresh()

            try: 
                # check modifications for extension
                driver.switch_to.window(extension)
                if extension_source_code != driver.page_source:
                    driver.get(url_path)
                    print(f"Navigated back to '{url_path}' due to extension page source changes")
            except:
                driver.refresh()

    except TimeoutException:
        # Handle TimeoutException when title condition is not met
        # print("Timeout: Title was not resolved to 'Example Domain'")
        pass

    except Exception as e:
        # Handle any other exceptions that occur
        # print("An error occurred:", str(e))
        pass
    return logs

# 6) runtime.onConnectExternal
def runtime_onCE(args_tuple):
    progress_bar, order, option, payloads, url_path, ext_id, ext_name, payload_file, result, server_payloads = args_tuple
    logs = []
    scripts = []
    payload = {}
    source = 'chrome.runtime.onConnectExternal'
    url_of_injection_example = 'https://www.example.com'
    
    
    for payload_no, i in enumerate(payloads):
        dots = '.'
        taintsink = result["sink"]
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
            obj = nomagic(taintsink,i,obj)
        else:
            obj = i

        if port!="" and portproperty!="" and portpassword!="":
            connect = {portproperty:portpassword}
            connect = json.dumps(connect)

        var = f"obj = JSON.parse('{obj}');"
        func = f".postMessage(obj)"

        script = f"{var}chrome.runtime.connect({connect}){func}"
        print(script)
        scripts.append(script)
        payload[payload_no] = i

    driver = Chrome(service=Service(), options=option)
    try:
        # Navigate to example.com
        driver.get(url_of_injection_example)
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

        for num, script in enumerate(scripts):
            # update progress bar
            progress_bar.update(1)
            # onConnectExternal case scenario will start from injecting script into example.com
            driver.switch_to.window(example)
            try:
                driver.execute_script(script)

                # get time of injection
                time_of_injection = dt.utcnow()

            except Exception as e:
                # print(' !!!! PAYLOAD FAILLED !!!!')
                # print('Error: ', str(e))
                driver.refresh()
                continue

            # check for alerts in example (for extension, example then payload)
            try:
                # wait 2 seconds to see if alert is detected
                WebDriverWait(driver, 2).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert.accept()
                # print('[example] + Alert Detected +')
                # get time of success [1) example]
                time_of_success = dt.utcnow()
                logs.append(payload_logging("SUCCESS", source, ext_id, ext_name, url_of_injection_example, 'normal', payload[num], script, time_of_injection, time_of_success, payload_file, 'nil'))
            
            except TimeoutException:
                driver.switch_to.window(extension)
                driver.refresh()
                driver.switch_to.window(example)

                # check for alerts in example again (for example, payload then extension)
                try:
                    # wait 2 seconds to see if alert is detected
                    WebDriverWait(driver, 2).until(EC.alert_is_present())
                    alert = driver.switch_to.alert
                    alert.accept()
                    # print('[example] + Alert Detected +')

                    # get time of success [3) example]
                    time_of_success = dt.utcnow()
                    logs.append(payload_logging("SUCCESS", source, ext_id, ext_name, url_of_injection_example, 'normal', payload[num], script, time_of_injection, time_of_success, payload_file, 'nil'))
                except TimeoutException:
                    # print('[example] = No alerts detected =')
                    logs.append(payload_logging("FAILURE", source, ext_id, ext_name, url_of_injection_example, 'normal', payload[num], script, time_of_injection, 'nil', payload_file, 'nil'))

            try: 
                # check modifications for example.com
                driver.switch_to.window(example)
                if example_source_code != driver.page_source:
                    driver.get("https://www.example.com")
                    # print("Navigated back to 'https://www.example.com' due to page source changes")
            except:
                driver.refresh()

            try: 
                # check modifications for extension
                driver.switch_to.window(extension)
                if extension_source_code != driver.page_source:
                    driver.get(url_path)
                    # print(f"Navigated back to '{url_path}' due to extension page source changes")
            except:
                driver.refresh()

    except TimeoutException:
        # Handle TimeoutException when title condition is not met
        # print("Timeout: Title was not resolved to 'Example Domain'")
        pass

    except Exception as e:
        # Handle any other exceptions that occur
        # print("An error occurred:", str(e))
        pass
    return logs

# new window.name_normal (works)
def window_name_N(args_tuple):
    progress_bar, order, option, payloads, url_path, ext_id, ext_name, payload_file, result, server_payloads = args_tuple

    logs = []
    source = 'window.name'
    url_of_injection_example = 'https://www.example.com'
    


    driver = Chrome(service=Service(), options=option)
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

        for payload_no, payload in enumerate(payloads):

            # update progress bar
            progress_bar.update(1)
            # since window.name is obtained from the website url, we will inject javascript to change the window.name
            driver.switch_to.window(example)

            try:
                driver.execute_script(f'window.name = `{payload}`;')

                # get time of injection
                time_of_injection = dt.utcnow()
            except Exception as e:
                error_logging(source, str(e))
                continue

            # observe behavior after payload injection
            # check for alerts in example
            try:
                # wait 2 seconds to see if alert is detected
                WebDriverWait(driver, 2).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert.accept()
                # print('[example] + Alert Detected +')

                # get time of success [1) example]
                time_of_success = dt.utcnow()
                logs.append(payload_logging("SUCCESS", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, r'window.name = `{payload}`;', time_of_injection, time_of_success, payload_file, 'nil'))
            
            except TimeoutException:
                # print('[example] = No alerts detected =')
                logs.append(payload_logging("FAILURE", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, r'window.name = `{payload}`;', time_of_injection, 'nil', payload_file, 'nil'))

                # 2) Check for alerts in example after refreshing extension
                driver.switch_to.window(extension)
                driver.refresh()
                driver.switch_to.window(example)

                try:
                    # wait 2 seconds to see if alert is detected
                    WebDriverWait(driver, 2).until(EC.alert_is_present())
                    alert = driver.switch_to.alert
                    alert.accept()
                    # print('[example] + Alert Detected +')

                    # get time of success [3) example]
                    time_of_success = dt.utcnow()
                    logs.append(payload_logging("SUCCESS", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, r'window.name = `{payload}`;', time_of_injection, time_of_success, payload_file, 'nil'))
                except TimeoutException:
                    # print('[example] = No alerts detected =')
                    logs.append(payload_logging("FAILURE", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, r'window.name = `{payload}`;', time_of_injection, 'nil', payload_file, 'nil'))

            try: 
                # check modifications for example.com
                driver.switch_to.window(example)
                if example_source_code != driver.page_source:
                    driver.get("https://www.example.com")
                    # print("Navigated back to 'https://www.example.com' due to page source changes")
            except Exception as e:
                error_logging(source, str(e))
                
            try: 
                # check modifications for extension
                driver.switch_to.window(extension)
                if extension_source_code != driver.page_source:
                    driver.get(url_path)
                    # print(f"Navigated back to '{url_path}' due to extension page source changes")
            except Exception as e:
                error_logging(source, str(e))


    except TimeoutException:
        # Handle TimeoutException when title condition is not met
        # print("Timeout: Title was not resolved to 'Example Domain'")
        error_logging(source, 'Failed to resolve https://www.example.com')

    except Exception as e:
        error_logging(source, str(e))

    return logs

# new location.href_normal (works)
def location_href_N(args_tuple):
    progress_bar, order, option, payloads, url_path, ext_id,result = args_tuple

    logs = []
    source = 'location.href'
    url_of_injection_example = 'https://www.example.com'
    

    driver = Chrome(service=Service(), options=option)
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
        for payload_no, payload in enumerate(payloads):
            
            # update progress bar
            progress_bar.update(1)

            # we can inject a script to change the location.href variable using query parameters or fragment Idenfiers
            for j in range(2):

                driver.switch_to.window(extension)
                driver.refresh()
                driver.switch_to.window(example)

                if j == 0:
                    try:
                        driver.execute_script(f"location.href = `https://www.example.com/?p={payload}`")

                        # get time of injection
                        time_of_injection = dt.utcnow()
                    except Exception as e:
                        error_logging(source, str(e))
                        continue
                else:
                    try:
                        driver.execute_script(f"location.href = `https://www.example.com/#{payload}`")

                        # get time of injection
                        time_of_injection = dt.utcnow()

                    except Exception as e:
                        error_logging(source, str(e))
                        continue

                # observe behavior after payload injection

                # 1) Check for alerts in example
                try:
                    # wait 2 seconds to see if alert is detected
                    WebDriverWait(driver, 2).until(EC.alert_is_present())
                    alert = driver.switch_to.alert
                    alert.accept()

                    time_of_success = dt.utcnow()
                    logs.append(payload_logging("SUCCESS", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, r'location.href = `https://www.example.com/?p={payload}`', time_of_injection, time_of_success, payload_file, 'nil'))

                except TimeoutException:
                    logs.append(payload_logging("FAILURE", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, r'location.href = `https://www.example.com/?p={payload}`', time_of_injection, 'nil', payload_file, 'nil'))

                driver.switch_to.window(extension)

                # 2) Check for alerts in example after refreshing extension
                driver.refresh()
                driver.switch_to.window(example)

                try:
                    # wait 2 seconds to see if alert is detected
                    WebDriverWait(driver, 2).until(EC.alert_is_present())
                    alert = driver.switch_to.alert
                    alert.accept()
                    

                    time_of_success = dt.utcnow()
                    logs.append(payload_logging("SUCCESS", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, r'location.href = `https://www.example.com/?p={payload}`', time_of_injection, time_of_success, payload_file, 'nil'))

                except TimeoutException:
                    logs.append(payload_logging("FAILURE", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, r'location.href = `https://www.example.com/?p={payload}`', time_of_injection, 'nil', payload_file, 'nil'))

                try: 
                    # check modifications for example.com
                    driver.switch_to.window(example)
                    if example_source_code != driver.page_source:
                        driver.get("https://www.example.com")
                        # print("Navigated back to 'https://www.example.com' due to page source changes")
                except:
                    pass

                try: 
                    # check modifications for extension
                    driver.switch_to.window(extension)
                    if extension_source_code != driver.page_source:
                        driver.get(url_path)
                        # print(f"Navigated back to '{url_path}' due to extension page source changes")
                except:
                    pass

    except TimeoutException:
        error_logging(source, 'Failed to resolve https://www.example.com')

    except Exception as e:
        error_logging(source, str(e))

    return logs

# combined contextMenu
def context_menu(args_tuple):
    progress_bar, order, option, payloads, url_path, ext_id, ext_name, payload_file, result, server_payloads = args_tuple

    # new contextMenu.selectionText_normal (works)
    def context_menu_selectionText_N(args_tuple):
        progress_bar, order, option, payloads, url_path, ext_id, ext_name, payload_file, result, server_payloads = args_tuple

        logs = []
        source = 'contextMenu.selectionText'

        url_of_injection_example = 'DYNAMIC_ANALYSIS/miscellaneous/xss_website.html'
        


        driver = Chrome(service=Service(), options=option)
        try:
            relative_path = 'DYNAMIC_ANALYSIS/miscellaneous/xss_website.html'
            website = 'file://' + os.path.abspath(relative_path)

            # get www.example.com
            driver.get(website)
            # driver.save_screenshot('DYNAMIC_ANALYSIS/ss.png')

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

                # update progress bar
                progress_bar.update(1) 

                driver.switch_to.window(example)

                try:
                    driver.execute_script(f'document.getElementById("h1_element").innerText = `{payload}`')

                    # get time of injection
                    time_of_injection = dt.utcnow()

                except Exception as e:
                    error_logging(source, str(e))
                    continue

                target_element = driver.find_element(By.ID, 'h1_element')

                try:
                    # Select the text using JavaScript
                    driver.execute_script("window.getSelection().selectAllChildren(arguments[0]);", target_element)
                except Exception as e:
                    error_logging(source, str(e))
                    continue

                # usage of context menu
                try:
                    actions = ActionChains(driver)
                    actions.context_click(target_element).perform()


                    # driver.save_screenshot('DYNAMIC_ANALYSIS/ss.png')


                    for _ in range(6):
                        subprocess.call(['xdotool', 'key', 'Down'])

                    # Simulate pressing the "Enter" key
                    subprocess.call(['xdotool', 'key', 'Return'])

                except Exception as e:
                    error_logging(source, str(e))
                    continue


                # observe behavior after payload injection
                # 1) Check for alerts in example.com
                try:
                    # wait 2 seconds to see if alert is detected
                    WebDriverWait(driver, 2).until(EC.alert_is_present())
                    alert = driver.switch_to.alert
                    alert.accept()
                    # print('[example] + Alert Detected +')

                    time_of_success = dt.utcnow()
                    logs.append(payload_logging("SUCCESS", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, r'document.getElementById("h1_element").innerText = `{payload}`', time_of_injection, time_of_success, payload_file, 'nil'))

                except TimeoutException:
                    logs.append(payload_logging("FAILURE", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, r'document.getElementById("h1_element").innerText = `{payload}`', time_of_injection, 'nil', payload_file, 'nil'))

                    driver.switch_to.window(extension)

                    # 2) Check for alerts in example after refreshing extension
                    driver.refresh()
                    driver.switch_to.window(example)


                    try:
                        # wait 2 seconds to see if alert is detected
                        WebDriverWait(driver, 2).until(EC.alert_is_present())
                        alert = driver.switch_to.alert
                        alert.accept()
                        
                        time_of_success = dt.utcnow()
                        logs.append(payload_logging("SUCCESS", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, r'document.getElementById("h1_element").innerText = `{payload}`', time_of_injection, time_of_success, payload_file, 'nil'))

                    except TimeoutException:
                        logs.append(payload_logging("FAILURE", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, r'document.getElementById("h1_element").innerText = `{payload}`', time_of_injection, 'nil', payload_file, 'nil'))


                # check for any modifications (snapshot back to original)
                try: 
                    # [1] check modifications for example.com
                    driver.switch_to.window(example)
                    if example_source_code != driver.page_source:
                        driver.get(website)

                except:
                    pass

                try: 
                    # [2] check modifications for extension
                    driver.switch_to.window(extension)
                    if extension_source_code != driver.page_source:
                        driver.get(url_path)
                        # print(f"Navigated back to '{url_path}' due to extension page source changes")

                except:
                    pass

        except TimeoutException:
            error_logging(source, f'Failed to resolve {website}')
            

        except Exception as e:
            error_logging(source, str(e))

        return logs

    # new contextMenu.link_Url (works)
    def context_menu_link_url_N(args_tuple):
        progress_bar, order, option, payloads, url_path, ext_id, ext_name, payload_file, result, server_payloads = args_tuple

        logs = []
        source = 'contextMenu.linkUrl'

        url_of_injection_example = 'DYNAMIC_ANALYSIS/miscellaneous/xss_website.html'
        

        driver = Chrome(service=Service(), options=option)

        try:
            relative_path = 'DYNAMIC_ANALYSIS/miscellaneous/xss_website.html'
            website = 'file://' + os.path.abspath(relative_path)

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

                # update progress bar
                progress_bar.update(1) 

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
                            script = r'var linkElement = document.getElementById("linkUrl"); linkElement.href = `{payload}`'
                            driver.execute_script(f'var linkElement = document.getElementById("linkUrl"); linkElement.href = `{payload}`')
                        
                            # get time of injection
                            time_of_injection = dt.utcnow()
                        except Exception as e:
                            error_logging(source, str(e))
                            continue
                    else:
                        try:
                            # PAYLOAD INJECTION CASE 2 (Injecting Query Parameters)
                            script = r'var linkElement = document.getElementById("linkUrl"); linkElement.href = "?q=" + `{}`'
                            driver.execute_script('var linkElement = document.getElementById("linkUrl"); linkElement.href = "?q=" + `{}`'.format(payload.replace('"', '\\"').replace("'", "\\'")))

                            # get time of injection
                            time_of_injection = dt.utcnow()

                        except Exception as e:
                            error_logging(source, str(e))
                            continue
                    
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
                            for _ in range(11):
                                subprocess.call(['xdotool', 'key', 'Down'])

                            # Simulate pressing the "Enter" key
                            subprocess.call(['xdotool', 'key', 'Return'])

                        except Exception as e:
                            error_logging(source, str(e))
                            continue

                    except Exception as e:
                        error_logging(source, str(e))
                        continue
                
                    # observe behavior after payload injection
                    # 1) Check for alerts in example.com
                    driver.switch_to.window(example)
                    # driver.save_screenshot('DYNAMIC_ANALYSIS/ss.png')

                    try:
                        # wait 2 seconds to see if alert is detected
                        WebDriverWait(driver, 2).until(EC.alert_is_present())
                        alert = driver.switch_to.alert
                        alert.accept()

                        time_of_success = dt.utcnow()
                        logs.append(payload_logging("SUCCESS", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, script, time_of_injection, time_of_success, payload_file, 'nil'))

                    except TimeoutException:
                        logs.append(payload_logging("FAILURE", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, script, time_of_injection, 'nil', payload_file, 'nil'))

                        driver.switch_to.window(extension)

                        # 2) Check for alerts in example after refreshing extension
                        driver.refresh()
                        driver.switch_to.window(example)
                        # driver.save_screenshot('DYNAMIC_ANALYSIS/ss.png')
                        try:
                            # wait 2 seconds to see if alert is detected
                            WebDriverWait(driver, 2).until(EC.alert_is_present())
                            alert = driver.switch_to.alert
                            alert.accept()

                            time_of_success = dt.utcnow()
                            logs.append(payload_logging("SUCCESS", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, script, time_of_injection, time_of_success, payload_file, 'nil'))

                        except TimeoutException:
                            logs.append(payload_logging("FAILURE", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, script, time_of_injection, 'nil', payload_file, 'nil'))

                    # check for any modifications (snapshot back to original)
                    try: 
                        # [1] check modifications for example.com
                        driver.switch_to.window(example)
                        if example_source_code != driver.page_source:
                            driver.get(website)
                            # print(f"Navigated back to '{website}' due to page source changes")

                    except:
                        pass

                    try: 
                        # [2] check modifications for extension
                        driver.switch_to.window(extension)
                        if extension_source_code != driver.page_source:
                            driver.get(url_path)
                            # print(f"Navigated back to '{url_path}' due to extension page source changes")
                    except:
                        pass

        except TimeoutException:
            error_logging(source, f'Failed to resolve {website}')
            pass

        except Exception as e:
            error_logging(source, str(e))
        
        return logs

    # new contextMenu.srcUrl (works)
    def context_menu_src_url_N(args_tuple):
        progress_bar, order, option, payloads, url_path, ext_id, ext_name, payload_file, result, server_payloads = args_tuple

        logs = []
        source = 'contextMenu.srcUrl'

        url_of_injection_example = 'DYNAMIC_ANALYSIS/miscellaneous/xss_website.html'
        


        driver = Chrome(service=Service(), options=option)

        try: 
            relative_path = 'DYNAMIC_ANALYSIS/miscellaneous/xss_website.html'
            website = 'file://' + os.path.abspath(relative_path)

            # get www.example.com
            driver.get(website)
            # set handler for example.com
            example = driver.current_window_handle
            # driver.save_screenshot('DYNAMIC_ANALYSIS/ss.png')

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

                # update progress bar
                progress_bar.update(1) 

                driver.switch_to.window(example)
                driver.refresh()

                try:
                    # using javascript, change the SRC value of an oredefined image element
                    target_element = driver.find_element(By.ID, 'srcUrl')
                    driver.execute_script(f"document.getElementById('srcUrl').src = `{payload}`")

                    # get time of injection
                    time_of_injection = dt.utcnow()

                except Exception as e:
                    error_logging(source, str(e))
                    continue

                # usage of contextMenu
                try:
                    # # perform right click to open context menu
                    actions = ActionChains(driver)
                    actions.drag_and_drop_by_offset(actions.move_to_element_with_offset(target_element,50,0).release().perform(), -50,0)
                    actions.move_to_element_with_offset(target_element, 25,0).context_click().perform()

                    # navigate to extension context menu option
                    time.sleep(1)
                    for _ in range(7):
                        subprocess.call(['xdotool', 'key', 'Down'])

                    # Simulate pressing the "Enter" key
                    subprocess.call(['xdotool', 'key', 'Return'])

                except Exception as e:
                    error_logging(source, str(e))
                    continue
            

                # observe behavior after payload injection
                # 1) check for alerts in example
                # driver.save_screenshot('DYNAMIC_ANALYSIS/ss.png')
                try:
                    # wait 2 seconds to see if alert is detected
                    WebDriverWait(driver, 2).until(EC.alert_is_present())
                    alert = driver.switch_to.alert
                    alert.accept()

                    time_of_success = dt.utcnow()
                    logs.append(payload_logging("SUCCESS", source, ext_id, ext_name, url_of_injection_example, 'normal', payload,r"document.getElementById('srcUrl').src = `{payload}`", time_of_injection, time_of_success, payload_file, 'nil'))

                except TimeoutException:
                    logs.append(payload_logging("FAILURE", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, r"document.getElementById('srcUrl').src = `{payload}`", time_of_injection, 'nil', payload_file, 'nil'))


                    # 2) Check for alerts in example after refreshing extension\
                    driver.switch_to.window(extension)
                    driver.refresh()

                    driver.switch_to.window(example)
                    # driver.save_screenshot('DYNAMIC_ANALYSIS/ss.png')

                    try:
                        # wait 2 seconds to see if alert is detected
                        WebDriverWait(driver, 2).until(EC.alert_is_present())
                        alert = driver.switch_to.alert
                        alert.accept()

                        time_of_success = dt.utcnow()
                        logs.append(payload_logging("SUCCESS", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, r"document.getElementById('srcUrl').src = `{payload}`", time_of_injection, time_of_success, payload_file, 'nil'))

                    except TimeoutException:
                        logs.append(payload_logging("FAILURE", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, r"document.getElementById('srcUrl').src = `{payload}`", time_of_injection, 'nil', payload_file, 'nil'))

                try: 
                    # check modifications for example.com
                    driver.switch_to.window(example)
                    if example_source_code != driver.page_source:
                        driver.get(website)
                        # print("Navigated back to 'xss_website.html' due to page source changes")
                except:
                    pass

                try: 
                    # check modifications for extension
                    driver.switch_to.window(extension)
                    if extension_source_code != driver.page_source:
                        driver.get(url_path)
                        # print(f"Navigated back to '{url_path}' due to extension page source changes")
                except:
                    pass

        except TimeoutException:
            error_logging(source, f'Failed to resolve {website}')
            pass

        except Exception as e:
            error_logging(source, str(e))
        
        return logs

    # new contextMenu.frameUrl (works for jerald but not for me. smlj)
    def context_menu_frame_url_N(args_tuple):
        progress_bar, order, option, payloads, url_path, ext_id, ext_name, payload_file, result, server_payloads = args_tuple

        logs = []
        source = 'contextMenu.frameUrl'

        url_of_injection_example = 'DYNAMIC_ANALYSIS/miscellaneous/xss_website.html'
        

        driver = Chrome(service=Service(), options=option)

        try:

            relative_path = 'DYNAMIC_ANALYSIS/miscellaneous/xss_website.html'
            website = 'file://' + os.path.abspath(relative_path)

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

                # update progress bar
                progress_bar.update(1) 

                for i in range(len(cases)):
                    driver.switch_to.window(example)

                    # using selenium to find element by ID
                    iframeElement = driver.find_element(By.ID, 'frameUrl')

                    if i == 0:
                        try:
                            driver.execute_script(f'var frameElement = document.getElementById("frameUrl"); frameElement.src = `https://www.example_xss.com/XSS?q={payload}`')
                            script = r'var frameElement = document.getElementById("frameUrl"); frameElement.src = `https://www.example_xss.com/XSS?q={payload}`;'
                            # get time of injection
                            time_of_injection = dt.utcnow()
                        except Exception as e:
                            error_logging(source, str(e))
                            continue
                    else:
                        try:
                            driver.execute_script(f'var frameElement = document.getElementById("frameUrl"); frameElement.src = `https://www.example_xss.com/XSS#{payload}`')
                            script = r'var frameElement = document.getElementById("frameUrl"); frameElement.src = `https://www.example_xss.com/XSS#{payload}`;'
                            # get time of injection
                            time_of_injection = dt.utcnow()
                        except Exception as e:
                            error_logging(source, str(e))
                            continue

                    # usage of context menu
                    try:
                        # # perform right click to open context menu
                        actions = ActionChains(driver)
                        actions.move_to_element(iframeElement)
                        actions.context_click().perform()

                        # navigate to extension context menu option

                        for _ in range(8):
                            subprocess.call(['xdotool', 'key', 'Down'])

                        # Simulate pressing the "Enter" key
                        subprocess.call(['xdotool', 'key', 'Return'])

                    except Exception as e:
                        error_logging(source, str(e))
                        continue

                    
                    # observe behavior after payload injection
                    # 1) Check for alerts in example.com
                    driver.switch_to.window(example)
                    # driver.save_screenshot('DYNAMIC_ANALYSIS/ss.png')

                    try:
                        # wait 2 seconds to see if alert is detected
                        WebDriverWait(driver, 2).until(EC.alert_is_present())
                        alert = driver.switch_to.alert
                        alert.accept()

                        time_of_success = dt.utcnow()
                        logs.append(payload_logging("SUCCESS", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, script, time_of_injection, time_of_success, payload_file, 'nil'))

                    except TimeoutException:
                        logs.append(payload_logging("FAILURE", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, script, time_of_injection, 'nil', payload_file, 'nil'))

                        # 2) Check for alerts in example after refreshing extension
                        driver.switch_to.window(extension)

                        driver.refresh()
                        driver.switch_to.window(example)

                        try:
                            # wait 2 seconds to see if alert is detected
                            WebDriverWait(driver, 2).until(EC.alert_is_present())
                            alert = driver.switch_to.alert
                            alert.accept()

                            time_of_success = dt.utcnow()
                            logs.append(payload_logging("SUCCESS", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, script, time_of_injection, time_of_success, payload_file, 'nil'))

                        except TimeoutException:
                            logs.append(payload_logging("FAILURE", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, script, time_of_injection, 'nil', payload_file, 'nil'))


                    # check for any modifications (snapshot back to original)
                    try: 
                        # [1] check modifications for example.com
                        driver.switch_to.window(example)
                        if example_source_code != driver.page_source:
                            driver.get(website)
                            # print(f"Navigated back to '{website}' due to page source changes")

                    except:
                        pass

                    try: 
                        # [2] check modifications for extension
                        driver.switch_to.window(extension)
                        if extension_source_code != driver.page_source:
                            driver.get(url_path)
                            # print(f"Navigated back to '{url_path}' due to extension page source changes")

                    except:
                        pass
                    
        except TimeoutException:
            error_logging(source, f'Failed to resolve {website}')

        except Exception as e:
            error_logging(source, str(e))

        return logs

    # new contextMenu.pageUrl (works)
    def context_menu_pageUrl_N(args_tuple):
        progress_bar, order, option, payloads, url_path, ext_id, ext_name, payload_file, result, server_payloads = args_tuple

        logs = []
        source = 'contextMenu.pageUrl'

        url_of_injection_example = 'DYNAMIC_ANALYSIS/miscellaneous/xss_website.html'
        

        driver = Chrome(service=Service(), options=option)
        
        try:
            relative_path = 'DYNAMIC_ANALYSIS/miscellaneous/xss_website.html'
            website = 'file://' + os.path.abspath(relative_path)

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

                # update progress bar
                progress_bar.update(1) 

                for i in range(len(cases)):
                    driver.switch_to.window(example)

                    # url encode xss payload 
                    encoded_payload = urllib.parse.quote(payload)

                    if i == 0:
                        try:    
                            driver.execute_script(f"window.history.replaceState(null, null, `{website}?qureyParam={encoded_payload}`)")
                            script = r"window.history.replaceState(null, null, `{website}?qureyParam={encoded_payload}`);"
                            # get time of injection
                            time_of_injection = dt.utcnow()
                        except Exception as e:
                            error_logging(source, str(e))
                            continue
                    else:
                        try:
                            driver.execute_script(f"window.history.replaceState(null, null, `{website}#{encoded_payload}`)")
                            script = r"window.history.replaceState(null, null, `{website}#{encoded_payload}`);"

                            # get time of injection
                            time_of_injection = dt.utcnow()
                        except Exception as e:
                            error_logging(source, str(e))
                            continue


                    PageUrlElement = driver.find_element(By.ID, 'pageUrl')

                    # usage of context menu
                    try:
                        # # perform right click to open context menu
                        actions = ActionChains(driver)
                        actions.move_to_element(PageUrlElement)
                        actions.context_click().perform()

                        for _ in range(8):
                            subprocess.call(['xdotool', 'key', 'Down'])

                        # Simulate pressing the "Enter" key
                        subprocess.call(['xdotool', 'key', 'Return'])

                    except Exception as e:
                        error_logging(source, str(e))
                        continue


                    # observe behavior after payload injection
                    # 1) Check for alerts in example.com
                    driver.switch_to.window(example)
                    # driver.save_screenshot('DYNAMIC_ANALYSIS/ss.png')
                    try:
                        # wait 2 seconds to see if alert is detected
                        WebDriverWait(driver, 2).until(EC.alert_is_present())
                        alert = driver.switch_to.alert
                        alert.accept()

                        time_of_success = dt.utcnow()
                        logs.append(payload_logging("SUCCESS", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, script, time_of_injection, time_of_success, payload_file, 'nil'))

                    except TimeoutException:
                        logs.append(payload_logging("FAILURE", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, script, time_of_injection, 'nil', payload_file, 'nil'))


                        # 2) Check for alerts in example after refreshing extension
                        driver.switch_to.window(extension)
                        driver.refresh()
                        driver.switch_to.window(example)
                        # driver.save_screenshot('DYNAMIC_ANALYSIS/ss.png')

                        try:
                            # wait 2 seconds to see if alert is detected
                            WebDriverWait(driver, 2).until(EC.alert_is_present())
                            alert = driver.switch_to.alert
                            alert.accept()

                            time_of_success = dt.utcnow()
                            logs.append(payload_logging("SUCCESS", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, script, time_of_injection, time_of_success, payload_file, 'nil'))

                        except TimeoutException:
                            logs.append(payload_logging("FAILURE", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, script, time_of_injection, 'nil', payload_file, 'nil'))

                    # check for any modifications (snapshot back to original)
                    try: 
                        # [1] check modifications for example.com
                        driver.switch_to.window(example)
                        if example_source_code != driver.page_source:
                            driver.get(website)
                            # print(f"Navigated back to '{website}' due to page source changes")

                    except Exception as e:
                        pass

                    try: 
                        # [2] check modifications for extension
                        driver.switch_to.window(extension)
                        if extension_source_code != driver.page_source:
                            driver.get(url_path)
                            # print(f"Navigated back to '{url_path}' due to extension page source changes")

                    except Exception as e:
                        pass


        except TimeoutException:
            # Handle TimeoutException when title condition is not met
            error_logging(source, f'Failed to resolve {website}')

        except Exception as e:
            error_logging(source, str(e))
    
        return logs

    source = result['taintsource']
    if 'selectionText' in result['taintsource']:
        return context_menu_selectionText_N(args_tuple)
    elif 'linkUrl' in result['taintsource']:
        return ontext_menu_link_url_N(args_tuple)
    elif 'srcUrl' in result['taintsource']:
        return context_menu_src_url_N(args_tuple)
    elif 'frameUrl' in result['taintsource']:
        return context_menu_frame_url_N(args_tuple)
    elif 'pageUrl' in result['taintsource']:
        return context_menu_pageUrl_N(args_tuple)
    else:
        progress_bar.update(len(payloads))
        return []

# combined chromeTabQuery
def chromeTabQuery(args_tuple):
    progress_bar, order, option, payloads, url_path, ext_id, ext_name, payload_file, result, server_payloads = args_tuple

    # new chromeTabsQuery.title (works)
    def chromeTabsQuery_title_N(args_tuple):
        progress_bar, order, option, payloads, url_path, ext_id, ext_name, payload_file, result, server_payloads = args_tuple

        logs = []
        source = 'chromeTabsQuery.title'

        url_of_injection_example = 'https://www.example.com'
        

        driver = Chrome(service=Service(), options=option)

        try:
            # get www.example.com
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

            for payload in payloads:

                # update progress bar
                progress_bar.update(1) 

                # change to example.com to change document.title property
                driver.switch_to.window(example)
                driver.refresh()

                try:
                    driver.execute_script(f'document.title = `{payload}`;')

                    # get time of injection
                    time_of_injection = dt.utcnow()

                except Exception as e:
                    error_logging(source, str(e))
                    continue

                # observe behavior after payload injection
                # 1) Check for alerts in example
                driver.switch_to.window(example)
                try:
                    # wait 2 seconds to see if alert is detected
                    WebDriverWait(driver, 2).until(EC.alert_is_present())
                    alert = driver.switch_to.alert
                    alert.accept()

                    time_of_success = dt.utcnow()
                    logs.append(payload_logging("SUCCESS", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, r"document.title = `{payload}`;", time_of_injection, time_of_success, payload_file, 'nil'))

                except TimeoutException:
                    logs.append(payload_logging("FAILURE", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, r"document.title = `{payload}`;", time_of_injection, 'nil', payload_file, 'nil'))

                    # 2) Check for alerts in example after refreshing extension
                    driver.switch_to.window(extension)
                    driver.refresh()
                    driver.switch_to.window(example)

                    try:
                        # wait 2 seconds to see if alert is detected
                        WebDriverWait(driver, 2).until(EC.alert_is_present())
                        alert = driver.switch_to.alert
                        alert.accept()

                        time_of_success = dt.utcnow()
                        logs.append(payload_logging("SUCCESS", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, r"document.title = `{payload}`;", time_of_injection, time_of_success, payload_file, 'nil'))

                    except TimeoutException:
                        logs.append(payload_logging("FAILURE", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, r"document.title = `{payload}`;", time_of_injection, 'nil', payload_file, 'nil'))


                try: 
                    # check modifications for example.com
                    driver.switch_to.window(example)
                    if example_source_code != driver.page_source:
                        driver.get("https://www.example.com")
                        # print("Navigated back to 'https://www.example.com' due to page source changes")
                except:
                    pass


                try: 
                    # check modifications for extension
                    driver.switch_to.window(extension)
                    if extension_source_code != driver.page_source:
                        driver.get(url_path)
                        # print(f"Navigated back to '{url_path}' due to extension page source changes")
                except:
                    pass


        except TimeoutException:
            error_logging(source, f'Failed to resolve https://www.example.com')

        except Exception as e:
            # Handle any other exceptions that occur
            error_logging(source, str(e))

        return logs

    # new chromeTabQuery.url (works)
    def chromeTabQuery_url_N(args_tuple):
        progress_bar, order, option, payloads, url_path, ext_id, ext_name, payload_file, result, server_payloads = args_tuple

        logs = []
        source = 'chromeTabQuery.url'

        url_of_injection_example = 'https://www.example.com'
        

        driver = Chrome(service=Service(), options=option)

        # Case Secnario for chromeTabQuery_url_new
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


            for payload in payloads:

                # update progress bar
                progress_bar.update(1) 


                payload = payload.strip()

                # change to example.com to change url property
                driver.switch_to.window(example)
                try:
                    driver.execute_script(f"location.href = `https://www.example.com/?p={payload}`")

                    # get time of injection
                    time_of_injection = dt.utcnow()

                except Exception as e:
                    error_logging(source, str(e))
                    continue

                # observe behavior after payload injection
                # 1) Check for alerts in example
                # driver.save_screenshot('DYNAMIC_ANALYSIS/ss.png')
                try:
                    # wait 2 seconds to see if alert is detected
                    WebDriverWait(driver, 2).until(EC.alert_is_present())
                    alert = driver.switch_to.alert
                    alert.accept()

                    time_of_success = dt.utcnow()
                    logs.append(payload_logging("SUCCESS", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, r"location.href = `https://www.example.com/?p={payload}`",time_of_injection, time_of_success, payload_file, 'nil'))
                
                except TimeoutException:
                    logs.append(payload_logging("FAILURE", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, r"location.href = `https://www.example.com/?p={payload}`",time_of_injection, 'nil', payload_file, 'nil'))

                    # 2) Check for alerts in example after refreshing extension
                    driver.switch_to.window(extension)
                    driver.refresh()
                    driver.switch_to.window(example)
                
                    try:
                        # wait 2 seconds to see if alert is detected
                        WebDriverWait(driver, 2).until(EC.alert_is_present())
                        alert = driver.switch_to.alert
                        alert.accept()

                        time_of_success = dt.utcnow()
                        logs.append(payload_logging("SUCCESS", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, r"location.href = `https://www.example.com/?p={payload}`",time_of_injection, time_of_success, payload_file, 'nil'))

                    except TimeoutException:
                        logs.append(payload_logging("FAILURE", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, r"location.href = `https://www.example.com/?p={payload}`",time_of_injection, 'nil', payload_file, 'nil'))


                try: 
                    # check modifications for example.com
                    driver.switch_to.window(example)
                    if example_source_code != driver.page_source:
                        driver.get("https://www.example.com")
                        # print("Navigated back to 'https://www.example.com' due to page source changes")

                except:
                    pass

                try: 
                    # check modifications for extension
                    driver.switch_to.window(extension)
                    if extension_source_code != driver.page_source:
                        driver.get(url_path)
                        # print(f"Navigated back to '{url_path}' due to extension page source changes")

                except:
                    pass


        except TimeoutException:
            # Handle TimeoutException when title condition is not met
            # print("Timeout: Title was not resolved to 'Example Domain'")
            error_logging(source, f'Failed to resolve https://www.example.com')

        except Exception as e:
            error_logging(source, str(e))

        return logs

    # new chromeTabQuery.favIconUrl (works)
    def chromeTabQuery_favIconUrl_N(args_tuple):

        progress_bar, order, option, payloads, url_path, ext_id, ext_name, payload_file, result, server_payloads = args_tuple

        logs = []
        source = 'chromeTabsQuery.favIconUrl'

        url_of_injection_example = 'DYNAMIC_ANALYSIS/miscellaneous/xss_website.html'
        


        driver = Chrome(service=Service(), options=option)
        dir_path = Path(f'DYNAMIC_ANALYSIS/miscellaneous/ChromeTabQueryFiles/favIconUrl_instance_{order}')

        def create_directory():
            nonlocal dir_path
            if not dir_path.exists():
                os.makedirs(dir_path)
                return True  # Directory was created
            else:
                return False  # Directory already existed
            
        def copy_picture_to_directory(picture_path, directory):
            shutil.copy(picture_path, directory)

        def access_directory():
            nonlocal dir_path
            pic_path = Path('DYNAMIC_ANALYSIS/miscellaneous/default.png')  # Specify the path of the picture you want to copy

            if create_directory():
                if pic_path.exists():
                    copy_picture_to_directory(pic_path, dir_path)
                
        def rename_file_with_payloads(payload):
            nonlocal dir_path
            payload = payload.strip()
            dir_list = tuple(dir_path.glob("*.*"))
            if not len(dir_list) == 1:
                return
            dir_list[0].rename(dir_path.joinpath(payload + ".png"))

        def changeFavIconUrl(driver, order ,payload):
            payload = payload.strip()

            try:
                # remove current favIconUrl
                driver.execute_script("""
                var linkElement = document.querySelector('link[rel="icon"]');
                if (linkElement) {
                linkElement.parentNode.removeChild(linkElement);
                }
                """)
            except Exception as e:
                error_logging(source, str(e))

            try:
                # set new favIconUrl
                driver.execute_script(f"""
                var link = document.createElement('link');
                link.type = 'image/jpg';
                link.rel = 'icon';
                link.href = './ChromeTabQueryFiles/favIconUrl_instance_{order}/{payload}.png';
                document.head.appendChild(link);
                """)


            except Exception as e:
                error_logging(source, str(e))

        # preconfigure files required
        access_directory()
        
        try:
            website = 'file://' + os.path.abspath(url_of_injection_example)

            # get www.example.com
            driver.get(website)
            # set handler for example.com
            example = driver.current_window_handle

            # Wait up to 5 seconds for the title to become "Example Domain"
            title_condition = EC.title_is('Xss Website')
            WebDriverWait(driver, 5).until(title_condition)

            # get page source code of example.com
            example_source_code = driver.page_source

            # add a default favIconUrl
            driver.execute_script("""
            var link = document.createElement('link');
            link.type = 'image/jpg';
            link.rel = 'icon';
            link.href = 'default.png';
            document.head.appendChild(link);
            """)

            # get extension popup.html
            driver.switch_to.new_window('tab')
            extension = driver.current_window_handle
            driver.get(url_path)

            # get page source code of extension
            extension_source_code = driver.page_source

            for payload in payloads:

                # update progress bar
                progress_bar.update(1) 

                # forbidden_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|', "'"]
                forbidden_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
                # skip payloads that contain forbidden_chars
                if any(char in payload for char in forbidden_chars):
                    continue

                driver.switch_to.window(example)
                try: 
                    # change filename to payloads
                    rename_file_with_payloads(payload)

                    # use filename as payload in ext
                    changeFavIconUrl(driver, order, payload)

                    # get time of injection
                    time_of_injection = dt.utcnow()
                except Exception as e:
                    error_logging(source, str(e))
                    continue

                driver.switch_to.window(example)
                # observe behavior after payload injection
                # 1) Check for alerts in example.com
                try:
                    # wait 2 seconds to see if alert is detected
                    WebDriverWait(driver, 2).until(EC.alert_is_present())
                    alert = driver.switch_to.alert
                    alert.accept()

                    time_of_success = dt.utcnow()
                    logs.append(payload_logging("SUCCESS", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, r"var link = document.createElement('link');link.type = 'image/jpg';link.rel = 'icon';link.href = './ChromeTabQueryFiles/favIconUrl_instance_{number}/{payload}.png';document.head.appendChild(link);",time_of_injection, time_of_success, payload_file, 'nil'))

                except TimeoutException:
                    logs.append(payload_logging("FAILURE", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, r"var link = document.createElement('link');link.type = 'image/jpg';link.rel = 'icon';link.href = './ChromeTabQueryFiles/favIconUrl_instance_{number}/{payload}.png';document.head.appendChild(link);",time_of_injection, 'nil', payload_file, 'nil'))

                    # 2) Check for alerts in example after refreshing extension
                    driver.switch_to.window(extension)
                    driver.refresh()
                    driver.switch_to.window(example)

                    try:
                        # wait 2 seconds to see if alert is detected
                        WebDriverWait(driver, 2).until(EC.alert_is_present())
                        alert = driver.switch_to.alert
                        alert.accept()

                        time_of_success = dt.utcnow()
                        logs.append(payload_logging("SUCCESS", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, r"var link = document.createElement('link');link.type = 'image/jpg';link.rel = 'icon';link.href = './ChromeTabQueryFiles/favIconUrl_instance_{number}/{payload}.png';document.head.appendChild(link);",time_of_injection, time_of_success, payload_file, 'nil'))

                    except TimeoutException:
                        logs.append(payload_logging("FAILURE", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, r"var link = document.createElement('link');link.type = 'image/jpg';link.rel = 'icon';link.href = './ChromeTabQueryFiles/favIconUrl_instance_{number}/{payload}.png';document.head.appendChild(link);",time_of_injection, 'nil', payload_file, 'nil'))


                # check for modifications in example 
                try: 
                    # check modifications for example.com
                    driver.switch_to.window(example)
                    if example_source_code != driver.page_source:
                        driver.get(website)
                        # print("Navigated back to 'xss_website.html' due to page source changes")
                except:
                    pass

                try: 
                    # check modifications for extension
                    driver.switch_to.window(extension)
                    if extension_source_code != driver.page_source:
                        driver.get(url_path)
                        # print(f"Navigated back to '{url_path}' due to extension page source changes")
                except:
                    pass

        except TimeoutException:
            # Handle TimeoutException when title condition is not met
            error_logging(source, f'Failed to resolve {website}')
            pass

        except Exception as e:
            # Handle any other exceptions that occur
            error_logging(source, str(e))

        return logs

    source = result['taintsource']
    if 'title' in result['taintsource']:
        return chromeTabsQuery_title_N(args_tuple)
    elif 'faviconUrl' in result['taintsource']:
        return chromeTabQuery_favIconUrl_N(args_tuple)
    elif 'url' in result['taintsource']:
        return chromeTabQuery_url_N(args_tuple)
    else:
        progress_bar.update(len(payloads))
        return []

# new location.search (works)
def locationSearch_N(args_tuple):
    progress_bar, order, option, payloads, url_path, ext_id, ext_name, payload_file, result, server_payloads = args_tuple

    logs = []
    source = 'location.search'
    url_of_injection_example = 'https://www.example.com'
    

    driver = Chrome(service=Service(), options=option)

    try:
        # navigate to example.com
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
        driver.get(url_path)
        extension = driver.current_window_handle

        # get page source code of extension
        extension_source_code = driver.page_source

        for payload in payloads:

            # update progress bar
            progress_bar.update(1) 

            # define a query parameter
            driver.switch_to.window(example)

            try:
                driver.execute_script(f'window.location.search=`?q={payload}`')

                # get time of injection
                time_of_injection = dt.utcnow()
            except Exception as e:
                error_logging(source, str(e))
                continue

            # 1) Check for alerts in example
            try:
                # wait 2 seconds to see if alert is detected
                WebDriverWait(driver, 2).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert.accept()

                time_of_success = dt.utcnow()
                logs.append(payload_logging("SUCCESS", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, r"window.location.search=`?q={payload}`", time_of_injection, time_of_success, payload_file, 'nil'))
            
            except TimeoutException:
                logs.append(payload_logging("FAILURE", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, r"window.location.search=`?q={payload}`", time_of_injection, 'nil', payload_file, 'nil'))

                # 2) Check for alerts in example after refreshing extension

                driver.switch_to.window(extension)
                driver.refresh()
                driver.switch_to.window(example)

                try:
                    # wait 2 seconds to see if alert is detected
                    WebDriverWait(driver, 2).until(EC.alert_is_present())
                    alert = driver.switch_to.alert
                    alert.accept()

                    time_of_success = dt.utcnow()
                    logs.append(payload_logging("SUCCESS", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, r"window.location.search=`?q={payload}`", time_of_injection, time_of_success, payload_file, 'nil'))
                except TimeoutException:
                    logs.append(payload_logging("FAILURE", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, r"window.location.search=`?q={payload}`", time_of_injection, 'nil', payload_file, 'nil'))


            try: 
                # check modifications for example.com
                driver.switch_to.window(example)
                if example_source_code != driver.page_source:
                    driver.get("https://www.example.com")
                    # print("Navigated back to 'https://www.example.com' due to page source changes")

            except:
                pass

            try: 
                # check modifications for extension
                driver.switch_to.window(extension)
                if extension_source_code != driver.page_source:
                    driver.get(url_path)
                    # print(f"Navigated back to '{url_path}' due to extension page source changes")

            except:
                pass


    except TimeoutException:
        error_logging(source, f'Failed to resolve https://www.example.com')
        pass

    except Exception as e:
        error_logging(source, str(e))

    return logs

# combined chromeDebugger
def chromeDebugger(args_tuple):
    progress_bar, order, option, payloads, url_path, ext_id, ext_name, payload_file, result, server_payloads = args_tuple

    # new chrome.Debugger.GetTargets (works)
    def chromeDebugger_title_N(args_tuple):
        progress_bar, order, option, payloads, url_path, ext_id, ext_name, payload_file, result, server_payloads = args_tuple

        logs = []
        source = 'chromeDebugger.GetTargets.title'

        url_of_injection_example = 'https://www.example.com'
        

        driver = Chrome(service=Service(), options=option)

        try:
            website = 'https://www.example.com'

            # navigate to example.com
            driver.get(website)
            # set handler for example.com
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

                # update progress bar
                progress_bar.update(1) 

                # change to example.com to change document.title property
                driver.switch_to.window(example)
                driver.refresh()    

                try:
                    driver.execute_script(f'document.title = `{payload}`;')

                    # get time of injection
                    time_of_injection = dt.utcnow()

                except Exception as e:
                    error_logging(source, str(e))
                    continue


                try:
                    # Press the F12 key to open the developer tools
                    subprocess.call(['xdotool', 'keydown', 'F12'])
                    subprocess.call(['xdotool', 'keyup', 'F12'])
                except Exception as e:
                    error_logging(source, str(e))
                    continue


                # observe behavior after payload injection
                # 1) Check for alerts in example.com
                driver.switch_to.window(example)
                try:
                    # wait 2 seconds to see if alert is detected
                    WebDriverWait(driver, 2).until(EC.alert_is_present())
                    alert = driver.switch_to.alert
                    alert.accept()

                    time_of_success = dt.utcnow()
                    logs.append(payload_logging("SUCCESS", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, r"document.title = `{payload}`;",time_of_injection, time_of_success, payload_file, 'nil'))

                except TimeoutException:
                    logs.append(payload_logging("FAILURE", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, r"document.title = `{payload}`;",time_of_injection, 'nil', payload_file, 'nil'))


                    # 2) Check for alerts in example after refreshing extension
                    driver.switch_to.window(extension)
                    driver.refresh()
                    driver.switch_to.window(example)

                    try:
                        # wait 2 seconds to see if alert is detected
                        WebDriverWait(driver, 2).until(EC.alert_is_present())
                        alert = driver.switch_to.alert
                        alert.accept()

                        time_of_success = dt.utcnow()
                        logs.append(payload_logging("SUCCESS", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, r"document.title = `{payload}`;",time_of_injection, time_of_success, payload_file, 'nil'))

                    except TimeoutException:
                        logs.append(payload_logging("FAILURE", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, r"document.title = `{payload}`;",time_of_injection, 'nil', payload_file, 'nil'))
                        
                    
                try: 
                    # [1] check modifications for example.com
                    driver.switch_to.window(example)
                    if example_source_code != driver.page_source:
                        driver.get(website)
                        # print(f"Navigated back to '{website}' due to page source changes")

                except Exception as e:
                    pass

                try: 
                    # [2] check modifications for extension
                    driver.switch_to.window(extension)
                    if extension_source_code != driver.page_source:
                        driver.get(url_path)
                        # print(f"Navigated back to '{url_path}' due to extension page source changes")

                except Exception as e:
                    pass

        except TimeoutException:
            # Handle TimeoutException when title condition is not met
            error_logging(source, f'Failed to resolve https://www.example.com')
            

        except Exception as e:
            error_logging(source, str(e))

        return logs

    # new chrome.Debugger.GetTargets (works, but loaded extension first instead of browser)
    def chromeDebugger_title_N_EXT_FIRST(args_tuple):
        progress_bar, order, option, payloads, url_path, ext_id, ext_name, payload_file, result, server_payloads = args_tuple

        logs = []
        source = 'chromeDebugger.GetTargets.title'

        url_of_injection_example = 'https://www.example.com'
        

        driver = Chrome(service=Service(), options=option)

        try:
            website = 'https://www.example.com'

            driver.get(url_path)
            extension = driver.current_window_handle
            extension_source_code = driver.page_source

            driver.switch_to.new_window('tab')

            # navigate to example.com
            driver.get(website)
            example = driver.current_window_handle
            example_source_code = driver.page_source


            for payload in payloads:

                # update progress bar
                progress_bar.update(1) 

                # change to example.com to change document.title property
                driver.switch_to.window(example)
                driver.refresh()    

                try:
                    driver.execute_script(f'document.title = `{payload}`;')

                    # get time of injection
                    time_of_injection = dt.utcnow()

                except Exception as e:
                    error_logging(source, str(e))
                    continue


                # Press the F12 key to open the developer tools
                try:
                    subprocess.call(['xdotool', 'keydown', 'F12'])
                    subprocess.call(['xdotool', 'keyup', 'F12'])
                except Exception as e:
                    error_logging(source, str(e))
                    continue


                # observe behavior after payload injection
                # 1) Check for alerts in example.com
                driver.switch_to.window(example)
                try:
                    # wait 2 seconds to see if alert is detected
                    WebDriverWait(driver, 2).until(EC.alert_is_present())
                    alert = driver.switch_to.alert
                    alert.accept()

                    time_of_success = dt.utcnow()
                    logs.append(payload_logging("SUCCESS", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, r"document.title = `{payload}`;",time_of_injection, time_of_success, payload_file, 'nil'))

                except TimeoutException:
                    logs.append(payload_logging("FAILURE", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, r"'document.title = `{payload}`;'",time_of_injection, 'nil', payload_file, 'nil'))

                    # 2) Check for alerts in example after refreshing extension
                    driver.switch_to.window(extension)
                    driver.refresh()
                    driver.switch_to.window(example)

                    try:
                        # wait 2 seconds to see if alert is detected
                        WebDriverWait(driver, 2).until(EC.alert_is_present())
                        alert = driver.switch_to.alert
                        alert.accept()

                        time_of_success = dt.utcnow()
                        logs.append(payload_logging("SUCCESS", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, r"document.title = `{payload}`;",time_of_injection, time_of_success, payload_file, 'nil'))

                    except TimeoutException:
                        logs.append(payload_logging("FAILURE", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, r"'document.title = `{payload}`;'",time_of_injection, 'nil', payload_file, 'nil'))
                        

                try: 
                    # [1] check modifications for example.com
                    driver.switch_to.window(example)
                    if example_source_code != driver.page_source:
                        driver.get(website)
                        # print(f"Navigated back to '{website}' due to page source changes")

                except Exception as e:
                    # print('Error: ', str(e))
                    pass

                try: 
                    # [2] check modifications for extension
                    driver.switch_to.window(extension)
                    if extension_source_code != driver.page_source:
                        driver.get(url_path)
                        # print(f"Navigated back to '{url_path}' due to extension page source changes")

                except Exception as e:
                    # print('Error: ', str(e))
                    pass

        except TimeoutException:
            # Handle TimeoutException when title condition is not met
            error_logging(source, f'Failed to resolve https://www.example.com')

        except Exception as e:
            # Handle any other exceptions that occur
            error_logging(source, str(e))

        return logs

    # new chrome.Debugger.GetTargets (works)
    def chromeDebugger_url_N(args_tuple):
        progress_bar, order, option, payloads, url_path, ext_id, ext_name, payload_file, result, server_payloads = args_tuple

        logs = []
        source = 'chromeTabQuery.url'

        url_of_injection_example = 'https://www.example.com'
        

        driver = Chrome(service=Service(), options=option)
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

            for payload in payloads:

                # update progress bar
                progress_bar.update(1) 

                payload = payload.strip()


                # change to example.com to change url property
                driver.switch_to.window(example)
                driver.refresh()

                try:
                    driver.execute_script(f"location.href = `https://www.example.com/?p={payload}`")

                    # get time of injection
                    time_of_injection = dt.utcnow()

                except Exception as e:
                    error_logging(source, str(e))
                    continue

                # Press the F12 key to open the developer tools
                try:
                    subprocess.call(['xdotool', 'keydown', 'F12'])
                    subprocess.call(['xdotool', 'keyup', 'F12'])
                except Exception as e:
                    error_logging(source, str(e))
                    continue



                # observe behavior after payload injection
                # 1) Check for alerts in example
                # driver.save_screenshot('DYNAMIC_ANALYSIS/ss.png')
                try:
                    # wait 2 seconds to see if alert is detected
                    WebDriverWait(driver, 2).until(EC.alert_is_present())
                    alert = driver.switch_to.alert
                    alert.accept()

                    time_of_success = dt.utcnow()
                    logs.append(payload_logging("SUCCESS", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, r"location.href = `https://www.example.com/?p={payload}`",time_of_injection, time_of_success, payload_file, 'nil'))
                
                except TimeoutException:
                    logs.append(payload_logging("FAILURE", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, r"location.href = `https://www.example.com/?p={payload}`",time_of_injection, 'nil', payload_file, 'nil'))

                    # 2) Check for alerts in example after refreshing extension
                    driver.switch_to.window(extension)
                    driver.refresh()
                    driver.switch_to.window(example)
                
                    try:
                        # wait 2 seconds to see if alert is detected
                        WebDriverWait(driver, 2).until(EC.alert_is_present())
                        alert = driver.switch_to.alert
                        alert.accept()

                        time_of_success = dt.utcnow()
                        logs.append(payload_logging("SUCCESS", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, r"location.href = `https://www.example.com/?p={payload}`",time_of_injection, time_of_success, payload_file, 'nil'))

                    except TimeoutException:
                        logs.append(payload_logging("FAILURE", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, r"location.href = `https://www.example.com/?p={payload}`",time_of_injection, 'nil', payload_file, 'nil'))


                try: 
                    # check modifications for example.com
                    driver.switch_to.window(example)
                    if example_source_code != driver.page_source:
                        driver.get("https://www.example.com")
                        # print("Navigated back to 'https://www.example.com' due to page source changes")

                except:
                    pass

                try: 
                    # check modifications for extension
                    driver.switch_to.window(extension)
                    if extension_source_code != driver.page_source:
                        driver.get(url_path)
                        # print(f"Navigated back to '{url_path}' due to extension page source changes")

                except:
                    pass



        except TimeoutException:
            # Handle TimeoutException when title condition is not met
            error_logging(source, f'Failed to resolve https://www.example.com')

        except Exception as e:
            # Handle any other exceptions that occur
            error_logging(source, str(e))
        return logs

    # new chromeDebugger_favIconUrl (works)
    def chromeDebugger_favIconUrl_N(args_tuple):
        
        progress_bar, order, option, payloads, url_path, ext_id, ext_name, payload_file, result, server_payloads = args_tuple

        logs = []
        source = 'chromeTabsQuery.favIconUrl'

        url_of_injection_example = 'DYNAMIC_ANALYSIS/miscellaneous/xss_website.html'
        

        driver = Chrome(service=Service(), options=option)
        dir_path = Path(f'DYNAMIC_ANALYSIS/miscellaneous/chromeDebuggerFiles/favIconUrl_instance_{order}')


        def create_directory():
            nonlocal dir_path
            if not dir_path.exists():
                os.makedirs(dir_path)
                return True  # Directory was created
            else:
                return False  # Directory already existed
            
        def copy_picture_to_directory(picture_path, directory):
            shutil.copy(picture_path, directory)

        def access_directory():
            nonlocal dir_path
            pic_path = Path('DYNAMIC_ANALYSIS/miscellaneous/default.png')  # Specify the path of the picture you want to copy
            if create_directory():
                if pic_path.exists():
                    copy_picture_to_directory(pic_path, dir_path)
                
        def rename_file_with_payloads(payload):
            nonlocal dir_path
            payload = payload.strip()

            dir_list = tuple(dir_path.glob("*.*"))
            if not len(dir_list) == 1:
                return
            dir_list[0].rename(dir_path.joinpath(payload + ".png"))

        def changeFavIconUrl(driver, order ,payload):
            payload = payload.strip()

            try:
                # remove current favIconUrl
                driver.execute_script("""
                var linkElement = document.querySelector('link[rel="icon"]');
                if (linkElement) {
                linkElement.parentNode.removeChild(linkElement);
                }
                """)
            except Exception as e:
                error_logging(source, str(e))

            try:
                # set new favIconUrl
                driver.execute_script(f"""
                var link = document.createElement('link');
                link.type = 'image/jpg';
                link.rel = 'icon';
                link.href = './chromeDebuggerFiles/favIconUrl_instance_{order}/{payload}.png';
                document.head.appendChild(link);
                """)


            except Exception as e:
                error_logging(source, str(e))

        # preconfigure files required
        access_directory()

        try:
            website = 'file://' + os.path.abspath(url_of_injection_example)

            # get www.example.com
            driver.get(website)
            driver.save_screenshot('DYNAMIC_ANALYSIS/ss.png')
            # set handler for example.com
            example = driver.current_window_handle

            # Wait up to 5 seconds for the title to become "Example Domain"
            title_condition = EC.title_is('Xss Website')
            WebDriverWait(driver, 5).until(title_condition)

            # get page source code of example.com
            example_source_code = driver.page_source

            # add a default favIconUrl
            driver.execute_script("""
            var link = document.createElement('link');
            link.type = 'image/jpg';
            link.rel = 'icon';
            link.href = 'default.png';
            document.head.appendChild(link);
            """)

            # get extension popup.html
            driver.switch_to.new_window('tab')
            extension = driver.current_window_handle
            driver.get(url_path)

            # get page source code of extension
            extension_source_code = driver.page_source

            for payload in payloads:

                # update progress bar
                progress_bar.update(1) 

                # forbidden_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|', "'"]
                forbidden_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
                # skip payloads that contain forbidden_chars
                if any(char in payload for char in forbidden_chars):
                    continue

                driver.switch_to.window(example)
                try: 
                    # change filename to payloads
                    rename_file_with_payloads(payload)

                    # use filename as payload in ext
                    changeFavIconUrl(driver, order, payload)

                    # get time of injection
                    time_of_injection = dt.utcnow()
                except Exception as e:
                    error_logging(source, str(e))
                    continue


                try:
                    # Press the F12 key to open the developer tools
                    subprocess.call(['xdotool', 'keydown', 'F12'])
                    subprocess.call(['xdotool', 'keyup', 'F12'])
                except Exception as e:
                    error_logging(source, str(e))

                # observe behavior after payload injection
                # 1) Check for alerts in example.com
                driver.switch_to.window(example)
                try:
                    # wait 2 seconds to see if alert is detected
                    WebDriverWait(driver, 2).until(EC.alert_is_present())
                    alert = driver.switch_to.alert
                    alert.accept()

                    time_of_success = dt.utcnow()
                    logs.append(payload_logging("SUCCESS", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, r"var link = document.createElement('link');link.type = 'image/jpg';link.rel = 'icon';link.href'./chromeDebuggerFiles/favIconUrl_instance_{number}/{payload}.png';document.head.appendChild(link);", time_of_injection, time_of_success, payload_file, 'nil'))

                except TimeoutException:
                    logs.append(payload_logging("FAILURE", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, r"var link = document.createElement('link');link.type = 'image/jpg';link.rel = 'icon';link.href'./chromeDebuggerFiles/favIconUrl_instance_{number}/{payload}.png';document.head.appendChild(link);", time_of_injection, 'nil', payload_file, 'nil'))

                    # 2) Check for alerts in example after refreshing extension
                    driver.switch_to.window(extension)
                    driver.refresh()
                    driver.switch_to.window(example)

                    try:
                        # wait 2 seconds to see if alert is detected
                        WebDriverWait(driver, 2).until(EC.alert_is_present())
                        alert = driver.switch_to.alert
                        alert.accept()

                        time_of_success = dt.utcnow()
                        logs.append(payload_logging("SUCCESS", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, r"var link = document.createElement('link');link.type = 'image/jpg';link.rel = 'icon';link.href'./chromeDebuggerFiles/favIconUrl_instance_{order}/{payload}.png';document.head.appendChild(link);", time_of_injection, time_of_success, payload_file, 'nil'))

                    except TimeoutException:
                        logs.append(payload_logging("FAILURE", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, r"var link = document.createElement('link');link.type = 'image/jpg';link.rel = 'icon';link.href'./chromeDebuggerFiles/favIconUrl_instance_{order}/{payload}.png';document.head.appendChild(link);", time_of_injection, 'nil', payload_file, 'nil'))


                # check for modifications in example 
                try: 
                    # check modifications for example.com
                    driver.switch_to.window(example)
                    if example_source_code != driver.page_source:
                        driver.get(website)
                        # print("Navigated back to 'xss_website.html' due to page source changes")
                except:
                    pass

                try: 
                    # check modifications for extension
                    driver.switch_to.window(extension)
                    if extension_source_code != driver.page_source:
                        driver.get(url_path)
                        # print(f"Navigated back to '{url_path}' due to extension page source changes")
                except:
                    pass

        except TimeoutException:
            # Handle TimeoutException when title condition is not met
            error_logging(source, f'Failed to resolve {website}')

        except Exception as e:
            # Handle any other exceptions that occur
            error_logging(source, str(e))

        return logs

    source = result['taintsource']
    if 'title' in result['taintsource']:
        return chromeDebugger_title_N(args_tuple)
    elif 'favIconUrl' in result['taintsource']:
        return chromeDebugger_favIconUrl_N(args_tuple)
    elif 'url' in result['taintsource']:
        return chromeDebugger_url_N(args_tuple)
    else:
        progress_bar.update(len(payloads))
        return []

# new window.addEventListernerMessage (shd work (old ver))
def windowAddEventListenerMessage(args_tuple):
    progress_bar, order, option, payloads, url_path, ext_id, ext_name, payload_file, result, server_payloads = args_tuple


    logs = []
    source = "window.addEventListerner('message')"
    url_of_injection_example = 'DYNAMIC_ANALYSIS/miscellaneous/xss_website.html'
    

    driver = Chrome(service=Service(), options=option)

    try:
        website = 'file://' + os.path.abspath(url_of_injection_example)

        # get www.example.com
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
            progress_bar.update(1)

            driver.switch_to.window(example)
            driver.refresh()


            try:
                payload = payload.strip()
                taintsink = result["sink"]
                obj = {}
                script = nomagic(taintsink,payload,obj)

                driver.execute_script(f"window.postMessage({script},'*')")
                
                # get time of injection
                time_of_injection = dt.utcnow()
            except Exception as e:
                error_logging(source, str(e))
                
                try:
                    driver.execute_script(f"window.postMessage(`{payload}`,'*')")
                    # get time of injection
                    time_of_injection = dt.utcnow()
                except Exception as e:
                    error_logging(source, str(e))
                    continue

            # observe behavior after payload injection
            # check for alerts in example
            try:
                # wait 2 seconds to see if alert is detected
                WebDriverWait(driver, 2).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert.accept()
                # print('[example] + Alert Detected +')

                # get time of success [1) example]
                time_of_success = dt.utcnow()
                logs.append(payload_logging("SUCCESS", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, r"window.postMessage({payload},'*')", time_of_injection, time_of_success, payload_file, 'nil'))
            
            except TimeoutException:
                # print('[example] = No alerts detected =')
                logs.append(payload_logging("FAILURE", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, r"window.postMessage({payload},'*')", time_of_injection, 'nil', payload_file, 'nil'))


                # 2) Check for alerts in example after refreshing extension
                driver.switch_to.window(extension)
                driver.refresh()
                driver.switch_to.window(example)


                try:
                    # wait 2 seconds to see if alert is detected
                    WebDriverWait(driver, 2).until(EC.alert_is_present())
                    alert = driver.switch_to.alert
                    alert.accept()
                    # print('[example] + Alert Detected +')

                    # get time of success [3) example]
                    time_of_success = dt.utcnow()
                    logs.append(payload_logging("SUCCESS", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, r"window.postMessage({payload},'*')", time_of_injection, time_of_success, payload_file, 'nil'))
                except TimeoutException:
                    # print('[example] = No alerts detected =')
                    logs.append(payload_logging("FAILURE", source, ext_id, ext_name, url_of_injection_example, 'normal', payload, r"window.postMessage({payload},'*')", time_of_injection, 'nil', payload_file, 'nil'))

            try: 
                # check modifications for example.com
                driver.switch_to.window(example)
                if example_source_code != driver.page_source:
                    driver.get(website)
                    # print("Navigated back to 'https://www.example.com' due to page source changes")
            except Exception as e:
                error_logging(source, str(e))
                
            try: 
                # check modifications for extension
                driver.switch_to.window(extension)
                if extension_source_code != driver.page_source:
                    driver.get(url_path)
                    # print(f"Navigated back to '{url_path}' due to extension page source changes")
            except Exception as e:
                error_logging(source, str(e))

    except TimeoutException:
        # Handle TimeoutException when title condition is not met
        error_logging(source, f'Failed to resolve {website}')

    except Exception as e:
        error_logging(source, str(e))

    return logs









