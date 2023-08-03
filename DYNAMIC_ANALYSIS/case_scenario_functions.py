import json
import logging
import os
import shutil
import subprocess
import time
import urllib.parse
from datetime import datetime as dt
from email.utils import format_datetime as fdt
from functools import reduce
from pathlib import Path

import requests
from pytz import timezone as tz
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
    keys = chain.split(".")[1:]
    msg.update(reduce(lambda x, y: {y: x}, reversed(keys), payload))
    obj = json.dumps(msg)
    return obj


#####################
# Logging Framework #
#####################


def payload_logging(
    outcome,
    source,
    extension_id,
    extension_name,
    url_of_website,
    payload_type,
    payload,
    script,
    time_of_injection,
    time_of_alert,
    payload_filename,
    packet_info,
):
    # Get logger and timezone
    logger = logging.getLogger("dynamic")
    timezone = logger.timezone


    # Format timezone
    if time_of_injection != "nil":
        time_of_injection = fdt(time_of_injection.astimezone(tz(timezone)))
    if time_of_alert != "nil":
        time_of_alert= fdt(time_of_alert.astimezone(tz(timezone)))

    # Log
    
    logger.critical(json.dumps({
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
        "packetInfo": packet_info,
    }))


def error_logging(source, error, max_chars=200):
    # Remove newline characters from the error message
    error = error.replace("\n", " ")

    # Truncate the error message to the specified maximum characters
    error = error[:max_chars]

    # Get logger
    logger = logging.getLogger("error")

    # Log
    datetime = fdt(dt.now(tz(logger.timezone)))
    logger.error(f"[{source}] - [{datetime}] - {error}")


##########################
# Case Scenario headless #
##########################
#   Updated functions    #
####################################################################################


# 1) runtime.onMessage
def runtime_onM(args_tuple):
    (
        progress_bar,
        order,
        option,
        payloads,
        url_path,
        ext_id,
        ext_name,
        payload_file,
        result,
        server_payloads,
    ) = args_tuple


    scripts = []
    scripts_s = []
    payload = {}
    payload_s = {}
    source = "chrome.runtime.onMessage"
    url_of_injection_example = "https://www.example.com"

    for payload_no, i in enumerate(payloads[1]):
        dots = "."
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
        if msgpassword != "" and msgproperty != "":
            obj[msgproperty] = msgpassword
        if dots in taintsink:
            obj = nomagic(taintsink, i, obj)
            var = f"obj = JSON.parse('{obj}');"
        else:
            var = f"obj = '{i}';"

        script = f"{var}chrome.runtime.sendMessage(obj)"
        scripts.append(script)
        payload[payload_no] = i

    for payload_no, i in enumerate(server_payloads[1]):
        dots = "."
        taintsink = result["sink"]
        obj = {}
        var = ""
        i = i.replace(
            "mhudogbhrqrjxjxelug", f"http://127.0.0.1:8000/xss/{order}/{payload_no}"
        )
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
        if msgpassword != "" and msgproperty != "":
            obj[msgproperty] = msgpassword
        if dots in taintsink:
            obj = nomagic(taintsink, i, obj)
            var = f"obj = JSON.parse('{obj}');"
        else:
            var = f"obj = '{i}';"

        script = f"{var}chrome.runtime.sendMessage(obj)"
        scripts_s.append(script)
        payload_s[payload_no] = i

    driver = Chrome(service=Service(), options=option)

    try:
        # Navigate to example.com
        driver.get(url_of_injection_example)
        example = driver.current_window_handle

        # Wait up to 5 seconds for the title to become "Example Domain"
        title_condition = EC.title_is("Example Domain")
        WebDriverWait(driver, 5).until(title_condition)

        # get page source code of example.com
        example_source_code = driver.page_source

        # get extension popup.html
        driver.switch_to.new_window("tab")
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
                
                payload_logging(
                    "SUCCESS",
                    source,
                    ext_id,
                    ext_name,
                    url_of_injection_example,
                    "normal",
                    payload[num],
                    script,
                    time_of_injection,
                    time_of_success,
                    payload_file,
                    "nil",
                )
                
            except TimeoutException:
                # log for failed payloads                
                payload_logging(
                    "FAILURE",
                    source,
                    ext_id,
                    ext_name,
                    url_of_injection_example,
                    "normal",
                    payload[num],
                    script,
                    time_of_injection,
                    "nil",
                    payload_file,
                    "nil",
                )
                

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

        for num, script in enumerate(scripts_s):
            progress_bar.update(1)
            try:
                driver.execute_script(script)
                time_of_injection = dt.utcnow()
            except Exception as e:
                driver.refresh()
                continue
            driver.switch_to.window(example)

            try:
                if "post" in payload_s[num]:
                    a = WebDriverWait(driver, 2).until(
                        EC.element_to_be_clickable((By.ID, "a"))
                    )
                    a.click()
            except:
                pass

            url = "http://127.0.0.1:8000/data/{}/{}".format(order, payload_no)
            time.sleep(3)
            packets: list = requests.get(url).json()["data"]
            if packets != []:
                payload_logging(
                    "SUCCESS",
                    source,
                    ext_id,
                    ext_name,
                    url_of_injection_example,
                    "server",
                    payload_s[num],
                    script,
                    time_of_injection,
                    "nil",
                    payload_file,
                    packets,
                )
                
            else:
                payload_logging(
                    "FAILURE",
                    source,
                    ext_id,
                    ext_name,
                    url_of_injection_example,
                    "server",
                    payload_s[num],
                    script,
                    time_of_injection,
                    "nil",
                    payload_file,
                    packets,
                )
                

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

    


# 2) runtime.onConnect
def runtime_onC(args_tuple):
    (
        progress_bar,
        order,
        option,
        payloads,
        url_path,
        ext_id,
        ext_name,
        payload_file,
        result,
        server_payloads,
    ) = args_tuple

    
    scripts = []
    scripts_s = []
    payload = {}
    payload_s = {}
    source = "chrome.runtime.onConnect"
    url_of_injection_example = "https://www.example.com"

    for payload_no, i in enumerate(payloads[1]):
        dots = "."
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
            obj = nomagic(taintsink, i, obj)
            var = f"obj = JSON.parse('{obj}');"
        else:
            obj = i
            var = f"obj = '{obj}';"

        if port != "" and portproperty != "" and portpassword != "":
            connect = {portproperty: portpassword}
            connect = json.dumps(connect)
            var = var + f"connect=JSON.parse('{connect}')"

        func = f".postMessage(obj)"
        script = f"{var}chrome.runtime.connect(connect){func}"
        scripts.append(script)
        payload[payload_no] = i

    for payload_no, i in enumerate(server_payloads[1]):
        dots = "."
        taintsink = result["sink"]
        obj = {}
        var = ""
        func = ""
        connect = ""
        i = i.replace(
            "mhudogbhrqrjxjxelug", f"http://127.0.0.1:8000/xss/{order}/{payload_no}"
        )
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
            obj = nomagic(taintsink, i, obj)
            var = f"obj = JSON.parse('{obj}');"
        else:
            obj = i
            var = f"obj = '{obj}';"

        if port != "" and portproperty != "" and portpassword != "":
            connect = {portproperty: portpassword}
            connect = json.dumps(connect)
            var = var + f"connect=JSON.parse('{connect}')"

        func = f".postMessage(obj)"
        script = f"{var}chrome.runtime.connect(connect){func}"
        scripts_s.append(script)
        payload_s[payload_no] = i

    driver = Chrome(service=Service(), options=option)
    try:
        # Navigate to example.com
        driver.get(url_of_injection_example)
        example = driver.current_window_handle

        # Wait up to 5 seconds for the title to become "Example Domain"
        title_condition = EC.title_is("Example Domain")
        WebDriverWait(driver, 5).until(title_condition)

        # get page source code of example.com
        example_source_code = driver.page_source

        # get extension popup.html
        driver.switch_to.new_window("tab")
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
                payload_logging(
                    "SUCCESS",
                    source,
                    ext_id,
                    ext_name,
                    url_of_injection_example,
                    "normal",
                    payload[num],
                    script,
                    time_of_injection,
                    time_of_success,
                    payload_file,
                    "nil",
                )
                
            except TimeoutException:
                payload_logging(
                    "FAILURE",
                    source,
                    ext_id,
                    ext_name,
                    url_of_injection_example,
                    "normal",
                    payload[num],
                    script,
                    time_of_injection,
                    "nil",
                    payload_file,
                    "nil",
                )
                

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

        for num, script in enumerate(scripts_s):
            progress_bar.update(1)
            try:
                driver.execute_script(script)
                time_of_injection = dt.utcnow()
            except Exception as e:
                driver.refresh()
                continue
            driver.switch_to.window(example)

            try:
                if "post" in payload_s[num]:
                    a = WebDriverWait(driver, 2).until(
                        EC.element_to_be_clickable((By.ID, "a"))
                    )
                    a.click()
            except:
                pass

            url = "http://127.0.0.1:8000/data/{}/{}".format(order, payload_no)
            time.sleep(3)
            packets: list = requests.get(url).json()["data"]
            if packets != []:
                payload_logging(
                    "SUCCESS",
                    source,
                    ext_id,
                    ext_name,
                    url_of_injection_example,
                    "server",
                    payload_s[num],
                    script,
                    time_of_injection,
                    "nil",
                    payload_file,
                    packets,
                )
                
            else:
                payload_logging(
                    "FAILURE",
                    source,
                    ext_id,
                    ext_name,
                    url_of_injection_example,
                    "server",
                    payload_s[num],
                    script,
                    time_of_injection,
                    "nil",
                    payload_file,
                    packets,
                )
                

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
    


# 3) cookies.get && cookies.getAll
def cookie_get(args_tuple):
    (
        progress_bar,
        order,
        option,
        payloads,
        url_path,
        ext_id,
        ext_name,
        payload_file,
        result,
        server_payloads,
    ) = args_tuple

    
    scripts = []
    scripts_s = []
    payload = {}
    payload_s = {}
    source = "cookies.get/cookies.getAll"
    url_of_injection_example = "https://www.example.com"

    for payload_no, i in enumerate(payloads[1]):
        dots = "."
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

        script = f"document.cookie = {obj} + document.cookie"
        scripts.append(script)
        payload[payload_no] = i

    for payload_no, i in enumerate(server_payloads[1]):
        dots = "."
        taintsource = result["taintsource"]
        cookie = ""
        x = ""
        i = i.replace(
            "mhudogbhrqrjxjxelug", f"http://127.0.0.1:8000/xss/{order}/{payload_no}"
        )
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

        script = f"document.cookie = {obj} + document.cookie"
        scripts_s.append(script)
        payload_s[payload_no] = i

    driver = Chrome(service=Service(), options=option)
    try:
        # Navigate to example.com
        driver.get(url_of_injection_example)
        example = driver.current_window_handle

        # Wait up to 5 seconds for the title to become "Example Domain"
        title_condition = EC.title_is("Example Domain")
        WebDriverWait(driver, 5).until(title_condition)

        # get page source code of example.com
        example_source_code = driver.page_source

        # get extension popup.html
        driver.switch_to.new_window("tab")
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
                continue

            # check for alerts in example
            try:
                # wait 2 seconds to see if alert is detected
                WebDriverWait(driver, 2).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert.accept()

                # get time of success [1) example]
                time_of_success = dt.utcnow()
                payload_logging(
                    "SUCCESS",
                    source,
                    ext_id,
                    ext_name,
                    url_of_injection_example,
                    "normal",
                    payload[num],
                    script,
                    time_of_injection,
                    time_of_success,
                    payload_file,
                    "nil",
                )
                

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

                    # get time of success [3) example]
                    time_of_success = dt.utcnow()
                    payload_logging(
                        "SUCCESS",
                        source,
                        ext_id,
                        ext_name,
                        url_of_injection_example,
                        "normal",
                        payload[num],
                        script,
                        time_of_injection,
                        time_of_success,
                        payload_file,
                        "nil",
                    )
                    
                except TimeoutException:
                    payload_logging(
                        "FAILURE",
                        source,
                        ext_id,
                        ext_name,
                        url_of_injection_example,
                        "normal",
                        payload[num],
                        script,
                        time_of_injection,
                        "nil",
                        payload_file,
                        "nil",
                    )
                    

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

        for num, script in enumerate(scripts_s):
            progress_bar.update(1)
            driver.switch_to.window(example)
            try:
                driver.execute_script(script)
                time_of_injection = dt.utcnow()
            except Exception as e:
                driver.refresh()
                continue
            driver.switch_to.window(extension)
            driver.refresh()
            driver.switch_to.window(example)

            try:
                if "post" in payload_s[num]:
                    a = WebDriverWait(driver, 2).until(
                        EC.element_to_be_clickable((By.ID, "a"))
                    )
                    a.click()
            except:
                pass

            url = "http://127.0.0.1:8000/data/{}/{}".format(order, payload_no)
            time.sleep(3)
            packets: list = requests.get(url).json()["data"]
            if packets != []:
                payload_logging(
                    "SUCCESS",
                    source,
                    ext_id,
                    ext_name,
                    url_of_injection_example,
                    "server",
                    payload_s[num],
                    script,
                    time_of_injection,
                    "nil",
                    payload_file,
                    packets,
                )
                
            else:
                payload_logging(
                    "FAILURE",
                    source,
                    ext_id,
                    ext_name,
                    url_of_injection_example,
                    "server",
                    payload_s[num],
                    script,
                    time_of_injection,
                    "nil",
                    payload_file,
                    packets,
                )
                

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

    


# 4) location.hash
def location_hash(args_tuple):
    (
        progress_bar,
        order,
        option,
        payloads,
        url_path,
        ext_id,
        ext_name,
        payload_file,
        result,
        server_payloads,
    ) = args_tuple

    
    scripts = []
    scripts_s = []
    payload = {}
    payload_s = {}
    source = "location.hash"
    url_of_injection_example = "https://www.example.com"

    for payload_no, i in enumerate(payloads[1]):
        script = f"window.location.hash = '{i}'"
        scripts.append(script)
        payload[payload_no] = i

    for payload_no, i in enumerate(server_payloads[1]):
        i = i.replace(
            "mhudogbhrqrjxjxelug", f"http://127.0.0.1:8000/xss/{order}/{payload_no}"
        )
        script = f"window.location.hash = '{i}'"
        scripts_s.append(script)
        payload_s[payload_no] = i

    driver = Chrome(service=Service(), options=option)
    try:
        # Navigate to example.com
        driver.get(url_of_injection_example)
        example = driver.current_window_handle

        # Wait up to 5 seconds for the title to become "Example Domain"
        title_condition = EC.title_is("Example Domain")
        WebDriverWait(driver, 5).until(title_condition)

        # get page source code of example.com
        example_source_code = driver.page_source

        # get extension popup.html
        driver.switch_to.new_window("tab")
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
                driver.refresh()
                continue

            # check for alerts in example (for extension, example then payload)
            try:
                # wait 2 seconds to see if alert is detected
                WebDriverWait(driver, 2).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert.accept()
                # get time of success [1) example]
                time_of_success = dt.utcnow()
                payload_logging(
                    "SUCCESS",
                    source,
                    ext_id,
                    ext_name,
                    url_of_injection_example,
                    "normal",
                    payload[num],
                    script,
                    time_of_injection,
                    time_of_success,
                    payload_file,
                    "nil",
                )
                

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

                    # get time of success [3) example]
                    time_of_success = dt.utcnow()
                    payload_logging(
                        "SUCCESS",
                        source,
                        ext_id,
                        ext_name,
                        url_of_injection_example,
                        "normal",
                        payload[num],
                        script,
                        time_of_injection,
                        time_of_success,
                        payload_file,
                        "nil",
                    )
                    
                except TimeoutException:
                    payload_logging(
                        "FAILURE",
                        source,
                        ext_id,
                        ext_name,
                        url_of_injection_example,
                        "normal",
                        payload[num],
                        script,
                        time_of_injection,
                        "nil",
                        payload_file,
                        "nil",
                    )
                    

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

        for num, script in enumerate(scripts_s):
            progress_bar.update(1)
            driver.switch_to.window(example)
            try:
                driver.execute_script(script)
                time_of_injection = dt.utcnow()
            except Exception as e:
                driver.refresh()
                continue
            driver.switch_to.window(extension)
            driver.refresh()
            driver.switch_to.window(example)

            try:
                if "post" in payload_s[num]:
                    a = WebDriverWait(driver, 2).until(
                        EC.element_to_be_clickable((By.ID, "a"))
                    )
                    a.click()
            except:
                pass

            url = "http://127.0.0.1:8000/data/{}/{}".format(order, payload_no)
            time.sleep(3)
            packets: list = requests.get(url).json()["data"]
            if packets != []:
                payload_logging(
                    "SUCCESS",
                    source,
                    ext_id,
                    ext_name,
                    url_of_injection_example,
                    "server",
                    payload_s[num],
                    script,
                    time_of_injection,
                    "nil",
                    payload_file,
                    packets,
                )
                
            else:
                payload_logging(
                    "FAILURE",
                    source,
                    ext_id,
                    ext_name,
                    url_of_injection_example,
                    "server",
                    payload_s[num],
                    script,
                    time_of_injection,
                    "nil",
                    payload_file,
                    packets,
                )
                

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

    


#  5) runtime.onMessageExternal
def runtime_onME(args_tuple):
    (
        progress_bar,
        order,
        option,
        payloads,
        url_path,
        ext_id,
        ext_name,
        payload_file,
        result,
        server_payloads,
    ) = args_tuple

    
    scripts = []
    scripts_s = []
    payload = {}
    payload_s = {}
    source = "chrome.runtime.onMessageExternal"
    url_of_injection_example = "https://www.example.com"

    for payload_no, i in enumerate(payloads[1]):
        dots = "."
        taintsink = result["sink"]
        obj = ""
        var = ""
        if dots in taintsink:
            obj = nomagic(taintsink, i, obj)
            var = f"obj = JSON.parse('{obj}');"
            script = f"{var}chrome.runtime.sendMessage('{ext_id}',obj)"
        else:
            obj = i
            script = f"chrome.runtime.sendMessage('{ext_id}','{obj}')"
        scripts.append(script)
        payload[payload_no] = i

    for payload_no, i in enumerate(server_payloads[1]):
        dots = "."
        taintsink = result["sink"]
        obj = ""
        var = ""
        i = i.replace(
            "mhudogbhrqrjxjxelug", f"http://127.0.0.1:8000/xss/{order}/{payload_no}"
        )
        if dots in taintsink:
            obj = nomagic(taintsink, i, obj)
            var = f"obj = JSON.parse('{obj}');"
            script = f"{var}chrome.runtime.sendMessage('{ext_id}',obj)"
        else:
            obj = i
            script = f"chrome.runtime.sendMessage('{ext_id}','{obj}')"
        scripts_s.append(script)
        payload_s[payload_no] = i

    driver = Chrome(service=Service(), options=option)
    try:
        # Navigate to example.com
        driver.get(url_of_injection_example)
        example = driver.current_window_handle

        # Wait up to 5 seconds for the title to become "Example Domain"
        title_condition = EC.title_is("Example Domain")
        WebDriverWait(driver, 5).until(title_condition)

        # get page source code of example.com
        example_source_code = driver.page_source

        # get extension popup.html
        driver.switch_to.new_window("tab")
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
                driver.refresh()
                continue

            # check for alerts in example (for extension, example then payload)
            try:
                # wait 2 seconds to see if alert is detected
                WebDriverWait(driver, 2).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert.accept()
                # get time of success [1) example]
                time_of_success = dt.utcnow()
                payload_logging(
                    "SUCCESS",
                    source,
                    ext_id,
                    ext_name,
                    url_of_injection_example,
                    "normal",
                    payload[num],
                    script,
                    time_of_injection,
                    time_of_success,
                    payload_file,
                    "nil",
                )
                

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

                    # get time of success [3) example]
                    time_of_success = dt.utcnow()
                    payload_logging(
                        "SUCCESS",
                        source,
                        ext_id,
                        ext_name,
                        url_of_injection_example,
                        "normal",
                        payload[num],
                        script,
                        time_of_injection,
                        time_of_success,
                        payload_file,
                        "nil",
                    )
                    
                except TimeoutException:
                    payload_logging(
                        "FAILURE",
                        source,
                        ext_id,
                        ext_name,
                        url_of_injection_example,
                        "normal",
                        payload[num],
                        script,
                        time_of_injection,
                        "nil",
                        payload_file,
                        "nil",
                    )
                    

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

        for num, script in enumerate(scripts_s):
            progress_bar.update(1)
            driver.switch_to.window(example)
            try:
                driver.execute_script(script)
                time_of_injection = dt.utcnow()
            except Exception as e:
                driver.refresh()
                continue
            driver.switch_to.window(extension)
            driver.refresh()
            driver.switch_to.window(example)

            try:
                if "post" in payload_s[num]:
                    a = WebDriverWait(driver, 2).until(
                        EC.element_to_be_clickable((By.ID, "a"))
                    )
                    a.click()
            except:
                pass

            url = "http://127.0.0.1:8000/data/{}/{}".format(order, payload_no)
            time.sleep(3)
            packets: list = requests.get(url).json()["data"]
            if packets != []:
                payload_logging(
                    "SUCCESS",
                    source,
                    ext_id,
                    ext_name,
                    url_of_injection_example,
                    "server",
                    payload_s[num],
                    script,
                    time_of_injection,
                    "nil",
                    payload_file,
                    packets,
                )
                
            else:
                payload_logging(
                    "FAILURE",
                    source,
                    ext_id,
                    ext_name,
                    url_of_injection_example,
                    "server",
                    payload_s[num],
                    script,
                    time_of_injection,
                    "nil",
                    payload_file,
                    packets,
                )
                

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

    


# 6) runtime.onConnectExternal
def runtime_onCE(args_tuple):
    (
        progress_bar,
        order,
        option,
        payloads,
        url_path,
        ext_id,
        ext_name,
        payload_file,
        result,
        server_payloads,
    ) = args_tuple

    
    scripts = []
    scripts_s = []
    payload = {}
    payload_s = {}
    source = "chrome.runtime.onConnectExternal"
    url_of_injection_example = "https://www.example.com"

    for payload_no, i in enumerate(payloads[1]):
        dots = "."
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
            obj = nomagic(taintsink, i, obj)
        else:
            obj = i

        var = f"obj = JSON.parse('{obj}');"

        if port != "" and portproperty != "" and portpassword != "":
            connect = {portproperty: portpassword}
            connect = json.dumps(connect)
            var = var + f"connect=JSON.parse('{connect}')"

        func = f".postMessage(obj)"
        script = f"{var}chrome.runtime.connect(connect){func}"
        scripts.append(script)
        payload[payload_no] = i

    for payload_no, i in enumerate(server_payloads[1]):
        dots = "."
        taintsink = result["sink"]
        obj = {}
        var = ""
        func = ""
        connect = ""
        i = i.replace(
            "mhudogbhrqrjxjxelug", f"http://127.0.0.1:8000/xss/{order}/{payload_no}"
        )
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
            obj = nomagic(taintsink, i, obj)
        else:
            obj = i

        var = f"obj = JSON.parse('{obj}');"

        if port != "" and portproperty != "" and portpassword != "":
            connect = {portproperty: portpassword}
            connect = json.dumps(connect)
            var = var + f"connect=JSON.parse('{connect}')"

        func = f".postMessage(obj)"
        script = f"{var}chrome.runtime.connect(connect){func}"
        scripts_s.append(script)
        payload_s[payload_no] = i

    driver = Chrome(service=Service(), options=option)
    try:
        # Navigate to example.com
        driver.get(url_of_injection_example)
        example = driver.current_window_handle

        # Wait up to 5 seconds for the title to become "Example Domain"
        title_condition = EC.title_is("Example Domain")
        WebDriverWait(driver, 5).until(title_condition)

        # get page source code of example.com
        example_source_code = driver.page_source

        # get extension popup.html
        driver.switch_to.new_window("tab")
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
                driver.refresh()
                continue

            # check for alerts in example (for extension, example then payload)
            try:
                # wait 2 seconds to see if alert is detected
                WebDriverWait(driver, 2).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert.accept()
                # get time of success [1) example]
                time_of_success = dt.utcnow()
                payload_logging(
                    "SUCCESS",
                    source,
                    ext_id,
                    ext_name,
                    url_of_injection_example,
                    "normal",
                    payload[num],
                    script,
                    time_of_injection,
                    time_of_success,
                    payload_file,
                    "nil",
                )
                

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

                    # get time of success [3) example]
                    time_of_success = dt.utcnow()
                    payload_logging(
                        "SUCCESS",
                        source,
                        ext_id,
                        ext_name,
                        url_of_injection_example,
                        "normal",
                        payload[num],
                        script,
                        time_of_injection,
                        time_of_success,
                        payload_file,
                        "nil",
                    )
                    
                except TimeoutException:
                    payload_logging(
                        "FAILURE",
                        source,
                        ext_id,
                        ext_name,
                        url_of_injection_example,
                        "normal",
                        payload[num],
                        script,
                        time_of_injection,
                        "nil",
                        payload_file,
                        "nil",
                    )
                    

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

        for num, script in enumerate(scripts_s):
            progress_bar.update(1)
            driver.switch_to.window(example)
            try:
                driver.execute_script(script)
                time_of_injection = dt.utcnow()
            except Exception as e:
                driver.refresh()
                continue
            driver.switch_to.window(extension)
            driver.refresh()
            driver.switch_to.window(example)

            try:
                if "post" in payload_s[num]:
                    a = WebDriverWait(driver, 2).until(
                        EC.element_to_be_clickable((By.ID, "a"))
                    )
                    a.click()
            except:
                pass

            url = "http://127.0.0.1:8000/data/{}/{}".format(order, payload_no)
            time.sleep(3)
            packets: list = requests.get(url).json()["data"]
            if packets != []:
                payload_logging(
                    "SUCCESS",
                    source,
                    ext_id,
                    ext_name,
                    url_of_injection_example,
                    "server",
                    payload_s[num],
                    script,
                    time_of_injection,
                    "nil",
                    payload_file,
                    packets,
                )
                
            else:
                payload_logging(
                    "FAILURE",
                    source,
                    ext_id,
                    ext_name,
                    url_of_injection_example,
                    "server",
                    payload_s[num],
                    script,
                    time_of_injection,
                    "nil",
                    payload_file,
                    packets,
                )
                

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



# new window.name_normal (works)
def window_name_N(args_tuple):
    (
        progress_bar,
        order,
        option,
        payloads,
        url_path,
        ext_id,
        ext_name,
        payload_file,
        result,
        server_payloads,
    ) = args_tuple


    
    source = "window.name"
    url_of_injection_example = "https://www.example.com"

    driver = Chrome(service=Service(), options=option)
    try:
        # Navigate to example.com
        driver.get("https://www.example.com")
        example = driver.current_window_handle

        # Wait up to 5 seconds for the title to become "Example Domain"
        title_condition = EC.title_is("Example Domain")
        WebDriverWait(driver, 5).until(title_condition)

        # get page source code of example.com
        example_source_code = driver.page_source

        # get extension popup.html
        driver.switch_to.new_window("tab")
        driver.get(url_path)
        extension = driver.current_window_handle

        # get page source code of extension
        extension_source_code = driver.page_source

        for payload_no, payload in enumerate(payloads[1]):
            # update progress bar
            progress_bar.update(1)
            # since window.name is obtained from the website url, we will inject javascript to change the window.name
            driver.switch_to.window(example)

            try:
                driver.execute_script(f"window.name = `{payload}`;")

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

                # get time of success [1) example]
                time_of_success = dt.utcnow()
                payload_logging(
                    "SUCCESS",
                    source,
                    ext_id,
                    ext_name,
                    url_of_injection_example,
                    "normal",
                    payload,
                    r"window.name = `{payload}`;",
                    time_of_injection,
                    time_of_success,
                    payload_file,
                    "nil",
                )
                

            except TimeoutException:
                payload_logging(
                    "FAILURE",
                    source,
                    ext_id,
                    ext_name,
                    url_of_injection_example,
                    "normal",
                    payload,
                    r"window.name = `{payload}`;",
                    time_of_injection,
                    "nil",
                    payload_file,
                    "nil",
                )
                

                # 2) Check for alerts in example after refreshing extension
                driver.switch_to.window(extension)
                driver.refresh()
                driver.switch_to.window(example)

                try:
                    # wait 2 seconds to see if alert is detected
                    WebDriverWait(driver, 2).until(EC.alert_is_present())
                    alert = driver.switch_to.alert
                    alert.accept()

                    # get time of success [3) example]
                    time_of_success = dt.utcnow()
                    payload_logging(
                        "SUCCESS",
                        source,
                        ext_id,
                        ext_name,
                        url_of_injection_example,
                        "normal",
                        payload,
                        r"window.name = `{payload}`;",
                        time_of_injection,
                        time_of_success,
                        payload_file,
                        "nil",
                    )
                    
                except TimeoutException:
                    payload_logging(
                        "FAILURE",
                        source,
                        ext_id,
                        ext_name,
                        url_of_injection_example,
                        "normal",
                        payload,
                        r"window.name = `{payload}`;",
                        time_of_injection,
                        "nil",
                        payload_file,
                        "nil",
                    )
                    

            try:
                # check modifications for example.com
                driver.switch_to.window(example)
                if example_source_code != driver.page_source:
                    driver.get("https://www.example.com")
            except Exception as e:
                error_logging(source, str(e))

            try:
                # check modifications for extension
                driver.switch_to.window(extension)
                if extension_source_code != driver.page_source:
                    driver.get(url_path)
            except Exception as e:
                error_logging(source, str(e))

        for payload_no, payload in enumerate(server_payloads[1]):
            progress_bar.update(1)

            # since window.name is obtained from the website url, we will inject javascript to change the window.name
            driver.switch_to.window(example)
            driver.refresh()

            payload = payload.replace(
                "mhudogbhrqrjxjxelug", f"http://127.0.0.1:8000/xss/{order}/{payload_no}"
            )
            try:
                driver.execute_script(f"window.name = `{payload}`;")
                # get time of injection
                time_of_injection = dt.utcnow()

            except Exception as e:
                continue

            driver.switch_to.window(extension)
            driver.refresh()
            driver.switch_to.window(example)

            try:
                if "post" in payload_s[num]:
                    a = WebDriverWait(driver, 2).until(
                        EC.element_to_be_clickable((By.ID, "a"))
                    )
                    a.click()
            except:
                pass

            url = "http://127.0.0.1:8000/data/{}/{}".format(order, payload_no)
            time.sleep(3)

            packets: list = requests.get(url).json()["data"]
            if packets != []:
                payload_logging(
                    "SUCCESS",
                    source,
                    ext_id,
                    ext_name,
                    url_of_injection_example,
                    "server",
                    payload,
                    r"window.name = `{payload}`",
                    time_of_injection,
                    "nil",
                    payload_file,
                    packets,
                )
                
            else:
                payload_logging(
                    "FAILURE",
                    source,
                    ext_id,
                    ext_name,
                    url_of_injection_example,
                    "server",
                    payload,
                    r"window.name = `{payload}`",
                    time_of_injection,
                    "nil",
                    payload_file,
                    packets,
                )
                

            try:
                # check modifications for example.com
                driver.switch_to.window(example)
                if example_source_code != driver.page_source:
                    driver.get("https://www.example.com")
            except:
                pass

            try:
                # check modifications for extension
                driver.switch_to.window(extension)
                if extension_source_code != driver.page_source:
                    driver.get(url_path)
            except:
                pass

    except TimeoutException:
        # Handle TimeoutException when title condition is not met
        error_logging(source, "Failed to resolve https://www.example.com")

    except Exception as e:
        error_logging(source, str(e))


# new location.href_normal (works)
def location_href_N(args_tuple):
    (
        progress_bar,
        order,
        option,
        payloads,
        url_path,
        ext_id,
        ext_name,
        payload_file,
        result,
        server_payloads,
    ) = args_tuple


    
    source = "location.href"
    url_of_injection_example = "https://www.example.com"

    driver = Chrome(service=Service(), options=option)
    try:
        # Navigate to example.com
        driver.get("https://www.example.com")
        # set handler for example.com
        example = driver.current_window_handle

        # Wait up to 5 seconds for the title to become "Example Domain"
        title_condition = EC.title_is("Example Domain")
        WebDriverWait(driver, 5).until(title_condition)

        # get page source code of example.com
        example_source_code = driver.page_source

        # get extension popup.html
        driver.switch_to.new_window("tab")
        extension = driver.current_window_handle
        driver.get(url_path)

        # get page source code of extension
        extension_source_code = driver.page_source

        # we can inject a script to change the location.href variable using query parameters or fragment Idenfiers
        for payload_no, payload in enumerate(payloads[1]):
            # update progress bar
            progress_bar.update(1)

            # we can inject a script to change the location.href variable using query parameters or fragment Idenfiers
            for j in range(2):
                driver.switch_to.window(extension)
                driver.refresh()
                driver.switch_to.window(example)

                if j == 0:
                    try:
                        driver.execute_script(
                            f"location.href = `https://www.example.com/?p={payload}`"
                        )

                        # get time of injection
                        time_of_injection = dt.utcnow()
                    except Exception as e:
                        error_logging(source, str(e))
                        continue
                else:
                    try:
                        driver.execute_script(
                            f"location.href = `https://www.example.com/#{payload}`"
                        )

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
                    payload_logging(
                        "SUCCESS",
                        source,
                        ext_id,
                        ext_name,
                        url_of_injection_example,
                        "normal",
                        payload,
                        r"location.href = `https://www.example.com/?p={payload}`",
                        time_of_injection,
                        time_of_success,
                        payload_file,
                        "nil",
                    )
                    

                except TimeoutException:
                    payload_logging(
                        "FAILURE",
                        source,
                        ext_id,
                        ext_name,
                        url_of_injection_example,
                        "normal",
                        payload,
                        r"location.href = `https://www.example.com/?p={payload}`",
                        time_of_injection,
                        "nil",
                        payload_file,
                        "nil",
                    )
                    

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
                    payload_logging(
                        "SUCCESS",
                        source,
                        ext_id,
                        ext_name,
                        url_of_injection_example,
                        "normal",
                        payload,
                        r"location.href = `https://www.example.com/?p={payload}`",
                        time_of_injection,
                        time_of_success,
                        payload_file,
                        "nil",
                    )
                    

                except TimeoutException:
                    payload_logging(
                        "FAILURE",
                        source,
                        ext_id,
                        ext_name,
                        url_of_injection_example,
                        "normal",
                        payload,
                        r"location.href = `https://www.example.com/?p={payload}`",
                        time_of_injection,
                        "nil",
                        payload_file,
                        "nil",
                    )
                    

                try:
                    # check modifications for example.com
                    driver.switch_to.window(example)
                    if example_source_code != driver.page_source:
                        driver.get("https://www.example.com")
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

        for payload_no, payload in enumerate(server_payloads[1]):
            progress_bar.upadate(1)
            driver.switch_to.window(example)
            driver.refresh()

            payload = payload.replace(
                "mhudogbhrqrjxjxelug", f"http://127.0.0.1:8000/xss/{order}/{payload_no}"
            )

            try:
                driver.execute_script(
                    f"location.href = `https://www.example.com/?p={payload}`"
                )

                # get time of injection
                time_of_injection = dt.utcnow()
            except Exception as e:
                error_logging(source, str(e))
                continue

            driver.switch_to.window(extension)
            driver.refresh()
            driver.switch_to.window(example)

            try:
                if "post" in payload_s[num]:
                    a = WebDriverWait(driver, 2).until(
                        EC.element_to_be_clickable((By.ID, "a"))
                    )
                    a.click()
            except:
                pass

            url = "http://127.0.0.1:8000/data/{}/{}".format(order, payload_no)
            time.sleep(3)

            packets: list = requests.get(url).json()["data"]

            if packets != []:
                payload_logging(
                    "SUCCESS",
                    source,
                    ext_id,
                    ext_name,
                    url_of_injection_example,
                    "server",
                    payload,
                    r"location.hash = `{payload}`",
                    time_of_injection,
                    "nil",
                    payload_file,
                    packets,
                )
                
            else:
                payload_logging(
                    "FAILURE",
                    source,
                    ext_id,
                    ext_name,
                    url_of_injection_example,
                    "server",
                    payload,
                    r"location.hash = `{payload}`",
                    time_of_injection,
                    "nil",
                    payload_file,
                    packets,
                )
                

            try:
                # check modifications for example.com
                driver.switch_to.window(example)
                if example_source_code != driver.page_source:
                    driver.get("https://www.example.com")
            except:
                pass

            try:
                # check modifications for extension
                driver.switch_to.window(extension)
                if extension_source_code != driver.page_source:
                    driver.get(url_path)
            except:
                pass

    except TimeoutException:
        error_logging(source, "Failed to resolve https://www.example.com")

    except Exception as e:
        error_logging(source, str(e))


# combined contextMenu
def context_menu(args_tuple):
    (
        progress_bar,
        _,
        _,
        payloads,
        _,
        _,
        _,
        _,
        result,
        server_payloads,
    ) = args_tuple



    # new contextMenu.selectionText_normal (works)
    def context_menu_selectionText_N(args_tuple):
        (
            progress_bar,
            order,
            option,
            payloads,
            url_path,
            ext_id,
            ext_name,
            payload_file,
            result,
            server_payloads,
        ) = args_tuple

        
        progress_bar = progress_bars[order]

        
        source = "contextMenu.selectionText"

        url_of_injection_example = "DYNAMIC_ANALYSIS/miscellaneous/xss_website.html"

        driver = Chrome(service=Service(), options=option)
        try:
            relative_path = "DYNAMIC_ANALYSIS/miscellaneous/xss_website.html"
            website = "file://" + os.path.abspath(relative_path)

            # get www.example.com
            driver.get(website)
            # driver.save_screenshot('DYNAMIC_ANALYSIS/ss.png')

            # set handler for example.com
            example = driver.current_window_handle

            # Wait up to 5 seconds for the title to become "Xss Website"
            title_condition = EC.title_is("Xss Website")
            WebDriverWait(driver, 5).until(title_condition)

            # get page source code of example.com
            example_source_code = driver.page_source

            # get extension popup.html
            driver.switch_to.new_window("tab")
            extension = driver.current_window_handle
            driver.get(url_path)
            # get page source code of extension
            extension_source_code = driver.page_source

            for payload in payloads[1]:
                # update progress bar
                progress_bar.update(1)

                driver.switch_to.window(example)

                try:
                    driver.execute_script(
                        f'document.getElementById("h1_element").innerText = `{payload}`'
                    )

                    # get time of injection
                    time_of_injection = dt.utcnow()

                except Exception as e:
                    error_logging(source, str(e))
                    continue

                target_element = driver.find_element(By.ID, "h1_element")

                try:
                    # Select the text using JavaScript
                    driver.execute_script(
                        "window.getSelection().selectAllChildren(arguments[0]);",
                        target_element,
                    )
                except Exception as e:
                    error_logging(source, str(e))
                    continue

                # usage of context menu
                try:
                    actions = ActionChains(driver)
                    actions.context_click(target_element).perform()

                    # driver.save_screenshot('DYNAMIC_ANALYSIS/ss.png')

                    for _ in range(6):
                        subprocess.call(["xdotool", "key", "Down"])

                    # Simulate pressing the "Enter" key
                    subprocess.call(["xdotool", "key", "Return"])

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
                    payload_logging(
                        "SUCCESS",
                        source,
                        ext_id,
                        ext_name,
                        url_of_injection_example,
                        "normal",
                        payload,
                        r'document.getElementById("h1_element").innerText = `{payload}`',
                        time_of_injection,
                        time_of_success,
                        payload_file,
                        "nil",
                    )
                    

                except TimeoutException:
                    payload_logging(
                        "FAILURE",
                        source,
                        ext_id,
                        ext_name,
                        url_of_injection_example,
                        "normal",
                        payload,
                        r'document.getElementById("h1_element").innerText = `{payload}`',
                        time_of_injection,
                        "nil",
                        payload_file,
                        "nil",
                    )
                    

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
                        payload_logging(
                            "SUCCESS",
                            source,
                            ext_id,
                            ext_name,
                            url_of_injection_example,
                            "normal",
                            payload,
                            r'document.getElementById("h1_element").innerText = `{payload}`',
                            time_of_injection,
                            time_of_success,
                            payload_file,
                            "nil",
                        )
                        

                    except TimeoutException:
                        payload_logging(
                            "FAILURE",
                            source,
                            ext_id,
                            ext_name,
                            url_of_injection_example,
                            "normal",
                            payload,
                            r'document.getElementById("h1_element").innerText = `{payload}`',
                            time_of_injection,
                            "nil",
                            payload_file,
                            "nil",
                        )
                        

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

            for payload_no, payload in enumerate(server_payloads[1]):
                progress_bar.update(1)

                driver.switch_to.window(example)
                driver.refresh()
                payload = payload.replace(
                    "mhudogbhrqrjxjxelug",
                    f"http://127.0.0.1:8000/xss/{order}/{payload_no}",
                )

                # inject
                try:
                    driver.execute_script(
                        f'document.getElementById("h1_element").innerText = `{payload}`'
                    )

                    # get time of injection
                    time_of_injection = dt.utcnow()

                except Exception as e:
                    error_logging(source, str(e))
                    continue

                target_element = driver.find_element(By.ID, "h1_element")

                # select element
                try:
                    # Select the text using JavaScript
                    driver.execute_script(
                        "window.getSelection().selectAllChildren(arguments[0]);",
                        target_element,
                    )
                except Exception as e:
                    error_logging(source, str(e))
                    continue

                # usage of context menu
                try:
                    actions = ActionChains(driver)
                    actions.context_click(target_element).perform()

                    # driver.save_screenshot('DYNAMIC_ANALYSIS/ss.png')

                    for _ in range(6):
                        subprocess.call(["xdotool", "key", "Down"])

                    # Simulate pressing the "Enter" key
                    subprocess.call(["xdotool", "key", "Return"])

                except Exception as e:
                    error_logging(source, str(e))
                    continue

                driver.switch_to.window(extension)
                driver.refresh()
                driver.switch_to.window(example)

                try:
                    if "post" in payload_s[num]:
                        a = WebDriverWait(driver, 2).until(
                            EC.element_to_be_clickable((By.ID, "a"))
                        )
                        a.click()
                except:
                    pass

                url = "http://127.0.0.1:8000/data/{}/{}".format(order, payload_no)
                time.sleep(3)
                packets: list = requests.get(url).json()["data"]

                if packets != []:
                    payload_logging(
                        "SUCCESS",
                        source,
                        ext_id,
                        ext_name,
                        url_of_injection_example,
                        "server",
                        payload,
                        r'document.getElementById("h1_element").innerText = `{payload}`',
                        time_of_injection,
                        "nil",
                        payload_file,
                        packets,
                    )
                    
                else:
                    payload_logging(
                        "FAILURE",
                        source,
                        ext_id,
                        ext_name,
                        url_of_injection_example,
                        "server",
                        payload,
                        r'document.getElementById("h1_element").innerText = `{payload}`',
                        time_of_injection,
                        "nil",
                        payload_file,
                        packets,
                    )
                    

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
            error_logging(source, f"Failed to resolve {website}")

        except Exception as e:
            error_logging(source, str(e))


    # new contextMenu.link_Url (works)
    def context_menu_link_url_N(args_tuple):
        (
            progress_bar,
            order,
            option,
            payloads,
            url_path,
            ext_id,
            ext_name,
            payload_file,
            result,
            server_payloads,
        ) = args_tuple

        
        progress_bar = progress_bars[order]
        
        source = "contextMenu.linkUrl"

        url_of_injection_example = "DYNAMIC_ANALYSIS/miscellaneous/xss_website.html"

        driver = Chrome(service=Service(), options=option)

        try:
            relative_path = "DYNAMIC_ANALYSIS/miscellaneous/xss_website.html"
            website = "file://" + os.path.abspath(relative_path)

            # get test xss website
            driver.get(website)
            # set handler for example.com
            example = driver.current_window_handle

            # Wait up to 5 seconds for the title to become "Xss Website"
            title_condition = EC.title_is("Xss Website")
            WebDriverWait(driver, 5).until(title_condition)

            # get page source code of example.com
            example_source_code = driver.page_source

            # get extension popup.html
            driver.switch_to.new_window("tab")
            extension = driver.current_window_handle
            driver.get(url_path)

            # get page source code of extension
            extension_source_code = driver.page_source

            cases = ["queryParams", "fragementIdentifier"]

            for payload in payloads[1]:
                # update progress bar
                progress_bar.update(1)

                # there are 2 possible ways to insert paylaod, either directly or using query parameters.
                for i in range(len(cases)):
                    # for link url, inject our payload into the link.
                    driver.switch_to.window(example)

                    # using selenium to find element by ID
                    target_element = driver.find_element(By.ID, "linkUrl")

                    # Payload Injection (Href)
                    if i == 0:
                        try:
                            # PAYLOAD INJECTION CASE 1 (Directly Injecting)
                            script = r'var linkElement = document.getElementById("linkUrl"); linkElement.href = `{payload}`'
                            driver.execute_script(
                                f'var linkElement = document.getElementById("linkUrl"); linkElement.href = `{payload}`'
                            )

                            # get time of injection
                            time_of_injection = dt.utcnow()
                        except Exception as e:
                            error_logging(source, str(e))
                            continue
                    else:
                        try:
                            # PAYLOAD INJECTION CASE 2 (Injecting Query Parameters)
                            script = r'var linkElement = document.getElementById("linkUrl"); linkElement.href = "?q=" + `{}`'
                            driver.execute_script(
                                'var linkElement = document.getElementById("linkUrl"); linkElement.href = "?q=" + `{}`'.format(
                                    payload.replace('"', '\\"').replace("'", "\\'")
                                )
                            )

                            # get time of injection
                            time_of_injection = dt.utcnow()

                        except Exception as e:
                            error_logging(source, str(e))
                            continue

                    # Seleting Text using javascript
                    try:
                        # perform text highlight/selection
                        driver.execute_script(
                            "window.getSelection().selectAllChildren(arguments[0]);",
                            target_element,
                        )

                        # usage of context menu
                        try:
                            # perform right click to open context menu
                            actions = ActionChains(driver)
                            actions.context_click(target_element).perform()

                            # navigate to extension context menu option
                            for _ in range(11):
                                subprocess.call(["xdotool", "key", "Down"])

                            # Simulate pressing the "Enter" key
                            subprocess.call(["xdotool", "key", "Return"])

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
                        payload_logging(
                            "SUCCESS",
                            source,
                            ext_id,
                            ext_name,
                            url_of_injection_example,
                            "normal",
                            payload,
                            script,
                            time_of_injection,
                            time_of_success,
                            payload_file,
                            "nil",
                        )
                        

                    except TimeoutException:
                        payload_logging(
                            "FAILURE",
                            source,
                            ext_id,
                            ext_name,
                            url_of_injection_example,
                            "normal",
                            payload,
                            script,
                            time_of_injection,
                            "nil",
                            payload_file,
                            "nil",
                        )
                        

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
                            payload_logging(
                                "SUCCESS",
                                source,
                                ext_id,
                                ext_name,
                                url_of_injection_example,
                                "normal",
                                payload,
                                script,
                                time_of_injection,
                                time_of_success,
                                payload_file,
                                "nil",
                            )
                            

                        except TimeoutException:
                            payload_logging(
                                "FAILURE",
                                source,
                                ext_id,
                                ext_name,
                                url_of_injection_example,
                                "normal",
                                payload,
                                script,
                                time_of_injection,
                                "nil",
                                payload_file,
                                "nil",
                            )
                            

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

            for payload_no, payload in enumerate(server_payloads[1]):
                progress_bar.update(1)

                driver.switch_to.window(example)
                payload = payload.replace(
                    "mhudogbhrqrjxjxelug",
                    f"http://127.0.0.1:8000/xss/{order}/{payload_no}",
                )

                # using selenium to find element by ID
                target_element = driver.find_element(By.ID, "linkUrl")

                try:
                    driver.execute_script(
                        f'var linkElement = document.getElementById("linkUrl"); linkElement.href = `{payload}`'
                    )

                    # get time of injection
                    time_of_injection = dt.utcnow()
                except Exception as e:
                    error_logging(source, str(e))
                    continue

                # Seleting Text using javascript
                try:
                    # perform text highlight/selection
                    driver.execute_script(
                        "window.getSelection().selectAllChildren(arguments[0]);",
                        target_element,
                    )

                    # usage of context menu
                    try:
                        # perform right click to open context menu
                        actions = ActionChains(driver)
                        actions.context_click(target_element).perform()

                        # navigate to extension context menu option
                        for _ in range(11):
                            subprocess.call(["xdotool", "key", "Down"])

                        # Simulate pressing the "Enter" key
                        subprocess.call(["xdotool", "key", "Return"])

                    except Exception as e:
                        error_logging(source, str(e))
                        continue

                except Exception as e:
                    error_logging(source, str(e))
                    continue

                driver.switch_to.window(extension)
                driver.refresh()
                driver.switch_to.window(example)

                try:
                    if "post" in payload_s[num]:
                        a = WebDriverWait(driver, 2).until(
                            EC.element_to_be_clickable((By.ID, "a"))
                        )
                        a.click()
                except:
                    pass

                url = "http://127.0.0.1:8000/data/{}/{}".format(order, payload_no)
                time.sleep(3)

                packets: list = requests.get(url).json()["data"]

                if packets != []:
                    payload_logging(
                        "SUCCESS",
                        source,
                        ext_id,
                        ext_name,
                        url_of_injection_example,
                        "server",
                        payload,
                        r'var linkElement = document.getElementById("linkUrl"); linkElement.href = `{payload}`',
                        time_of_injection,
                        "nil",
                        payload_file,
                        packets,
                    )
                    
                else:
                    payload_logging(
                        "FAILURE",
                        source,
                        ext_id,
                        ext_name,
                        url_of_injection_example,
                        "server",
                        payload,
                        r'var linkElement = document.getElementById("linkUrl"); linkElement.href = `{payload}`',
                        time_of_injection,
                        "nil",
                        payload_file,
                        packets,
                    )
                    

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
            error_logging(source, f"Failed to resolve {website}")
            pass

        except Exception as e:
            error_logging(source, str(e))


    # new contextMenu.srcUrl (works)
    def context_menu_src_url_N(args_tuple):
        (
            progress_bar,
            order,
            option,
            payloads,
            url_path,
            ext_id,
            ext_name,
            payload_file,
            result,
            server_payloads,
        ) = args_tuple

        
        progress_bar = progress_bars[order]
        
        source = "contextMenu.srcUrl"

        url_of_injection_example = "DYNAMIC_ANALYSIS/miscellaneous/xss_website.html"

        driver = Chrome(service=Service(), options=option)

        try:
            relative_path = "DYNAMIC_ANALYSIS/miscellaneous/xss_website.html"
            website = "file://" + os.path.abspath(relative_path)

            # get www.example.com
            driver.get(website)
            # set handler for example.com
            example = driver.current_window_handle
            # driver.save_screenshot('DYNAMIC_ANALYSIS/ss.png')

            # Wait up to 5 seconds for the title to become "Xss Website"
            title_condition = EC.title_is("Xss Website")
            WebDriverWait(driver, 5).until(title_condition)

            # get page source code of example.com
            example_source_code = driver.page_source

            # get extension popup.html
            driver.switch_to.new_window("tab")
            extension = driver.current_window_handle
            driver.get(url_path)

            # get page source code of extension
            extension_source_code = driver.page_source

            for payload in payloads[1]:
                # update progress bar
                progress_bar.update(1)

                driver.switch_to.window(example)
                driver.refresh()

                try:
                    # using javascript, change the SRC value of an oredefined image element
                    target_element = driver.find_element(By.ID, "srcUrl")
                    driver.execute_script(
                        f"document.getElementById('srcUrl').src = `{payload}`"
                    )

                    # get time of injection
                    time_of_injection = dt.utcnow()

                except Exception as e:
                    error_logging(source, str(e))
                    continue

                # usage of contextMenu
                try:
                    # # perform right click to open context menu
                    actions = ActionChains(driver)
                    actions.drag_and_drop_by_offset(
                        actions.move_to_element_with_offset(target_element, 50, 0)
                        .release()
                        .perform(),
                        -50,
                        0,
                    )
                    actions.move_to_element_with_offset(
                        target_element, 25, 0
                    ).context_click().perform()

                    # navigate to extension context menu option
                    time.sleep(1)
                    for _ in range(7):
                        subprocess.call(["xdotool", "key", "Down"])

                    # Simulate pressing the "Enter" key
                    subprocess.call(["xdotool", "key", "Return"])

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
                    payload_logging(
                        "SUCCESS",
                        source,
                        ext_id,
                        ext_name,
                        url_of_injection_example,
                        "normal",
                        payload,
                        r"document.getElementById('srcUrl').src = `{payload}`",
                        time_of_injection,
                        time_of_success,
                        payload_file,
                        "nil",
                    )
                    

                except TimeoutException:
                    payload_logging(
                        "FAILURE",
                        source,
                        ext_id,
                        ext_name,
                        url_of_injection_example,
                        "normal",
                        payload,
                        r"document.getElementById('srcUrl').src = `{payload}`",
                        time_of_injection,
                        "nil",
                        payload_file,
                        "nil",
                    )
                    

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
                        payload_logging(
                            "SUCCESS",
                            source,
                            ext_id,
                            ext_name,
                            url_of_injection_example,
                            "normal",
                            payload,
                            r"document.getElementById('srcUrl').src = `{payload}`",
                            time_of_injection,
                            time_of_success,
                            payload_file,
                            "nil",
                        )
                        

                    except TimeoutException:
                        payload_logging(
                            "FAILURE",
                            source,
                            ext_id,
                            ext_name,
                            url_of_injection_example,
                            "normal",
                            payload,
                            r"document.getElementById('srcUrl').src = `{payload}`",
                            time_of_injection,
                            "nil",
                            payload_file,
                            "nil",
                        )
                        

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

            for payload_no, payload in enumerate(server_payloads[1]):
                progress_bar.update(1)

                driver.switch_to.window(example)
                driver.refresh()

                payload = payload.replace(
                    "mhudogbhrqrjxjxelug",
                    f"http://127.0.0.1:8000/xss/{order}/{payload_no}",
                )
                try:
                    # using javascript, change the SRC value of an oredefined image element
                    target_element = driver.find_element(By.ID, "srcUrl")
                    driver.execute_script(
                        f"document.getElementById('srcUrl').src = `{payload}`"
                    )

                    # get time of injection
                    time_of_injection = dt.utcnow()

                except Exception as e:
                    error_logging(source, str(e))
                    continue

                # usage of contextMenu
                try:
                    # # perform right click to open context menu
                    actions = ActionChains(driver)
                    actions.drag_and_drop_by_offset(
                        actions.move_to_element_with_offset(target_element, 50, 0)
                        .release()
                        .perform(),
                        -50,
                        0,
                    )
                    actions.move_to_element_with_offset(
                        target_element, 25, 0
                    ).context_click().perform()

                    # navigate to extension context menu option
                    time.sleep(1)
                    for _ in range(7):
                        subprocess.call(["xdotool", "key", "Down"])

                    # Simulate pressing the "Enter" key
                    subprocess.call(["xdotool", "key", "Return"])

                except Exception as e:
                    error_logging(source, str(e))
                    continue

                driver.switch_to.window(extension)
                driver.refresh()
                driver.switch_to.window(example)

                try:
                    if "post" in payload_s[num]:
                        a = WebDriverWait(driver, 2).until(
                            EC.element_to_be_clickable((By.ID, "a"))
                        )
                        a.click()
                except:
                    pass

                url = "http://127.0.0.1:8000/data/{}/{}".format(order, payload_no)
                time.sleep(3)

                packets: list = requests.get(url).json()["data"]

                if packets != []:
                    payload_logging(
                        "SUCCESS",
                        source,
                        ext_id,
                        ext_name,
                        url_of_injection_example,
                        "server",
                        payload,
                        r"document.getElementById('srcUrl').src = `{payload}`",
                        time_of_injection,
                        "nil",
                        payload_file,
                        packets,
                    )
                    
                else:
                    payload_logging(
                        "FAILURE",
                        source,
                        ext_id,
                        ext_name,
                        url_of_injection_example,
                        "server",
                        payload,
                        r"document.getElementById('srcUrl').src = `{payload}`",
                        time_of_injection,
                        "nil",
                        payload_file,
                        packets,
                    )
                    

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
            error_logging(source, f"Failed to resolve {website}")
            pass

        except Exception as e:
            error_logging(source, str(e))


    # new contextMenu.frameUrl (works for jerald but not for me. smlj)
    def context_menu_frame_url_N(args_tuple):
        (
            progress_bar,
            order,
            option,
            payloads,
            url_path,
            ext_id,
            ext_name,
            payload_file,
            result,
            server_payloads,
        ) = args_tuple

        
        progress_bar = progress_bars[order]

        source = "contextMenu.frameUrl"

        url_of_injection_example = "DYNAMIC_ANALYSIS/miscellaneous/xss_website.html"

        driver = Chrome(service=Service(), options=option)

        try:
            relative_path = "DYNAMIC_ANALYSIS/miscellaneous/xss_website.html"
            website = "file://" + os.path.abspath(relative_path)

            # get test xss website
            driver.get(website)
            # set handler for example.com
            example = driver.current_window_handle

            # Wait up to 5 seconds for the title to become "Xss Website"
            title_condition = EC.title_is("Xss Website")
            WebDriverWait(driver, 5).until(title_condition)

            # get page source code of example.com
            example_source_code = driver.page_source

            # get extension popup.html
            driver.switch_to.new_window("tab")
            extension = driver.current_window_handle
            driver.get(url_path)

            # get page source code of extension
            extension_source_code = driver.page_source

            cases = ["queryParams", "fragementIdentifier"]

            for payload in payloads[1]:
                # update progress bar
                progress_bar.update(1)

                for i in range(len(cases)):
                    driver.switch_to.window(example)

                    # using selenium to find element by ID
                    iframeElement = driver.find_element(By.ID, "frameUrl")

                    if i == 0:
                        try:
                            driver.execute_script(
                                f'var frameElement = document.getElementById("frameUrl"); frameElement.src = `https://www.example_xss.com/XSS?q={payload}`'
                            )
                            script = r'var frameElement = document.getElementById("frameUrl"); frameElement.src = `https://www.example_xss.com/XSS?q={payload}`;'
                            # get time of injection
                            time_of_injection = dt.utcnow()
                        except Exception as e:
                            error_logging(source, str(e))
                            continue
                    else:
                        try:
                            driver.execute_script(
                                f'var frameElement = document.getElementById("frameUrl"); frameElement.src = `https://www.example_xss.com/XSS#{payload}`'
                            )
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
                            subprocess.call(["xdotool", "key", "Down"])

                        # Simulate pressing the "Enter" key
                        subprocess.call(["xdotool", "key", "Return"])

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
                        payload_logging(
                            "SUCCESS",
                            source,
                            ext_id,
                            ext_name,
                            url_of_injection_example,
                            "normal",
                            payload,
                            script,
                            time_of_injection,
                            time_of_success,
                            payload_file,
                            "nil",
                        )
                        

                    except TimeoutException:
                        payload_logging(
                            "FAILURE",
                            source,
                            ext_id,
                            ext_name,
                            url_of_injection_example,
                            "normal",
                            payload,
                            script,
                            time_of_injection,
                            "nil",
                            payload_file,
                            "nil",
                        )
                        

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
                            payload_logging(
                                "SUCCESS",
                                source,
                                ext_id,
                                ext_name,
                                url_of_injection_example,
                                "normal",
                                payload,
                                script,
                                time_of_injection,
                                time_of_success,
                                payload_file,
                                "nil",
                            )
                            

                        except TimeoutException:
                            payload_logging(
                                "FAILURE",
                                source,
                                ext_id,
                                ext_name,
                                url_of_injection_example,
                                "normal",
                                payload,
                                script,
                                time_of_injection,
                                "nil",
                                payload_file,
                                "nil",
                            )
                            

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

            for payload_no, payload in enumerate(server_payloads[1]):
                progress_bar.update(1)

                driver.switch_to.window(example)
                payload = payload.replace(
                    "mhudogbhrqrjxjxelug",
                    f"http://127.0.0.1:8000/xss/{order}/{payload_no}",
                )

                iframeElement = driver.find_element(By.ID, "frameUrl")

                try:
                    driver.execute_script(
                        f'var frameElement = document.getElementById("frameUrl"); frameElement.src = `https://www.example_xss.com/XSS?q={payload}`'
                    )
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
                        subprocess.call(["xdotool", "key", "Down"])

                    # Simulate pressing the "Enter" key
                    subprocess.call(["xdotool", "key", "Return"])

                except Exception as e:
                    error_logging(source, str(e))
                    continue

                driver.switch_to.window(extension)
                driver.refresh()
                driver.switch_to.window(example)

                try:
                    if "post" in payload_s[num]:
                        a = WebDriverWait(driver, 2).until(
                            EC.element_to_be_clickable((By.ID, "a"))
                        )
                        a.click()
                except:
                    pass

                url = "http://127.0.0.1:8000/data/{}/{}".format(order, payload_no)
                time.sleep(3)

                packets: list = requests.get(url).json()["data"]
                if packets != []:
                    payload_logging(
                        "SUCCESS",
                        source,
                        ext_id,
                        ext_name,
                        url_of_injection_example,
                        "server",
                        payload,
                        r'var frameElement = document.getElementById("frameUrl"); frameElement.src = `https://www.example_xss.com/XSS?q={payload}`',
                        time_of_injection,
                        "nil",
                        payload_file,
                        packets,
                    )
                    
                else:
                    payload_logging(
                        "FAILURE",
                        source,
                        ext_id,
                        ext_name,
                        url_of_injection_example,
                        "server",
                        payload,
                        r'var frameElement = document.getElementById("frameUrl"); frameElement.src = `https://www.example_xss.com/XSS?q={payload}`',
                        time_of_injection,
                        "nil",
                        payload_file,
                        packets,
                    )
                    

        except TimeoutException:
            error_logging(source, f"Failed to resolve {website}")

        except Exception as e:
            error_logging(source, str(e))


    # new contextMenu.pageUrl (works)
    def context_menu_pageUrl_N(args_tuple):
        (
            progress_bar,
            order,
            option,
            payloads,
            url_path,
            ext_id,
            ext_name,
            payload_file,
            result,
            server_payloads,
        ) = args_tuple

        
        progress_bar = progress_bars[order]
        
        source = "contextMenu.pageUrl"

        url_of_injection_example = "DYNAMIC_ANALYSIS/miscellaneous/xss_website.html"

        driver = Chrome(service=Service(), options=option)

        try:
            relative_path = "DYNAMIC_ANALYSIS/miscellaneous/xss_website.html"
            website = "file://" + os.path.abspath(relative_path)

            # get test xss website
            driver.get(website)

            # set handler for example.com
            example = driver.current_window_handle

            # Wait up to 5 seconds for the title to become "Xss Website"
            title_condition = EC.title_is("Xss Website")
            WebDriverWait(driver, 5).until(title_condition)

            # get page source code of example.com
            example_source_code = driver.page_source

            # get extension popup.html
            driver.switch_to.new_window("tab")
            extension = driver.current_window_handle
            driver.get(url_path)

            # get page source code of extension
            extension_source_code = driver.page_source

            cases = ["queryParams", "fragementIdentifier"]

            for payload in payloads[1]:
                # update progress bar
                progress_bar.update(1)

                for i in range(len(cases)):
                    driver.switch_to.window(example)

                    # url encode xss payload
                    encoded_payload = urllib.parse.quote(payload)

                    if i == 0:
                        try:
                            driver.execute_script(
                                f"window.history.replaceState(null, null, `{website}?qureyParam={encoded_payload}`)"
                            )
                            script = r"window.history.replaceState(null, null, `{website}?qureyParam={encoded_payload}`);"
                            # get time of injection
                            time_of_injection = dt.utcnow()
                        except Exception as e:
                            error_logging(source, str(e))
                            continue
                    else:
                        try:
                            driver.execute_script(
                                f"window.history.replaceState(null, null, `{website}#{encoded_payload}`)"
                            )
                            script = r"window.history.replaceState(null, null, `{website}#{encoded_payload}`);"

                            # get time of injection
                            time_of_injection = dt.utcnow()
                        except Exception as e:
                            error_logging(source, str(e))
                            continue

                    PageUrlElement = driver.find_element(By.ID, "pageUrl")

                    # usage of context menu
                    try:
                        # # perform right click to open context menu
                        actions = ActionChains(driver)
                        actions.move_to_element(PageUrlElement)
                        actions.context_click().perform()

                        for _ in range(8):
                            subprocess.call(["xdotool", "key", "Down"])

                        # Simulate pressing the "Enter" key
                        subprocess.call(["xdotool", "key", "Return"])

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
                        payload_logging(
                            "SUCCESS",
                            source,
                            ext_id,
                            ext_name,
                            url_of_injection_example,
                            "normal",
                            payload,
                            script,
                            time_of_injection,
                            time_of_success,
                            payload_file,
                            "nil",
                        )
                        

                    except TimeoutException:
                        payload_logging(
                            "FAILURE",
                            source,
                            ext_id,
                            ext_name,
                            url_of_injection_example,
                            "normal",
                            payload,
                            script,
                            time_of_injection,
                            "nil",
                            payload_file,
                            "nil",
                        )
                        

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
                            payload_logging(
                                "SUCCESS",
                                source,
                                ext_id,
                                ext_name,
                                url_of_injection_example,
                                "normal",
                                payload,
                                script,
                                time_of_injection,
                                time_of_success,
                                payload_file,
                                "nil",
                            )
                            

                        except TimeoutException:
                            payload_logging(
                                "FAILURE",
                                source,
                                ext_id,
                                ext_name,
                                url_of_injection_example,
                                "normal",
                                payload,
                                script,
                                time_of_injection,
                                "nil",
                                payload_file,
                                "nil",
                            )
                            

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

            for payload_no, payload in enumerate(server_payloads[1]):
                progress_bar.update(1)

                driver.switch_to.window(example)
                payload = payload.replace(
                    "mhudogbhrqrjxjxelug",
                    f"http://127.0.0.1:8000/xss/{order}/{payload_no}",
                )

                try:
                    driver.execute_script(
                        f"window.history.replaceState(null, null, `{website}?qureyParam={payload}`)"
                    )
                    # get time of injection
                    time_of_injection = dt.utcnow()
                except Exception as e:
                    error_logging(source, str(e))
                    continue

                PageUrlElement = driver.find_element(By.ID, "pageUrl")

                # usage of context menu
                try:
                    # # perform right click to open context menu
                    actions = ActionChains(driver)
                    actions.move_to_element(PageUrlElement)
                    actions.context_click().perform()

                    for _ in range(8):
                        subprocess.call(["xdotool", "key", "Down"])

                    # Simulate pressing the "Enter" key
                    subprocess.call(["xdotool", "key", "Return"])

                except Exception as e:
                    error_logging(source, str(e))
                    continue

                driver.switch_to.window(extension)
                driver.refresh()
                driver.switch_to.window(example)

                try:
                    if "post" in payload_s[num]:
                        a = WebDriverWait(driver, 2).until(
                            EC.element_to_be_clickable((By.ID, "a"))
                        )
                        a.click()
                except:
                    pass

                url = "http://127.0.0.1:8000/data/{}/{}".format(order, payload_no)
                time.sleep(3)

                packets: list = requests.get(url).json()["data"]
                if packets != []:
                    payload_logging(
                        "SUCCESS",
                        source,
                        ext_id,
                        ext_name,
                        url_of_injection_example,
                        "server",
                        payload,
                        r"window.history.replaceState(null, null, `{website}?qureyParam={payload}`);",
                        time_of_injection,
                        "nil",
                        payload_file,
                        packets,
                    )
                    
                else:
                    payload_logging(
                        "FAILURE",
                        source,
                        ext_id,
                        ext_name,
                        url_of_injection_example,
                        "server",
                        payload,
                        r"window.history.replaceState(null, null, `{website}?qureyParam={payload}`);",
                        time_of_injection,
                        "nil",
                        payload_file,
                        packets,
                    )
                    

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
            error_logging(source, f"Failed to resolve {website}")

        except Exception as e:
            error_logging(source, str(e))


    source = result["taintsource"]
    match source:
        case "selectionText":
            return context_menu_selectionText_N(args_tuple)
        case "linkUrl":
            return ontext_menu_link_url_N(args_tuple)
        case "srcUrl":
            return context_menu_src_url_N(args_tuple)
        case "frameUrl":
            return context_menu_frame_url_N(args_tuple)
        case "pageUrl":
            return context_menu_pageUrl_N(args_tuple)
        case _:
            progress_bar.update(payloads[0]+server_payloads[0])
            return


# combined chromeTabQuery
def chromeTabQuery(args_tuple):
    (
        progress_bar,
        _,
        _,
        payloads,
        _,
        _,
        _,
        _,
        result,
        server_payloads,
    ) = args_tuple


    # new chromeTabsQuery.title (works)
    def chromeTabsQuery_title_N(args_tuple):
        (
            progress_bar,
            order,
            option,
            payloads,
            url_path,
            ext_id,
            ext_name,
            payload_file,
            result,
            server_payloads,
        ) = args_tuple

        
        progress_bar = progress_bars[order]
        
        source = "chromeTabsQuery.title"

        url_of_injection_example = "https://www.example.com"

        driver = Chrome(service=Service(), options=option)

        try:
            # get www.example.com
            driver.get("https://www.example.com")

            # set handler for example.com
            example = driver.current_window_handle

            # Wait up to 5 seconds for the title to become "Example Domain"
            title_condition = EC.title_is("Example Domain")
            WebDriverWait(driver, 5).until(title_condition)

            # get page source code of example.com
            example_source_code = driver.page_source

            # get extension popup.html
            driver.switch_to.new_window("tab")
            extension = driver.current_window_handle
            driver.get(url_path)

            # get page source code of extension
            extension_source_code = driver.page_source

            for payload in payloads[1]:
                # update progress bar
                progress_bar.update(1)

                # change to example.com to change document.title property
                driver.switch_to.window(example)
                driver.refresh()

                try:
                    driver.execute_script(f"document.title = `{payload}`;")

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
                    payload_logging(
                        "SUCCESS",
                        source,
                        ext_id,
                        ext_name,
                        url_of_injection_example,
                        "normal",
                        payload,
                        r"document.title = `{payload}`;",
                        time_of_injection,
                        time_of_success,
                        payload_file,
                        "nil",
                    )
                    

                except TimeoutException:
                    payload_logging(
                        "FAILURE",
                        source,
                        ext_id,
                        ext_name,
                        url_of_injection_example,
                        "normal",
                        payload,
                        r"document.title = `{payload}`;",
                        time_of_injection,
                        "nil",
                        payload_file,
                        "nil",
                    )
                    

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
                        payload_logging(
                            "SUCCESS",
                            source,
                            ext_id,
                            ext_name,
                            url_of_injection_example,
                            "normal",
                            payload,
                            r"document.title = `{payload}`;",
                            time_of_injection,
                            time_of_success,
                            payload_file,
                            "nil",
                        )
                        

                    except TimeoutException:
                        payload_logging(
                            "FAILURE",
                            source,
                            ext_id,
                            ext_name,
                            url_of_injection_example,
                            "normal",
                            payload,
                            r"document.title = `{payload}`;",
                            time_of_injection,
                            "nil",
                            payload_file,
                            "nil",
                        )
                        

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

            for payload_no, payload in enumerate(server_payloads[1]):
                progress_bar.update(1)

                driver.switch_to.window(example)
                driver.refresh()
                payload = payload.replace(
                    "mhudogbhrqrjxjxelug",
                    f"http://127.0.0.1:8000/xss/{order}/{payload_no}",
                )

                try:
                    driver.execute_script(f"document.title = `{payload}`;")
                    # get time of injection
                    time_of_injection = dt.utcnow()

                except Exception as e:
                    error_logging(source, str(e))
                    continue

                driver.switch_to.window(extension)
                driver.refresh()
                driver.switch_to.window(example)

                try:
                    if "post" in payload_s[num]:
                        a = WebDriverWait(driver, 2).until(
                            EC.element_to_be_clickable((By.ID, "a"))
                        )
                        a.click()
                except:
                    pass

                url = "http://127.0.0.1:8000/data/{}/{}".format(order, payload_no)
                time.sleep(3)

                packets: list = requests.get(url).json()["data"]
                if packets != []:
                    payload_logging(
                        "SUCCESS",
                        source,
                        ext_id,
                        ext_name,
                        url_of_injection_example,
                        "server",
                        payload,
                        r"document.title = `{payload}`;",
                        time_of_injection,
                        "nil",
                        payload_file,
                        packets,
                    )
                    
                else:
                    payload_logging(
                        "FAILURE",
                        source,
                        ext_id,
                        ext_name,
                        url_of_injection_example,
                        "server",
                        payload,
                        r"document.title = `{payload}`;",
                        time_of_injection,
                        "nil",
                        payload_file,
                        packets,
                    )
                    

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
            error_logging(source, f"Failed to resolve https://www.example.com")

        except Exception as e:
            # Handle any other exceptions that occur
            error_logging(source, str(e))

        
        

    # new chromeTabQuery.url (works)
    def chromeTabQuery_url_N(args_tuple):
        (
            progress_bar,
            order,
            option,
            payloads,
            url_path,
            ext_id,
            ext_name,
            payload_file,
            result,
            server_payloads,
        ) = args_tuple

        
        progress_bar = progress_bars[order]

        source = "chromeTabQuery.url"

        url_of_injection_example = "https://www.example.com"

        driver = Chrome(service=Service(), options=option)

        # Case Secnario for chromeTabQuery_url_new
        try:
            # Navigate to example.com
            driver.get("https://www.example.com")
            # set handler for example.com
            example = driver.current_window_handle

            # Wait up to 5 seconds for the title to become "Example Domain"
            title_condition = EC.title_is("Example Domain")
            WebDriverWait(driver, 5).until(title_condition)

            # get page source code of example.com
            example_source_code = driver.page_source

            # get extension popup.html
            driver.switch_to.new_window("tab")
            extension = driver.current_window_handle
            driver.get(url_path)

            # get page source code of extension
            extension_source_code = driver.page_source

            for payload in payloads[1]:
                # update progress bar
                progress_bar.update(1)

                payload = payload.strip()

                # change to example.com to change url property
                driver.switch_to.window(example)
                try:
                    driver.execute_script(
                        f"location.href = `https://www.example.com/?p={payload}`"
                    )

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
                    payload_logging(
                        "SUCCESS",
                        source,
                        ext_id,
                        ext_name,
                        url_of_injection_example,
                        "normal",
                        payload,
                        r"location.href = `https://www.example.com/?p={payload}`",
                        time_of_injection,
                        time_of_success,
                        payload_file,
                        "nil",
                    )
                    

                except TimeoutException:
                    payload_logging(
                        "FAILURE",
                        source,
                        ext_id,
                        ext_name,
                        url_of_injection_example,
                        "normal",
                        payload,
                        r"location.href = `https://www.example.com/?p={payload}`",
                        time_of_injection,
                        "nil",
                        payload_file,
                        "nil",
                    )
                    

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
                        payload_logging(
                            "SUCCESS",
                            source,
                            ext_id,
                            ext_name,
                            url_of_injection_example,
                            "normal",
                            payload,
                            r"location.href = `https://www.example.com/?p={payload}`",
                            time_of_injection,
                            time_of_success,
                            payload_file,
                            "nil",
                        )
                        

                    except TimeoutException:
                        payload_logging(
                            "FAILURE",
                            source,
                            ext_id,
                            ext_name,
                            url_of_injection_example,
                            "normal",
                            payload,
                            r"location.href = `https://www.example.com/?p={payload}`",
                            time_of_injection,
                            "nil",
                            payload_file,
                            "nil",
                        )
                        

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

            for payload_no, payload in enumerate(server_payloads[1]):
                progress_bar.update(1)
                driver.switch_to.window(example)
                driver.refresh()

                payload = payload.replace(
                    "mhudogbhrqrjxjxelug",
                    f"http://127.0.0.1:8000/xss/{order}/{payload_no}",
                )

                try:
                    driver.execute_script(
                        f"location.href = `https://www.example.com/?p={payload}`"
                    )

                    # get time of injection
                    time_of_injection = dt.utcnow()

                except Exception as e:
                    error_logging(source, str(e))
                    continue

                driver.switch_to.window(extension)
                driver.refresh()
                driver.switch_to.window(example)

                try:
                    if "post" in payload_s[num]:
                        a = WebDriverWait(driver, 2).until(
                            EC.element_to_be_clickable((By.ID, "a"))
                        )
                        a.click()
                except:
                    pass

                url = "http://127.0.0.1:8000/data/{}/{}".format(order, payload_no)
                time.sleep(3)

                packets: list = requests.get(url).json()["data"]
                if packets != []:
                    payload_logging(
                        "SUCCESS",
                        source,
                        ext_id,
                        ext_name,
                        url_of_injection_example,
                        "server",
                        payload,
                        r"location.href = `https://www.example.com/?p={payload}`",
                        time_of_injection,
                        "nil",
                        payload_file,
                        packets,
                    )
                    
                else:
                    payload_logging(
                        "FAILURE",
                        source,
                        ext_id,
                        ext_name,
                        url_of_injection_example,
                        "server",
                        payload,
                        r"location.href = `https://www.example.com/?p={payload}`",
                        time_of_injection,
                        "nil",
                        payload_file,
                        packets,
                    )
                    

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
            error_logging(source, f"Failed to resolve https://www.example.com")

        except Exception as e:
            error_logging(source, str(e))
        
        

    # new chromeTabQuery.favIconUrl (works)
    def chromeTabQuery_favIconUrl_N(args_tuple):
        (
            progress_bar,
            order,
            option,
            payloads,
            url_path,
            ext_id,
            ext_name,
            payload_file,
            result,
            server_payloads,
        ) = args_tuple

        
        progress_bar = progress_bars[order]

        # automatically populate server_progressbar
        progress_bar.update(server_payloads[0])

        
        source = "chromeTabsQuery.favIconUrl"

        url_of_injection_example = "DYNAMIC_ANALYSIS/miscellaneous/xss_website.html"

        driver = Chrome(service=Service(), options=option)
        dir_path = Path(
            f"DYNAMIC_ANALYSIS/miscellaneous/ChromeTabQueryFiles/favIconUrl_instance_{order}"
        )

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
            pic_path = Path(
                "DYNAMIC_ANALYSIS/miscellaneous/default.png"
            )  # Specify the path of the picture you want to copy

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

        def changeFavIconUrl(driver, order, payload):
            payload = payload.strip()

            try:
                # remove current favIconUrl
                driver.execute_script(
                    """
                var linkElement = document.querySelector('link[rel="icon"]');
                if (linkElement) {
                linkElement.parentNode.removeChild(linkElement);
                }
                """
                )
            except Exception as e:
                error_logging(source, str(e))

            try:
                # set new favIconUrl
                driver.execute_script(
                    f"""
                var link = document.createElement('link');
                link.type = 'image/jpg';
                link.rel = 'icon';
                link.href = './ChromeTabQueryFiles/favIconUrl_instance_{order}/{payload}.png';
                document.head.appendChild(link);
                """
                )

            except Exception as e:
                error_logging(source, str(e))

        # preconfigure files required
        access_directory()

        try:
            website = "file://" + os.path.abspath(url_of_injection_example)

            # get www.example.com
            driver.get(website)
            # set handler for example.com
            example = driver.current_window_handle

            # Wait up to 5 seconds for the title to become "Example Domain"
            title_condition = EC.title_is("Xss Website")
            WebDriverWait(driver, 5).until(title_condition)

            # get page source code of example.com
            example_source_code = driver.page_source

            # add a default favIconUrl
            driver.execute_script(
                """
            var link = document.createElement('link');
            link.type = 'image/jpg';
            link.rel = 'icon';
            link.href = 'default.png';
            document.head.appendChild(link);
            """
            )

            # get extension popup.html
            driver.switch_to.new_window("tab")
            extension = driver.current_window_handle
            driver.get(url_path)

            # get page source code of extension
            extension_source_code = driver.page_source

            for payload in payloads[1]:
                # update progress bar
                progress_bar.update(1)

                # forbidden_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|', "'"]
                forbidden_chars = ["/", "\\", ":", "*", "?", '"', "<", ">", "|"]
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
                    payload_logging(
                        "SUCCESS",
                        source,
                        ext_id,
                        ext_name,
                        url_of_injection_example,
                        "normal",
                        payload,
                        r"var link = document.createElement('link');link.type = 'image/jpg';link.rel = 'icon';link.href = './ChromeTabQueryFiles/favIconUrl_instance_{number}/{payload}.png';document.head.appendChild(link);",
                        time_of_injection,
                        time_of_success,
                        payload_file,
                        "nil",
                    )
                    

                except TimeoutException:
                    payload_logging(
                        "FAILURE",
                        source,
                        ext_id,
                        ext_name,
                        url_of_injection_example,
                        "normal",
                        payload,
                        r"var link = document.createElement('link');link.type = 'image/jpg';link.rel = 'icon';link.href = './ChromeTabQueryFiles/favIconUrl_instance_{number}/{payload}.png';document.head.appendChild(link);",
                        time_of_injection,
                        "nil",
                        payload_file,
                        "nil",
                    )
                    

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
                        payload_logging(
                            "SUCCESS",
                            source,
                            ext_id,
                            ext_name,
                            url_of_injection_example,
                            "normal",
                            payload,
                            r"var link = document.createElement('link');link.type = 'image/jpg';link.rel = 'icon';link.href = './ChromeTabQueryFiles/favIconUrl_instance_{number}/{payload}.png';document.head.appendChild(link);",
                            time_of_injection,
                            time_of_success,
                            payload_file,
                            "nil",
                        )
                        

                    except TimeoutException:
                        payload_logging(
                            "FAILURE",
                            source,
                            ext_id,
                            ext_name,
                            url_of_injection_example,
                            "normal",
                            payload,
                            r"var link = document.createElement('link');link.type = 'image/jpg';link.rel = 'icon';link.href = './ChromeTabQueryFiles/favIconUrl_instance_{number}/{payload}.png';document.head.appendChild(link);",
                            time_of_injection,
                            "nil",
                            payload_file,
                            "nil",
                        )
                        

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
            error_logging(source, f"Failed to resolve {website}")
            pass

        except Exception as e:
            # Handle any other exceptions that occur
            error_logging(source, str(e))
        
        

    source = result["taintsource"]
    match source:
        case "title":
            return chromeTabsQuery_title_N(args_tuple)
        case "faviconUrl":
            return chromeTabQuery_favIconUrl_N(args_tuple)
        case "url":
            return chromeTabQuery_url_N(args_tuple)
        case _:
            progress_bar.update(payloads[0] + server_payloads[0])
            return


# new location.search (works)
def locationSearch_N(args_tuple):
    (
        progress_bar,
        order,
        option,
        payloads,
        url_path,
        ext_id,
        ext_name,
        payload_file,
        result,
        server_payloads,
    ) = args_tuple


    source = "location.search"
    url_of_injection_example = "https://www.example.com"

    driver = Chrome(service=Service(), options=option)

    try:
        # navigate to example.com
        driver.get("https://www.example.com")
        # set handler for example.com
        example = driver.current_window_handle

        # Wait up to 5 seconds for the title to become "Example Domain"
        title_condition = EC.title_is("Example Domain")
        WebDriverWait(driver, 5).until(title_condition)

        # get page source code of example.com
        example_source_code = driver.page_source

        # get extension popup.html
        driver.switch_to.new_window("tab")
        driver.get(url_path)
        extension = driver.current_window_handle

        # get page source code of extension
        extension_source_code = driver.page_source

        for payload in payloads[1]:
            # update progress bar
            progress_bar.update(1)

            # define a query parameter
            driver.switch_to.window(example)

            try:
                driver.execute_script(f"window.location.search=`?q={payload}`")

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
                payload_logging(
                    "SUCCESS",
                    source,
                    ext_id,
                    ext_name,
                    url_of_injection_example,
                    "normal",
                    payload,
                    r"window.location.search=`?q={payload}`",
                    time_of_injection,
                    time_of_success,
                    payload_file,
                    "nil",
                )
                

            except TimeoutException:
                payload_logging(
                    "FAILURE",
                    source,
                    ext_id,
                    ext_name,
                    url_of_injection_example,
                    "normal",
                    payload,
                    r"window.location.search=`?q={payload}`",
                    time_of_injection,
                    "nil",
                    payload_file,
                    "nil",
                )
                

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
                    payload_logging(
                        "SUCCESS",
                        source,
                        ext_id,
                        ext_name,
                        url_of_injection_example,
                        "normal",
                        payload,
                        r"window.location.search=`?q={payload}`",
                        time_of_injection,
                        time_of_success,
                        payload_file,
                        "nil",
                    )
                    
                except TimeoutException:
                    payload_logging(
                        "FAILURE",
                        source,
                        ext_id,
                        ext_name,
                        url_of_injection_example,
                        "normal",
                        payload,
                        r"window.location.search=`?q={payload}`",
                        time_of_injection,
                        "nil",
                        payload_file,
                        "nil",
                    )
                    

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

        for payload_no, payload in enumerate(server_payloads[1]):
            progress_bar.update(1)
            driver.switch_to.window(example)
            driver.refresh()

            payload = payload.replace(
                "mhudogbhrqrjxjxelug", f"http://127.0.0.1:8000/xss/{order}/{payload_no}"
            )

            try:
                driver.execute_script(f"window.location.search=`?q={payload}`")

                # get time of injection
                time_of_injection = dt.utcnow()
            except Exception as e:
                error_logging(source, str(e))
                continue

            driver.switch_to.window(extension)
            driver.refresh()
            driver.switch_to.window(example)

            try:
                if "post" in payload_s[num]:
                    a = WebDriverWait(driver, 2).until(
                        EC.element_to_be_clickable((By.ID, "a"))
                    )
                    a.click()
            except:
                pass

            url = "http://127.0.0.1:8000/data/{}/{}".format(order, payload_no)
            time.sleep(3)

            packets: list = requests.get(url).json()["data"]
            if packets != []:
                payload_logging(
                    "SUCCESS",
                    source,
                    ext_id,
                    ext_name,
                    url_of_injection_example,
                    "server",
                    payload,
                    r"window.location.search=`?q={payload}`",
                    time_of_injection,
                    "nil",
                    payload_file,
                    packets,
                )
                
            else:
                payload_logging(
                    "FAILURE",
                    source,
                    ext_id,
                    ext_name,
                    url_of_injection_example,
                    "server",
                    payload,
                    r"window.location.search=`?q={payload}`",
                    time_of_injection,
                    "nil",
                    payload_file,
                    packets,
                )
                

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
        error_logging(source, f"Failed to resolve https://www.example.com")
        pass

    except Exception as e:
        error_logging(source, str(e))


# combined chromeDebugger
def chromeDebugger(args_tuple):
    (
        progress_bar,
        _,
        _,
        payloads,
        _,
        _,
        _,
        _,
        result,
        server_payloads,
    ) = args_tuple


    # new chrome.Debugger.GetTargets (works)
    def chromeDebugger_title_N(args_tuple):
        (
            progress_bar,
            order,
            option,
            payloads,
            url_path,
            ext_id,
            ext_name,
            payload_file,
            result,
            server_payloads,
        ) = args_tuple

        
        progress_bar = progress_bars[order]
        
        source = "chromeDebugger.GetTargets.title"

        url_of_injection_example = "https://www.example.com"

        driver = Chrome(service=Service(), options=option)

        try:
            website = "https://www.example.com"

            # navigate to example.com
            driver.get(website)
            # set handler for example.com
            example = driver.current_window_handle

            # Wait up to 5 seconds for the title to become "Example Domain"
            title_condition = EC.title_is("Example Domain")
            WebDriverWait(driver, 5).until(title_condition)

            # get page source code of example.com
            example_source_code = driver.page_source

            # get extension popup.html
            driver.switch_to.new_window("tab")
            driver.get(url_path)
            extension = driver.current_window_handle

            # get page source code of extension
            extension_source_code = driver.page_source

            for payload in payloads[1]:
                # update progress bar
                progress_bar.update(1)

                # change to example.com to change document.title property
                driver.switch_to.window(example)
                driver.refresh()

                try:
                    driver.execute_script(f"document.title = `{payload}`;")

                    # get time of injection
                    time_of_injection = dt.utcnow()

                except Exception as e:
                    error_logging(source, str(e))
                    continue

                try:
                    # Press the F12 key to open the developer tools
                    subprocess.call(["xdotool", "keydown", "F12"])
                    subprocess.call(["xdotool", "keyup", "F12"])
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
                    payload_logging(
                        "SUCCESS",
                        source,
                        ext_id,
                        ext_name,
                        url_of_injection_example,
                        "normal",
                        payload,
                        r"document.title = `{payload}`;",
                        time_of_injection,
                        time_of_success,
                        payload_file,
                        "nil",
                    )
                    

                except TimeoutException:
                    payload_logging(
                        "FAILURE",
                        source,
                        ext_id,
                        ext_name,
                        url_of_injection_example,
                        "normal",
                        payload,
                        r"document.title = `{payload}`;",
                        time_of_injection,
                        "nil",
                        payload_file,
                        "nil",
                    )
                    

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
                        payload_logging(
                            "SUCCESS",
                            source,
                            ext_id,
                            ext_name,
                            url_of_injection_example,
                            "normal",
                            payload,
                            r"document.title = `{payload}`;",
                            time_of_injection,
                            time_of_success,
                            payload_file,
                            "nil",
                        )
                        

                    except TimeoutException:
                        payload_logging(
                            "FAILURE",
                            source,
                            ext_id,
                            ext_name,
                            url_of_injection_example,
                            "normal",
                            payload,
                            r"document.title = `{payload}`;",
                            time_of_injection,
                            "nil",
                            payload_file,
                            "nil",
                        )
                        

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

            for payload_no, payload in enumerate(server_payloads[1]):
                progress_bar.update(1)
                driver.switch_to.window(example)
                driver.refresh()
                payload = payload.replace(
                    "mhudogbhrqrjxjxelug",
                    f"http://127.0.0.1:8000/xss/{order}/{payload_no}",
                )

                try:
                    driver.execute_script(f"document.title = `{payload}`;")

                    # get time of injection
                    time_of_injection = dt.utcnow()

                except Exception as e:
                    error_logging(source, str(e))
                    continue

                try:
                    # Press the F12 key to open the developer tools
                    subprocess.call(["xdotool", "keydown", "F12"])
                    subprocess.call(["xdotool", "keyup", "F12"])
                except Exception as e:
                    error_logging(source, str(e))
                    continue

                driver.switch_to.window(extension)
                driver.refresh()
                driver.switch_to.window(example)

                try:
                    if "post" in payload_s[num]:
                        a = WebDriverWait(driver, 2).until(
                            EC.element_to_be_clickable((By.ID, "a"))
                        )
                        a.click()
                except:
                    pass

                url = "http://127.0.0.1:8000/data/{}/{}".format(order, payload_no)
                time.sleep(3)

                packets: list = requests.get(url).json()["data"]
                if packets != []:
                    payload_logging(
                        "SUCCESS",
                        source,
                        ext_id,
                        ext_name,
                        url_of_injection_example,
                        "server",
                        payload,
                        r"document.title = `{payload}`;",
                        time_of_injection,
                        "nil",
                        payload_file,
                        packets,
                    )
                    
                else:
                    payload_logging(
                        "FAILURE",
                        source,
                        ext_id,
                        ext_name,
                        url_of_injection_example,
                        "server",
                        payload,
                        r"document.title = `{payload}`;",
                        time_of_injection,
                        "nil",
                        payload_file,
                        packets,
                    )
                    

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
            error_logging(source, f"Failed to resolve https://www.example.com")

        except Exception as e:
            error_logging(source, str(e))
        
        

    # new chrome.Debugger.GetTargets (works)
    def chromeDebugger_url_N(args_tuple):
        (
            progress_bar,
            order,
            option,
            payloads,
            url_path,
            ext_id,
            ext_name,
            payload_file,
            result,
            server_payloads,
        ) = args_tuple

        
        progress_bar = progress_bars[order]
        
        source = "chromeTabQuery.url"

        url_of_injection_example = "https://www.example.com"

        driver = Chrome(service=Service(), options=option)
        try:
            # Navigate to example.com
            driver.get("https://www.example.com")
            # set handler for example.com
            example = driver.current_window_handle

            # Wait up to 5 seconds for the title to become "Example Domain"
            title_condition = EC.title_is("Example Domain")
            WebDriverWait(driver, 5).until(title_condition)

            # get page source code of example.com
            example_source_code = driver.page_source

            # get extension popup.html
            driver.switch_to.new_window("tab")
            extension = driver.current_window_handle
            driver.get(url_path)

            # get page source code of extension
            extension_source_code = driver.page_source

            for payload in payloads[1]:
                # update progress bar
                progress_bar.update(1)

                payload = payload.strip()

                # change to example.com to change url property
                driver.switch_to.window(example)
                driver.refresh()

                try:
                    driver.execute_script(
                        f"location.href = `https://www.example.com/?p={payload}`"
                    )

                    # get time of injection
                    time_of_injection = dt.utcnow()

                except Exception as e:
                    error_logging(source, str(e))
                    continue

                # Press the F12 key to open the developer tools
                try:
                    subprocess.call(["xdotool", "keydown", "F12"])
                    subprocess.call(["xdotool", "keyup", "F12"])
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
                    payload_logging(
                        "SUCCESS",
                        source,
                        ext_id,
                        ext_name,
                        url_of_injection_example,
                        "normal",
                        payload,
                        r"location.href = `https://www.example.com/?p={payload}`",
                        time_of_injection,
                        time_of_success,
                        payload_file,
                        "nil",
                    )
                    

                except TimeoutException:
                    payload_logging(
                        "FAILURE",
                        source,
                        ext_id,
                        ext_name,
                        url_of_injection_example,
                        "normal",
                        payload,
                        r"location.href = `https://www.example.com/?p={payload}`",
                        time_of_injection,
                        "nil",
                        payload_file,
                        "nil",
                    )
                    

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
                        payload_logging(
                            "SUCCESS",
                            source,
                            ext_id,
                            ext_name,
                            url_of_injection_example,
                            "normal",
                            payload,
                            r"location.href = `https://www.example.com/?p={payload}`",
                            time_of_injection,
                            time_of_success,
                            payload_file,
                            "nil",
                        )
                        

                    except TimeoutException:
                        payload_logging(
                            "FAILURE",
                            source,
                            ext_id,
                            ext_name,
                            url_of_injection_example,
                            "normal",
                            payload,
                            r"location.href = `https://www.example.com/?p={payload}`",
                            time_of_injection,
                            "nil",
                            payload_file,
                            "nil",
                        )
                        

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

            for payload_no, payload in enumerate(server_payloads[1]):
                progress_bar.update(1)

                driver.switch_to.window(example)
                driver.refresh()
                payload = payload.replace(
                    "mhudogbhrqrjxjxelug",
                    f"http://127.0.0.1:8000/xss/{order}/{payload_no}",
                )

                try:
                    driver.execute_script(
                        f"location.href = `https://www.example.com/?p={payload}`"
                    )

                    # get time of injection
                    time_of_injection = dt.utcnow()

                except Exception as e:
                    error_logging(source, str(e))
                    continue

                # Press the F12 key to open the developer tools
                try:
                    subprocess.call(["xdotool", "keydown", "F12"])
                    subprocess.call(["xdotool", "keyup", "F12"])
                except Exception as e:
                    error_logging(source, str(e))
                    continue

                driver.switch_to.window(extension)
                driver.refresh()
                driver.switch_to.window(example)

                try:
                    if "post" in payload_s[num]:
                        a = WebDriverWait(driver, 2).until(
                            EC.element_to_be_clickable((By.ID, "a"))
                        )
                        a.click()
                except:
                    pass

                url = "http://127.0.0.1:8000/data/{}/{}".format(order, payload_no)
                time.sleep(3)

                packets: list = requests.get(url).json()["data"]
                if packets != []:
                    payload_logging(
                        "SUCCESS",
                        source,
                        ext_id,
                        ext_name,
                        url_of_injection_example,
                        "server",
                        payload,
                        r"location.href = `https://www.example.com/?p={payload}`",
                        time_of_injection,
                        "nil",
                        payload_file,
                        packets,
                    )
                    
                else:
                    payload_logging(
                        "FAILURE",
                        source,
                        ext_id,
                        ext_name,
                        url_of_injection_example,
                        "server",
                        payload,
                        r"location.href = `https://www.example.com/?p={payload}`",
                        time_of_injection,
                        "nil",
                        payload_file,
                        packets,
                    )
                    

                try:
                    # check modifications for example.com
                    driver.switch_to.window(example)
                    if example_source_code != driver.page_source:
                        driver.get("https://www.example.com")
                except:
                    pass

                try:
                    # check modifications for extension
                    driver.switch_to.window(extension)
                    if extension_source_code != driver.page_source:
                        driver.get(url_path)
                except:
                    pass

        except TimeoutException:
            # Handle TimeoutException when title condition is not met
            error_logging(source, f"Failed to resolve https://www.example.com")

        except Exception as e:
            # Handle any other exceptions that occur
            error_logging(source, str(e))
        
        

    # new chromeDebugger_favIconUrl (works)
    def chromeDebugger_favIconUrl_N(args_tuple):
        (
            progress_bar,
            order,
            option,
            payloads,
            url_path,
            ext_id,
            ext_name,
            payload_file,
            result,
            server_payloads,
        ) = args_tuple

        
        progress_bar = progress_bars[order]

        # automatically populate server_progressbar
        progress_bar.update(server_payloads[0])

        
        source = "chromeTabsQuery.favIconUrl"

        url_of_injection_example = "DYNAMIC_ANALYSIS/miscellaneous/xss_website.html"

        driver = Chrome(service=Service(), options=option)
        dir_path = Path(
            f"DYNAMIC_ANALYSIS/miscellaneous/chromeDebuggerFiles/favIconUrl_instance_{order}"
        )

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
            pic_path = Path(
                "DYNAMIC_ANALYSIS/miscellaneous/default.png"
            )  # Specify the path of the picture you want to copy
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

        def changeFavIconUrl(driver, order, payload):
            payload = payload.strip()

            try:
                # remove current favIconUrl
                driver.execute_script(
                    """
                var linkElement = document.querySelector('link[rel="icon"]');
                if (linkElement) {
                linkElement.parentNode.removeChild(linkElement);
                }
                """
                )
            except Exception as e:
                error_logging(source, str(e))

            try:
                # set new favIconUrl
                driver.execute_script(
                    f"""
                var link = document.createElement('link');
                link.type = 'image/jpg';
                link.rel = 'icon';
                link.href = './chromeDebuggerFiles/favIconUrl_instance_{order}/{payload}.png';
                document.head.appendChild(link);
                """
                )

            except Exception as e:
                error_logging(source, str(e))

        # preconfigure files required
        access_directory()

        try:
            website = "file://" + os.path.abspath(url_of_injection_example)

            # get www.example.com
            driver.get(website)
            driver.save_screenshot("DYNAMIC_ANALYSIS/ss.png")
            # set handler for example.com
            example = driver.current_window_handle

            # Wait up to 5 seconds for the title to become "Example Domain"
            title_condition = EC.title_is("Xss Website")
            WebDriverWait(driver, 5).until(title_condition)

            # get page source code of example.com
            example_source_code = driver.page_source

            # add a default favIconUrl
            driver.execute_script(
                """
            var link = document.createElement('link');
            link.type = 'image/jpg';
            link.rel = 'icon';
            link.href = 'default.png';
            document.head.appendChild(link);
            """
            )

            # get extension popup.html
            driver.switch_to.new_window("tab")
            extension = driver.current_window_handle
            driver.get(url_path)

            # get page source code of extension
            extension_source_code = driver.page_source

            for payload in payloads[1]:
                # update progress bar
                progress_bar.update(1)

                # forbidden_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|', "'"]
                forbidden_chars = ["/", "\\", ":", "*", "?", '"', "<", ">", "|"]
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
                    subprocess.call(["xdotool", "keydown", "F12"])
                    subprocess.call(["xdotool", "keyup", "F12"])
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
                    payload_logging(
                        "SUCCESS",
                        source,
                        ext_id,
                        ext_name,
                        url_of_injection_example,
                        "normal",
                        payload,
                        r"var link = document.createElement('link');link.type = 'image/jpg';link.rel = 'icon';link.href'./chromeDebuggerFiles/favIconUrl_instance_{number}/{payload}.png';document.head.appendChild(link);",
                        time_of_injection,
                        time_of_success,
                        payload_file,
                        "nil",
                    )
                    

                except TimeoutException:
                    payload_logging(
                        "FAILURE",
                        source,
                        ext_id,
                        ext_name,
                        url_of_injection_example,
                        "normal",
                        payload,
                        r"var link = document.createElement('link');link.type = 'image/jpg';link.rel = 'icon';link.href'./chromeDebuggerFiles/favIconUrl_instance_{number}/{payload}.png';document.head.appendChild(link);",
                        time_of_injection,
                        "nil",
                        payload_file,
                        "nil",
                    )
                    

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
                        payload_logging(
                            "SUCCESS",
                            source,
                            ext_id,
                            ext_name,
                            url_of_injection_example,
                            "normal",
                            payload,
                            r"var link = document.createElement('link');link.type = 'image/jpg';link.rel = 'icon';link.href'./chromeDebuggerFiles/favIconUrl_instance_{order}/{payload}.png';document.head.appendChild(link);",
                            time_of_injection,
                            time_of_success,
                            payload_file,
                            "nil",
                        )
                        

                    except TimeoutException:
                        payload_logging(
                            "FAILURE",
                            source,
                            ext_id,
                            ext_name,
                            url_of_injection_example,
                            "normal",
                            payload,
                            r"var link = document.createElement('link');link.type = 'image/jpg';link.rel = 'icon';link.href'./chromeDebuggerFiles/favIconUrl_instance_{order}/{payload}.png';document.head.appendChild(link);",
                            time_of_injection,
                            "nil",
                            payload_file,
                            "nil",
                        )
                        

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
            error_logging(source, f"Failed to resolve {website}")

        except Exception as e:
            # Handle any other exceptions that occur
            error_logging(source, str(e))
        
        

    source = result["taintsource"]
    match source:
        case "title":
            return chromeDebugger_title_N(args_tuple)
        case "favIconUrl":
            return chromeDebugger_favIconUrl_N(args_tuple)
        case "url":
            return chromeDebugger_url_N(args_tuple)
        case _:
            progress_bar.update(payloads[0] + server_payloads[0])
            return


# new window.addEventListernerMessage (shd work (old ver))
def windowAddEventListenerMessage(args_tuple):
    (
        progress_bar,
        order,
        option,
        payloads,
        url_path,
        ext_id,
        ext_name,
        payload_file,
        result,
        server_payloads,
    ) = args_tuple

    
    source = "window.addEventListerner('message')"
    url_of_injection_example = "DYNAMIC_ANALYSIS/miscellaneous/xss_website.html"

    driver = Chrome(service=Service(), options=option)

    try:
        website = "file://" + os.path.abspath(url_of_injection_example)

        # get www.example.com
        driver.get(website)
        # set handler for example.com
        example = driver.current_window_handle

        # Wait up to 5 seconds for the title to become "Xss Website"
        title_condition = EC.title_is("Xss Website")
        WebDriverWait(driver, 5).until(title_condition)

        # get page source code of example.com
        example_source_code = driver.page_source

        # get extension popup.html
        driver.switch_to.new_window("tab")
        extension = driver.current_window_handle
        driver.get(url_path)

        # get page source code of extension
        extension_source_code = driver.page_source

        for payload in payloads[1]:
            progress_bar.update(1)

            driver.switch_to.window(example)
            driver.refresh()

            try:
                payload = payload.strip()
                taintsink = result["sink"]
                obj = {}
                script = nomagic(taintsink, payload, obj)

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
                payload_logging(
                    "SUCCESS",
                    source,
                    ext_id,
                    ext_name,
                    url_of_injection_example,
                    "normal",
                    payload,
                    r"window.postMessage({payload},'*')",
                    time_of_injection,
                    time_of_success,
                    payload_file,
                    "nil",
                )
                

            except TimeoutException:
                payload_logging(
                    "FAILURE",
                    source,
                    ext_id,
                    ext_name,
                    url_of_injection_example,
                    "normal",
                    payload,
                    r"window.postMessage({payload},'*')",
                    time_of_injection,
                    "nil",
                    payload_file,
                    "nil",
                )
                

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
                    payload_logging(
                        "SUCCESS",
                        source,
                        ext_id,
                        ext_name,
                        url_of_injection_example,
                        "normal",
                        payload,
                        r"window.postMessage({payload},'*')",
                        time_of_injection,
                        time_of_success,
                        payload_file,
                        "nil",
                    )
                    
                except TimeoutException:
                    payload_logging(
                        "FAILURE",
                        source,
                        ext_id,
                        ext_name,
                        url_of_injection_example,
                        "normal",
                        payload,
                        r"window.postMessage({payload},'*')",
                        time_of_injection,
                        "nil",
                        payload_file,
                        "nil",
                    )
                    

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

        for payload_no, payload in enumerate(server_payloads[1]):
            progress_bar.update(1)
            driver.switch_to.window(example)
            driver.refresh()
            payload = payload.replace(
                "mhudogbhrqrjxjxelug", f"http://127.0.0.1:8000/xss/{order}/{payload_no}"
            )

            try:
                payload = payload.strip()
                taintsink = result["sink"]
                obj = {}
                script = nomagic(taintsink, payload, obj)

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

            driver.switch_to.window(extension)
            driver.refresh()
            driver.switch_to.window(example)

            try:
                if "post" in payload_s[num]:
                    a = WebDriverWait(driver, 2).until(
                        EC.element_to_be_clickable((By.ID, "a"))
                    )
                    a.click()
            except:
                pass

            url = "http://127.0.0.1:8000/data/{}/{}".format(order, payload_no)
            time.sleep(3)

            packets: list = requests.get(url).json()["data"]
            if packets != []:
                payload_logging(
                    "SUCCESS",
                    source,
                    ext_id,
                    ext_name,
                    url_of_injection_example,
                    "server",
                    payload,
                    r"window.postMessage({payload},'*')",
                    time_of_injection,
                    "nil",
                    payload_file,
                    packets,
                )
                
            else:
                payload_logging(
                    "FAILURE",
                    source,
                    ext_id,
                    ext_name,
                    url_of_injection_example,
                    "server",
                    payload,
                    r"window.postMessage({payload},'*')",
                    time_of_injection,
                    "nil",
                    payload_file,
                    packets,
                )
                

            try:
                # check modifications for example.com
                driver.switch_to.window(example)
                if example_source_code != driver.page_source:
                    driver.get(website)
            except Exception as e:
                error_logging(source, str(e))

            try:
                # check modifications for extension
                driver.switch_to.window(extension)
                if extension_source_code != driver.page_source:
                    driver.get(url_path)
            except Exception as e:
                error_logging(source, str(e))

    except TimeoutException:
        # Handle TimeoutException when title condition is not met
        error_logging(source, f"Failed to resolve {website}")

    except Exception as e:
        error_logging(source, str(e))
