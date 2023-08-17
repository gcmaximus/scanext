import json
import logging
import os
import shutil
import subprocess
import urllib.parse
from functools import reduce
from pathlib import Path
from time import sleep, time

import requests
from selenium.common.exceptions import (
    JavascriptException,
    InvalidArgumentException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver import ActionChains, Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib3.exceptions import MaxRetryError, ProtocolError

from selenium.webdriver.support.select import Select


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


def nomagic(chain: str, payload: str, msg: dict):
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

    # Log
    logger.critical(
        json.dumps(
            {
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
            }
        )
    )


def error_logging(source, msg, max_chars=400):
    # Remove newline characters from the error message
    msg = str(msg).replace("\n", " ")

    # Truncate the error message to the specified maximum characters
    msg = msg[:max_chars]

    # Get logger
    logger = logging.getLogger("error")

    # Log
    # datetime = fdt(dt.now(tz(logger.timezone)))
    # logger.error(f"[{source}][{datetime}] {msg}")
    logger.error(f"[{source}] {msg}")


##########################
# Case Scenario headless #
##########################
#   Updated functions    #
##########################


# 1) runtime.onMessage
def runtime_onM(
    rlock,
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
):
    scripts = []
    scripts_s = []
    payload = {}
    payload_s = {}
    source = "chrome.runtime.onMessage"
    relative_path = "DYNAMIC_ANALYSIS/miscellaneous/example.html"
    url_of_injection_example = "file://" + os.path.abspath(relative_path)

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
                driver.switch_to.window(extension)
                driver.execute_script(script)
                time_of_injection = time()

                # check for alerts in example
                driver.switch_to.window(example)
                try:
                    # wait 2 seconds to see if alert is detected
                    WebDriverWait(driver, 2).until(EC.alert_is_present())
                    alert = driver.switch_to.alert
                    alert.accept()

                    # get time of success [2) extension]
                    time_of_success = time()

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

                # check modifications for example
                driver.switch_to.window(example)
                if example_source_code != driver.page_source:
                    driver.get(url_of_injection_example)

                # check modifications for extension
                driver.switch_to.window(extension)
                if extension_source_code != driver.page_source:
                    driver.get(url_path)

            except JavascriptException:
                pass
            except (WebDriverException, ProtocolError, MaxRetryError) as e:
                with rlock:
                    error_logging(source, f"{order} {e.__class__.__name__}")
                    driver.quit()
                    driver = Chrome(service=Service(), options=option)
                    driver.get(url_of_injection_example)
                    example_source_code = (
                        driver.page_source
                    )  # set new example page source
                    example = driver.current_window_handle  # set new example handle
                    driver.switch_to.new_window("tab")  # switch to new tab
                    driver.get(url_path)  # browse to new extension popup
                    extension = driver.current_window_handle  # set new extension handle
                    extension_source_code = (
                        driver.page_source
                    )  # set new extension page source
            except Exception as e:
                error_logging(source, f"{e.__class__.__name__}[Thd {order}]: {e}")

        for num, script in enumerate(scripts_s):
            progress_bar.update(1)
            try:
                driver.switch_to.window(extension)
                driver.execute_script(script)
                time_of_injection = time()

                driver.switch_to.window(example)

                url = "http://127.0.0.1:8000/data/{}/{}".format(order, payload_no)
                sleep(3)
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

                # check modifications for example.com
                driver.switch_to.window(example)
                if example_source_code != driver.page_source:
                    driver.get(url_of_injection_example)

                # check modifications for extension
                driver.switch_to.window(extension)
                if extension_source_code != driver.page_source:
                    driver.get(url_path)

            except JavascriptException:
                pass
            except (WebDriverException, ProtocolError, MaxRetryError) as e:
                with rlock:
                    error_logging(source, f"{order} {e.__class__.__name__}")
                    driver.quit()
                    driver = Chrome(service=Service(), options=option)
                    driver.get(url_of_injection_example)
                    example_source_code = (
                        driver.page_source
                    )  # set new example page source
                    example = driver.current_window_handle  # set new example handle
                    driver.switch_to.new_window("tab")  # switch to new tab
                    driver.get(url_path)  # browse to new extension popup
                    extension = driver.current_window_handle  # set new extension handle
                    extension_source_code = (
                        driver.page_source
                    )  # set new extension page source

            except Exception as e:
                error_logging(
                    source,
                    f"{e.__class__.__name__}[Thread {order} svr payload]: {e}",
                )
    except Exception as e:
        error_logging(source, f"{e.__class__.__name__}[Thread {order} ended]: {e}")
    finally:
        driver.quit()


# 2) runtime.onConnect
def runtime_onC(
    rlock,
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
):
    scripts = []
    scripts_s = []
    payload = {}
    payload_s = {}
    source = "chrome.runtime.onConnect"
    relative_path = "DYNAMIC_ANALYSIS/miscellaneous/example.html"
    url_of_injection_example = "file://" + os.path.abspath(relative_path)

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
                driver.switch_to.window(extension)
                driver.execute_script(script)
                time_of_injection = time()
                # check for alerts in example
                driver.switch_to.window(example)
                try:
                    # wait 2 seconds to see if alert is detected
                    WebDriverWait(driver, 2).until(EC.alert_is_present())
                    alert = driver.switch_to.alert
                    alert.accept()

                    # get time of success [2) extension]
                    time_of_success = time()
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

                # check modifications for example
                driver.switch_to.window(example)
                if example_source_code != driver.page_source:
                    driver.get(url_of_injection_example)

                # check modifications for extension
                driver.switch_to.window(extension)
                if extension_source_code != driver.page_source:
                    driver.get(url_path)

            except JavascriptException:
                pass
            except (WebDriverException, ProtocolError, MaxRetryError) as e:
                with rlock:
                    error_logging(source, f"{order} {e.__class__.__name__}")
                    driver.quit()
                    driver = Chrome(service=Service(), options=option)
                    driver.get(url_of_injection_example)
                    example_source_code = (
                        driver.page_source
                    )  # set new example page source
                    example = driver.current_window_handle  # set new example handle
                    driver.switch_to.new_window("tab")  # switch to new tab
                    driver.get(url_path)  # browse to new extension popup
                    extension = driver.current_window_handle  # set new extension handle
                    extension_source_code = (
                        driver.page_source
                    )  # set new extension page source
            except Exception as e:
                error_logging(
                    source, f"{e.__class__.__name__}[Thread {order} norm payload]: {e}"
                )

        for num, script in enumerate(scripts_s):
            progress_bar.update(1)
            try:
                driver.switch_to.window(extension)
                driver.execute_script(script)
                time_of_injection = time()

                driver.switch_to.window(example)

                url = "http://127.0.0.1:8000/data/{}/{}".format(order, payload_no)
                sleep(3)
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

                # check modifications for example.com
                driver.switch_to.window(example)
                if example_source_code != driver.page_source:
                    driver.get(url_of_injection_example)

                # check modifications for extension
                driver.switch_to.window(extension)
                if extension_source_code != driver.page_source:
                    driver.get(url_path)

            except JavascriptException:
                pass
            except (WebDriverException, ProtocolError, MaxRetryError) as e:
                with rlock:
                    error_logging(source, f"{order} {e.__class__.__name__}")
                    driver.quit()
                    driver = Chrome(service=Service(), options=option)
                    driver.get(url_of_injection_example)
                    example_source_code = (
                        driver.page_source
                    )  # set new example page source
                    example = driver.current_window_handle  # set new example handle
                    driver.switch_to.new_window("tab")  # switch to new tab
                    driver.get(url_path)  # browse to new extension popup
                    extension = driver.current_window_handle  # set new extension handle
                    extension_source_code = (
                        driver.page_source
                    )  # set new extension page source
            except Exception as e:
                error_logging(
                    source,
                    f"{e.__class__.__name__}[Thread {order} svr payload]: {e}",
                )

    except Exception as e:
        error_logging(source, f"{e.__class__.__name__}[Thread {order} ended]: {e}")
    finally:
        driver.quit()


# 3) cookies.get && cookies.getAll
def cookie_get(
    rlock,
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
):
    scripts = []
    scripts_s = []
    payload = {}
    payload_s = {}
    source = "cookies.get/cookies.getAll"
    relative_path = "DYNAMIC_ANALYSIS/miscellaneous/example.html"
    url_of_injection_example = "file://" + os.path.abspath(relative_path)

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

            try:
                # cookie case scenario will start from injecting script into example.com
                driver.switch_to.window(example)
                driver.execute_script(script)

                # get time of injection
                time_of_injection = time()

                # check for alerts in example
                try:
                    # wait 2 seconds to see if alert is detected
                    WebDriverWait(driver, 2).until(EC.alert_is_present())
                    alert = driver.switch_to.alert
                    alert.accept()

                    # get time of success [1) example]
                    time_of_success = time()
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
                        time_of_success = time()
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

                # check modifications for example
                driver.switch_to.window(example)
                if example_source_code != driver.page_source:
                    driver.get(url_of_injection_example)

                # check modifications for extension
                driver.switch_to.window(extension)
                if extension_source_code != driver.page_source:
                    driver.get(url_path)

            except JavascriptException:
                pass
            except (WebDriverException, ProtocolError, MaxRetryError) as e:
                with rlock:
                    error_logging(source, f"{order} {e.__class__.__name__}")
                    driver.quit()
                    driver = Chrome(service=Service(), options=option)
                    driver.get(url_of_injection_example)
                    example_source_code = (
                        driver.page_source
                    )  # set new example page source
                    example = driver.current_window_handle  # set new example handle
                    driver.switch_to.new_window("tab")  # switch to new tab
                    driver.get(url_path)  # browse to new extension popup
                    extension = driver.current_window_handle  # set new extension handle
                    extension_source_code = (
                        driver.page_source
                    )  # set new extension page source
            except Exception as e:
                error_logging(
                    source, f"{e.__class__.__name__}[Thread {order} norm payload]: {e}"
                )

        for num, script in enumerate(scripts_s):
            progress_bar.update(1)
            try:
                driver.switch_to.window(example)
                driver.execute_script(script)
                time_of_injection = time()

                driver.switch_to.window(extension)
                driver.refresh()
                driver.switch_to.window(example)

                url = "http://127.0.0.1:8000/data/{}/{}".format(order, payload_no)
                sleep(3)
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

                # check modifications for example.com
                driver.switch_to.window(example)
                if example_source_code != driver.page_source:
                    driver.get(url_of_injection_example)

                # check modifications for extension
                driver.switch_to.window(extension)
                if extension_source_code != driver.page_source:
                    driver.get(url_path)

            except JavascriptException:
                pass
            except (WebDriverException, ProtocolError, MaxRetryError) as e:
                with rlock:
                    error_logging(source, f"{order} {e.__class__.__name__}")
                    driver.quit()
                    driver = Chrome(service=Service(), options=option)
                    driver.get(url_of_injection_example)
                    example_source_code = (
                        driver.page_source
                    )  # set new example page source
                    example = driver.current_window_handle  # set new example handle
                    driver.switch_to.new_window("tab")  # switch to new tab
                    driver.get(url_path)  # browse to new extension popup
                    extension = driver.current_window_handle  # set new extension handle
                    extension_source_code = (
                        driver.page_source
                    )  # set new extension page source
            except Exception as e:
                error_logging(
                    source,
                    f"{e.__class__.__name__}[Thread {order} svr payload]: {e}",
                )

    except Exception as e:
        error_logging(source, f"{e.__class__.__name__}[Thread {order} ended]: {e}")
    finally:
        driver.quit()


# 4) location.hash
def location_hash(
    rlock,
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
):
    scripts = []
    scripts_s = []
    payload = {}
    payload_s = {}
    source = "location.hash"
    relative_path = "DYNAMIC_ANALYSIS/miscellaneous/example.html"
    url_of_injection_example = "file://" + os.path.abspath(relative_path)

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
            try:
                # location.hash case scenario will start from injecting script into example.com
                driver.switch_to.window(example)
                driver.execute_script(script)

                # get time of injection
                time_of_injection = time()

                # check for alerts in example (for extension, example then payload)
                try:
                    # wait 2 seconds to see if alert is detected
                    WebDriverWait(driver, 2).until(EC.alert_is_present())
                    alert = driver.switch_to.alert
                    alert.accept()
                    # get time of success [1) example]
                    time_of_success = time()
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
                        time_of_success = time()
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

                # check modifications for example
                driver.switch_to.window(example)
                if example_source_code != driver.page_source:
                    driver.get(url_of_injection_example)

                # check modifications for extension
                driver.switch_to.window(extension)
                if extension_source_code != driver.page_source:
                    driver.get(url_path)

            except JavascriptException:
                pass
            except (WebDriverException, ProtocolError, MaxRetryError) as e:
                with rlock:
                    error_logging(source, f"{order} {e.__class__.__name__}")
                    driver.quit()
                    driver = Chrome(service=Service(), options=option)
                    driver.get(url_of_injection_example)
                    example_source_code = (
                        driver.page_source
                    )  # set new example page source
                    example = driver.current_window_handle  # set new example handle
                    driver.switch_to.new_window("tab")  # switch to new tab
                    driver.get(url_path)  # browse to new extension popup
                    extension = driver.current_window_handle  # set new extension handle
                    extension_source_code = (
                        driver.page_source
                    )  # set new extension page source
            except Exception as e:
                error_logging(
                    source, f"{e.__class__.__name__}[Thread {order} norm payload]: {e}"
                )

        for num, script in enumerate(scripts_s):
            progress_bar.update(1)
            try:
                driver.switch_to.window(example)
                driver.execute_script(script)
                time_of_injection = time()

                driver.switch_to.window(extension)
                driver.refresh()
                driver.switch_to.window(example)

                url = "http://127.0.0.1:8000/data/{}/{}".format(order, payload_no)
                sleep(3)
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

                # check modifications for example.com
                driver.switch_to.window(example)
                if example_source_code != driver.page_source:
                    driver.get(url_of_injection_example)

                # check modifications for extension
                driver.switch_to.window(extension)
                if extension_source_code != driver.page_source:
                    driver.get(url_path)

            except JavascriptException:
                pass
            except (WebDriverException, ProtocolError, MaxRetryError) as e:
                with rlock:
                    error_logging(source, f"{order} {e.__class__.__name__}")
                    driver.quit()
                    driver = Chrome(service=Service(), options=option)
                    driver.get(url_of_injection_example)
                    example_source_code = (
                        driver.page_source
                    )  # set new example page source
                    example = driver.current_window_handle  # set new example handle
                    driver.switch_to.new_window("tab")  # switch to new tab
                    driver.get(url_path)  # browse to new extension popup
                    extension = driver.current_window_handle  # set new extension handle
                    extension_source_code = (
                        driver.page_source
                    )  # set new extension page source
            except Exception as e:
                error_logging(
                    source,
                    f"{e.__class__.__name__}[Thread {order} svr payload]: {e}",
                )

    except Exception as e:
        error_logging(source, f"{e.__class__.__name__}[Thread {order} ended]: {e}")
    finally:
        driver.quit()


#  5) runtime.onMessageExternal
def runtime_onME(
    rlock,
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
):
    scripts = []
    scripts_s = []
    payload = {}
    payload_s = {}
    source = "chrome.runtime.onMessageExternal"
    relative_path = "DYNAMIC_ANALYSIS/miscellaneous/example.html"
    url_of_injection_example = "file://" + os.path.abspath(relative_path)

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
            try:
                # onMessageExternal case scenario will start from injecting script into example.com
                driver.switch_to.window(example)
                driver.execute_script(script)

                # get time of injection
                time_of_injection = time()

                # check for alerts in example (for extension, example then payload)
                try:
                    # wait 2 seconds to see if alert is detected
                    WebDriverWait(driver, 2).until(EC.alert_is_present())
                    alert = driver.switch_to.alert
                    alert.accept()
                    # get time of success [1) example]
                    time_of_success = time()
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
                        time_of_success = time()
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

                # check modifications for example
                driver.switch_to.window(example)
                if example_source_code != driver.page_source:
                    driver.get(url_of_injection_example)

                # check modifications for extension
                driver.switch_to.window(extension)
                if extension_source_code != driver.page_source:
                    driver.get(url_path)

            except JavascriptException:
                pass
            except (WebDriverException, ProtocolError, MaxRetryError) as e:
                with rlock:
                    error_logging(source, f"{order} {e.__class__.__name__}")
                    driver.quit()
                    driver = Chrome(service=Service(), options=option)
                    driver.get(url_of_injection_example)
                    example_source_code = (
                        driver.page_source
                    )  # set new example page source
                    example = driver.current_window_handle  # set new example handle
                    driver.switch_to.new_window("tab")  # switch to new tab
                    driver.get(url_path)  # browse to new extension popup
                    extension = driver.current_window_handle  # set new extension handle
                    extension_source_code = (
                        driver.page_source
                    )  # set new extension page source
            except Exception as e:
                error_logging(
                    source, f"{e.__class__.__name__}[Thread {order} norm payload]: {e}"
                )

        for num, script in enumerate(scripts_s):
            progress_bar.update(1)
            try:
                driver.switch_to.window(example)
                driver.execute_script(script)
                time_of_injection = time()

                driver.switch_to.window(extension)
                driver.refresh()
                driver.switch_to.window(example)

                url = "http://127.0.0.1:8000/data/{}/{}".format(order, payload_no)
                sleep(3)
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

                # check modifications for example.com
                driver.switch_to.window(example)
                if example_source_code != driver.page_source:
                    driver.get(url_of_injection_example)

                # check modifications for extension
                driver.switch_to.window(extension)
                if extension_source_code != driver.page_source:
                    driver.get(url_path)

            except JavascriptException:
                pass
            except (WebDriverException, ProtocolError, MaxRetryError) as e:
                with rlock:
                    error_logging(source, f"{order} {e.__class__.__name__}")
                    driver.quit()
                    driver = Chrome(service=Service(), options=option)
                    driver.get(url_of_injection_example)
                    example_source_code = (
                        driver.page_source
                    )  # set new example page source
                    example = driver.current_window_handle  # set new example handle
                    driver.switch_to.new_window("tab")  # switch to new tab
                    driver.get(url_path)  # browse to new extension popup
                    extension = driver.current_window_handle  # set new extension handle
                    extension_source_code = (
                        driver.page_source
                    )  # set new extension page source
            except Exception as e:
                error_logging(
                    source,
                    f"{e.__class__.__name__}[Thread {order} svr payload]: {e}",
                )

    except Exception as e:
        error_logging(source, f"{e.__class__.__name__}[Thread {order} ended]: {e}")
    finally:
        driver.quit()


# 6) runtime.onConnectExternal
def runtime_onCE(
    rlock,
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
):
    scripts = []
    scripts_s = []
    payload = {}
    payload_s = {}
    source = "chrome.runtime.onConnectExternal"
    relative_path = "DYNAMIC_ANALYSIS/miscellaneous/example.html"
    url_of_injection_example = "file://" + os.path.abspath(relative_path)

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
            try:
                # onConnectExternal case scenario will start from injecting script into example.com
                driver.switch_to.window(example)
                driver.execute_script(script)

                # get time of injection
                time_of_injection = time()

                # check for alerts in example (for extension, example then payload)
                try:
                    # wait 2 seconds to see if alert is detected
                    WebDriverWait(driver, 2).until(EC.alert_is_present())
                    alert = driver.switch_to.alert
                    alert.accept()
                    # get time of success [1) example]
                    time_of_success = time()
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
                        time_of_success = time()
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

                # check modifications for example
                driver.switch_to.window(example)
                if example_source_code != driver.page_source:
                    driver.get(url_of_injection_example)

                # check modifications for extension
                driver.switch_to.window(extension)
                if extension_source_code != driver.page_source:
                    driver.get(url_path)

            except JavascriptException:
                pass
            except (WebDriverException, ProtocolError, MaxRetryError) as e:
                with rlock:
                    error_logging(source, f"{order} {e.__class__.__name__}")
                    driver.quit()
                    driver = Chrome(service=Service(), options=option)
                    driver.get(url_of_injection_example)
                    example_source_code = (
                        driver.page_source
                    )  # set new example page source
                    example = driver.current_window_handle  # set new example handle
                    driver.switch_to.new_window("tab")  # switch to new tab
                    driver.get(url_path)  # browse to new extension popup
                    extension = driver.current_window_handle  # set new extension handle
                    extension_source_code = (
                        driver.page_source
                    )  # set new extension page source
            except Exception as e:
                error_logging(
                    source, f"{e.__class__.__name__}[Thread {order} norm payload]: {e}"
                )

        for num, script in enumerate(scripts_s):
            progress_bar.update(1)
            try:
                driver.switch_to.window(example)
                driver.execute_script(script)
                time_of_injection = time()

                driver.switch_to.window(extension)
                driver.refresh()
                driver.switch_to.window(example)

                url = "http://127.0.0.1:8000/data/{}/{}".format(order, payload_no)
                sleep(3)
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

                # check modifications for example.com
                driver.switch_to.window(example)
                if example_source_code != driver.page_source:
                    driver.get(url_of_injection_example)

                # check modifications for extension
                driver.switch_to.window(extension)
                if extension_source_code != driver.page_source:
                    driver.get(url_path)

            except JavascriptException:
                pass
            except (WebDriverException, ProtocolError, MaxRetryError) as e:
                with rlock:
                    error_logging(source, f"{order} {e.__class__.__name__}")
                    driver.quit()
                    driver = Chrome(service=Service(), options=option)
                    driver.get(url_of_injection_example)
                    example_source_code = (
                        driver.page_source
                    )  # set new example page source
                    example = driver.current_window_handle  # set new example handle
                    driver.switch_to.new_window("tab")  # switch to new tab
                    driver.get(url_path)  # browse to new extension popup
                    extension = driver.current_window_handle  # set new extension handle
                    extension_source_code = (
                        driver.page_source
                    )  # set new extension page source
            except Exception as e:
                error_logging(
                    source,
                    f"{e.__class__.__name__}[Thread {order} svr payload]: {e}",
                )

    except Exception as e:
        error_logging(source, f"{e.__class__.__name__}[Thread {order} ended]: {e}")
    finally:
        driver.quit()


# new window.name_normal (works)
def window_name_N(
    rlock,
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
):
    source = "window.name"
    relative_path = "DYNAMIC_ANALYSIS/miscellaneous/example.html"
    url_of_injection_example = "file://" + os.path.abspath(relative_path)

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

        for payload_no, payload in enumerate(payloads[1]):
            # update progress bar
            progress_bar.update(1)

            try:
                # since window.name is obtained from the website url, we will inject javascript to change the window.name
                driver.switch_to.window(example)

                driver.execute_script(f"window.name = `{payload}`;")

                # get time of injection
                time_of_injection = time()

                # observe behavior after payload injection
                # check for alerts in example
                try:
                    # wait 2 seconds to see if alert is detected
                    WebDriverWait(driver, 2).until(EC.alert_is_present())
                    alert = driver.switch_to.alert
                    alert.accept()

                    # get time of success [1) example]
                    time_of_success = time()
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
                        time_of_success = time()
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

                # check modifications for example
                driver.switch_to.window(example)
                if example_source_code != driver.page_source:
                    driver.get(url_of_injection_example)

                # check modifications for extension
                driver.switch_to.window(extension)
                if extension_source_code != driver.page_source:
                    driver.get(url_path)

            except JavascriptException:
                pass
            except (WebDriverException, ProtocolError, MaxRetryError) as e:
                with rlock:
                    error_logging(source, f"{order} {e.__class__.__name__}")
                    driver.quit()
                    driver = Chrome(service=Service(), options=option)
                    driver.get(url_of_injection_example)
                    example_source_code = (
                        driver.page_source
                    )  # set new example page source
                    example = driver.current_window_handle  # set new example handle
                    driver.switch_to.new_window("tab")  # switch to new tab
                    driver.get(url_path)  # browse to new extension popup
                    extension = driver.current_window_handle  # set new extension handle
                    extension_source_code = (
                        driver.page_source
                    )  # set new extension page source
            except Exception as e:
                error_logging(
                    source, f"{e.__class__.__name__}[Thread {order} norm payload]: {e}"
                )

        for payload_no, payload in enumerate(server_payloads[1]):
            progress_bar.update(1)
            payload = payload.replace(
                "mhudogbhrqrjxjxelug", f"http://127.0.0.1:8000/xss/{order}/{payload_no}"
            )
            try:
                # since window.name is obtained from the website url, we will inject javascript to change the window.name
                driver.switch_to.window(example)
                driver.refresh()

                driver.execute_script(f"window.name = `{payload}`;")
                # get time of injection
                time_of_injection = time()

                driver.switch_to.window(extension)
                driver.refresh()
                driver.switch_to.window(example)

                url = "http://127.0.0.1:8000/data/{}/{}".format(order, payload_no)
                sleep(3)

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

                # check modifications for example.com
                driver.switch_to.window(example)
                if example_source_code != driver.page_source:
                    driver.get(url_of_injection_example)

                # check modifications for extension
                driver.switch_to.window(extension)
                if extension_source_code != driver.page_source:
                    driver.get(url_path)

            except JavascriptException:
                pass
            except (WebDriverException, ProtocolError, MaxRetryError) as e:
                with rlock:
                    error_logging(source, f"{order} {e.__class__.__name__}")
                    driver.quit()
                    driver = Chrome(service=Service(), options=option)
                    driver.get(url_of_injection_example)
                    example_source_code = (
                        driver.page_source
                    )  # set new example page source
                    example = driver.current_window_handle  # set new example handle
                    driver.switch_to.new_window("tab")  # switch to new tab
                    driver.get(url_path)  # browse to new extension popup
                    extension = driver.current_window_handle  # set new extension handle
                    extension_source_code = (
                        driver.page_source
                    )  # set new extension page source
            except Exception as e:
                error_logging(
                    source,
                    f"{e.__class__.__name__}[Thread {order} svr payload]: {e}",
                )

    except Exception as e:
        error_logging(source, f"{e.__class__.__name__}[Thread {order} ended]: {e}")
    finally:
        driver.quit()


# new location.href_normal (works)
def location_href_N(
    rlock,
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
):
    source = "location.href"
    relative_path = "DYNAMIC_ANALYSIS/miscellaneous/example.html"
    url_of_injection_example = "file://" + os.path.abspath(relative_path)

    driver = Chrome(service=Service(), options=option)
    try:
        # Navigate to example.com
        driver.get(url_of_injection_example)
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
            scripts = (
                f"location.href = `{url_of_injection_example}/?p={payload}`",
                f"location.href = `{url_of_injection_example}/#{payload}`",
            )

            # we can inject a script to change the location.href variable using query parameters or fragment Idenfiers
            for j in scripts:
                try:
                    driver.switch_to.window(extension)
                    driver.refresh()
                    driver.switch_to.window(example)

                    driver.execute_script(j)

                    # get time of injection
                    time_of_injection = time()

                    # observe behavior after payload injection

                    # 1) Check for alerts in example
                    try:
                        # wait 2 seconds to see if alert is detected
                        WebDriverWait(driver, 2).until(EC.alert_is_present())
                        alert = driver.switch_to.alert
                        alert.accept()

                        time_of_success = time()
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

                        time_of_success = time()
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

                    # check modifications for example
                    driver.switch_to.window(example)
                    if example_source_code != driver.page_source:
                        driver.get(url_of_injection_example)

                    # check modifications for extension
                    driver.switch_to.window(extension)
                    if extension_source_code != driver.page_source:
                        driver.get(url_path)
                except JavascriptException:
                    pass
                except (WebDriverException, ProtocolError, MaxRetryError) as e:
                    with rlock:
                        error_logging(source, f"{order} {e.__class__.__name__}")
                        driver.quit()
                        driver = Chrome(service=Service(), options=option)
                        driver.get(url_of_injection_example)
                        example_source_code = (
                            driver.page_source
                        )  # set new example page source
                        example = driver.current_window_handle  # set new example handle
                        driver.switch_to.new_window("tab")  # switch to new tab
                        driver.get(url_path)  # browse to new extension popup
                        extension = (
                            driver.current_window_handle
                        )  # set new extension handle
                        extension_source_code = (
                            driver.page_source
                        )  # set new extension page source

                except Exception as e:
                    error_logging(
                        source,
                        f"{e.__class__.__name__}[Thread {order} norm payload]: {e}",
                    )

        for payload_no, payload in enumerate(server_payloads[1]):
            progress_bar.update(1)
            payload = payload.replace(
                "mhudogbhrqrjxjxelug", f"http://127.0.0.1:8000/xss/{order}/{payload_no}"
            )

            try:
                driver.switch_to.window(example)
                driver.refresh()
                driver.execute_script(
                    f"location.href = `https://www.example.com/?p={payload}`"
                )

                # get time of injection
                time_of_injection = time()

                driver.switch_to.window(extension)
                driver.refresh()
                driver.switch_to.window(example)

                url = "http://127.0.0.1:8000/data/{}/{}".format(order, payload_no)
                sleep(3)

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

                # check modifications for example.com
                driver.switch_to.window(example)
                if example_source_code != driver.page_source:
                    driver.get("https://www.example.com")

                # check modifications for extension
                driver.switch_to.window(extension)
                if extension_source_code != driver.page_source:
                    driver.get(url_path)

            except JavascriptException:
                pass
            except (WebDriverException, ProtocolError, MaxRetryError) as e:
                with rlock:
                    error_logging(source, f"{order} {e.__class__.__name__}")
                    driver.quit()
                    driver = Chrome(service=Service(), options=option)
                    driver.get(url_of_injection_example)
                    example_source_code = (
                        driver.page_source
                    )  # set new example page source
                    example = driver.current_window_handle  # set new example handle
                    driver.switch_to.new_window("tab")  # switch to new tab
                    driver.get(url_path)  # browse to new extension popup
                    extension = driver.current_window_handle  # set new extension handle
                    extension_source_code = (
                        driver.page_source
                    )  # set new extension page source
            except Exception as e:
                error_logging(
                    source,
                    f"{e.__class__.__name__}[Thread {order} svr payload]: {e}",
                )

    except Exception as e:
        error_logging(source, f"{e.__class__.__name__}[Thread {order} ended]: {e}")
    finally:
        driver.quit()


# combined contextMenu
def context_menu(
    rlock,
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
):
    # save args
    args = locals()
    url_of_injection_example = "DYNAMIC_ANALYSIS/miscellaneous/xss_website.html"
    website = "file://" + os.path.abspath(url_of_injection_example)

    # new contextMenu.selectionText_normal (works)
    def context_menu_selectionText_N(
        rlock,
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
    ):
        source = "contextMenu.selectionText"

        driver = Chrome(service=Service(), options=option)
        try:
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
                # update progress bar
                progress_bar.update(1)

                try:
                    driver.switch_to.window(example)

                    driver.execute_script(
                        f'document.getElementById("h1_element").innerText = `{payload}`'
                    )

                    # get time of injection
                    time_of_injection = time()

                    target_element = driver.find_element(By.ID, "h1_element")

                    # Select the text using JavaScript
                    driver.execute_script(
                        "window.getSelection().selectAllChildren(arguments[0]);",
                        target_element,
                    )

                    # usage of context menu
                    actions = ActionChains(driver)
                    actions.context_click(target_element).perform()

                    # driver.save_screenshot('DYNAMIC_ANALYSIS/ss.png')

                    for _ in range(6):
                        with rlock:
                            subprocess.call(["xdotool", "key", "Down"])

                    # Simulate pressing the "Enter" key
                    with rlock:
                        subprocess.call(["xdotool", "key", "Return"])
                    # observe behavior after payload injection
                    # 1) Check for alerts in example.com
                    try:
                        # wait 2 seconds to see if alert is detected
                        WebDriverWait(driver, 2).until(EC.alert_is_present())
                        alert = driver.switch_to.alert
                        alert.accept()

                        time_of_success = time()
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

                            time_of_success = time()
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
                    # [1] check modifications for example.com
                    driver.switch_to.window(example)
                    if example_source_code != driver.page_source:
                        driver.get(website)

                    # [2] check modifications for extension
                    driver.switch_to.window(extension)
                    if extension_source_code != driver.page_source:
                        driver.get(url_path)

                except JavascriptException:
                    pass
                except (WebDriverException, ProtocolError, MaxRetryError) as e:
                    with rlock:
                        error_logging(source, f"{order} {e.__class__.__name__}")
                        driver.quit()
                        driver = Chrome(service=Service(), options=option)
                        driver.get(url_of_injection_example)
                        example_source_code = (
                            driver.page_source
                        )  # set new example page source
                        example = driver.current_window_handle  # set new example handle
                        driver.switch_to.new_window("tab")  # switch to new tab
                        driver.get(url_path)  # browse to new extension popup
                        extension = (
                            driver.current_window_handle
                        )  # set new extension handle
                        extension_source_code = (
                            driver.page_source
                        )  # set new extension page source

                except Exception as e:
                    error_logging(
                        source,
                        f"{e.__class__.__name__}[Thread {order} norm payload]: {e}",
                    )

            for payload_no, payload in enumerate(server_payloads[1]):
                progress_bar.update(1)
                payload = payload.replace(
                    "mhudogbhrqrjxjxelug",
                    f"http://127.0.0.1:8000/xss/{order}/{payload_no}",
                )

                # inject
                try:
                    driver.switch_to.window(example)
                    driver.refresh()
                    driver.execute_script(
                        f'document.getElementById("h1_element").innerText = `{payload}`'
                    )

                    # get time of injection
                    time_of_injection = time()

                    target_element = driver.find_element(By.ID, "h1_element")

                    # select element
                    # Select the text using JavaScript
                    driver.execute_script(
                        "window.getSelection().selectAllChildren(arguments[0]);",
                        target_element,
                    )

                    # usage of context menu
                    actions = ActionChains(driver)
                    actions.context_click(target_element).perform()

                    for _ in range(6):
                        with rlock:
                            subprocess.call(["xdotool", "key", "Down"])

                    # Simulate pressing the "Enter" key
                    with rlock:
                        subprocess.call(["xdotool", "key", "Return"])

                    driver.switch_to.window(extension)
                    driver.refresh()
                    driver.switch_to.window(example)

                    url = "http://127.0.0.1:8000/data/{}/{}".format(order, payload_no)
                    sleep(3)
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
                    # [1] check modifications for example.com
                    driver.switch_to.window(example)
                    if example_source_code != driver.page_source:
                        driver.get(website)

                    # [2] check modifications for extension
                    driver.switch_to.window(extension)
                    if extension_source_code != driver.page_source:
                        driver.get(url_path)
                        # print(f"Navigated back to '{url_path}' due to extension page source changes")

                except JavascriptException:
                    pass
                except (WebDriverException, ProtocolError, MaxRetryError) as e:
                    with rlock:
                        error_logging(source, f"{order} {e.__class__.__name__}")
                        driver.quit()
                        driver = Chrome(service=Service(), options=option)
                        driver.get(url_of_injection_example)
                        example_source_code = (
                            driver.page_source
                        )  # set new example page source
                        example = driver.current_window_handle  # set new example handle
                        driver.switch_to.new_window("tab")  # switch to new tab
                        driver.get(url_path)  # browse to new extension popup
                        extension = (
                            driver.current_window_handle
                        )  # set new extension handle
                        extension_source_code = (
                            driver.page_source
                        )  # set new extension page source
                except Exception as e:
                    error_logging(
                        source,
                        f"{e.__class__.__name__}[Thread {order} svr payload]: {e}",
                    )

        except Exception as e:
            error_logging(source, f"{e.__class__.__name__}[Thread {order} ended]: {e}")
        finally:
            driver.quit()

    # new contextMenu.link_Url (works)
    def context_menu_link_url_N(
        rlock,
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
    ):
        source = "contextMenu.linkUrl"

        driver = Chrome(service=Service(), options=option)

        try:
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

            for payload in payloads[1]:
                # update progress bar
                progress_bar.update(1)
                cases = {
                    r'var linkElement = document.getElementById("linkUrl"); linkElement.href = `{payload}`': f'var linkElement = document.getElementById("linkUrl"); linkElement.href = `{payload}`',
                    r'var linkElement = document.getElementById("linkUrl"); linkElement.href = "?q=" + `{}`': 'var linkElement = document.getElementById("linkUrl"); linkElement.href = "?q=" + `{}`'.format(
                        payload.replace('"', '\\"').replace("'", "\\'")
                    ),
                }

                # there are 2 possible ways to insert paylaod, either directly or using query parameters.
                for i, j in cases.items():
                    try:
                        # for link url, inject our payload into the link.
                        driver.switch_to.window(example)

                        # using selenium to find element by ID
                        target_element = driver.find_element(By.ID, "linkUrl")

                        # Payload Injection (Href)
                        # PAYLOAD INJECTION CASE 1 (Directly Injecting)
                        script = i
                        driver.execute_script(j)

                        # get time of injection
                        time_of_injection = time()

                        # Seleting Text using javascript

                        # perform text highlight/selection
                        driver.execute_script(
                            "window.getSelection().selectAllChildren(arguments[0]);",
                            target_element,
                        )

                        # usage of context menu
                        # perform right click to open context menu
                        actions = ActionChains(driver)
                        actions.context_click(target_element).perform()

                        # navigate to extension context menu option
                        for _ in range(11):
                            with rlock:
                                subprocess.call(["xdotool", "key", "Down"])

                        # Simulate pressing the "Enter" key
                        with rlock:
                            subprocess.call(["xdotool", "key", "Return"])

                        # observe behavior after payload injection
                        # 1) Check for alerts in example.com
                        driver.switch_to.window(example)

                        try:
                            # wait 2 seconds to see if alert is detected
                            WebDriverWait(driver, 2).until(EC.alert_is_present())
                            alert = driver.switch_to.alert
                            alert.accept()

                            time_of_success = time()
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

                                time_of_success = time()
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
                        # [1] check modifications for example.com
                        driver.switch_to.window(example)
                        if example_source_code != driver.page_source:
                            driver.get(website)

                        # [2] check modifications for extension
                        driver.switch_to.window(extension)
                        if extension_source_code != driver.page_source:
                            driver.get(url_path)

                    except JavascriptException:
                        pass
                    except (WebDriverException, ProtocolError, MaxRetryError) as e:
                        with rlock:
                            error_logging(source, f"{order} {e.__class__.__name__}")
                            driver.quit()
                            driver = Chrome(service=Service(), options=option)
                            driver.get(url_of_injection_example)
                            example_source_code = (
                                driver.page_source
                            )  # set new example page source
                            example = (
                                driver.current_window_handle
                            )  # set new example handle
                            driver.switch_to.new_window("tab")  # switch to new tab
                            driver.get(url_path)  # browse to new extension popup
                            extension = (
                                driver.current_window_handle
                            )  # set new extension handle
                            extension_source_code = (
                                driver.page_source
                            )  # set new extension page source

                    except Exception as e:
                        error_logging(
                            source,
                            f"{e.__class__.__name__}[Thread {order} norm payload]: {e}",
                        )

            for payload_no, payload in enumerate(server_payloads[1]):
                progress_bar.update(1)

                payload = payload.replace(
                    "mhudogbhrqrjxjxelug",
                    f"http://127.0.0.1:8000/xss/{order}/{payload_no}",
                )
                try:
                    driver.switch_to.window(example)
                    # using selenium to find element by ID
                    target_element = driver.find_element(By.ID, "linkUrl")

                    driver.execute_script(
                        f'var linkElement = document.getElementById("linkUrl"); linkElement.href = `{payload}`'
                    )

                    # get time of injection
                    time_of_injection = time()

                    # Seleting Text using javascript
                    # perform text highlight/selection
                    driver.execute_script(
                        "window.getSelection().selectAllChildren(arguments[0]);",
                        target_element,
                    )

                    # usage of context menu
                    # perform right click to open context menu
                    actions = ActionChains(driver)
                    actions.context_click(target_element).perform()

                    # navigate to extension context menu option
                    for _ in range(11):
                        with rlock:
                            subprocess.call(["xdotool", "key", "Down"])

                    # Simulate pressing the "Enter" key
                    with rlock:
                        subprocess.call(["xdotool", "key", "Return"])

                    driver.switch_to.window(extension)
                    driver.refresh()
                    driver.switch_to.window(example)

                    url = "http://127.0.0.1:8000/data/{}/{}".format(order, payload_no)
                    sleep(3)

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
                    # [1] check modifications for example.com
                    driver.switch_to.window(example)
                    if example_source_code != driver.page_source:
                        driver.get(website)

                    # [2] check modifications for extension
                    driver.switch_to.window(extension)
                    if extension_source_code != driver.page_source:
                        driver.get(url_path)

                except JavascriptException:
                    pass
                except (WebDriverException, ProtocolError, MaxRetryError) as e:
                    with rlock:
                        error_logging(source, f"{order} {e.__class__.__name__}")
                        driver.quit()
                        driver = Chrome(service=Service(), options=option)
                        driver.get(url_of_injection_example)
                        example_source_code = (
                            driver.page_source
                        )  # set new example page source
                        example = driver.current_window_handle  # set new example handle
                        driver.switch_to.new_window("tab")  # switch to new tab
                        driver.get(url_path)  # browse to new extension popup
                        extension = (
                            driver.current_window_handle
                        )  # set new extension handle
                        extension_source_code = (
                            driver.page_source
                        )  # set new extension page source
                except Exception as e:
                    error_logging(
                        source,
                        f"{e.__class__.__name__}[Thread {order} svr payload]: {e}",
                    )

        except Exception as e:
            error_logging(source, f"{e.__class__.__name__}[Thread {order} ended]: {e}")
        finally:
            driver.quit()

    # new contextMenu.srcUrl (works)
    def context_menu_src_url_N(
        rlock,
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
    ):
        source = "contextMenu.srcUrl"

        driver = Chrome(service=Service(), options=option)

        try:
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

                try:
                    driver.switch_to.window(example)
                    # using javascript, change the SRC value of an oredefined image element
                    target_element = driver.find_element(By.ID, "srcUrl")
                    driver.execute_script(
                        f"document.getElementById('srcUrl').src = `{payload}`"
                    )

                    # get time of injection
                    time_of_injection = time()
                    # usage of contextMenu
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
                    sleep(1)
                    for _ in range(7):
                        with rlock:
                            subprocess.call(["xdotool", "key", "Down"])

                    # Simulate pressing the "Enter" key
                    with rlock:
                        subprocess.call(["xdotool", "key", "Return"])

                    # observe behavior after payload injection
                    # 1) check for alerts in example
                    try:
                        # wait 2 seconds to see if alert is detected
                        WebDriverWait(driver, 2).until(EC.alert_is_present())
                        alert = driver.switch_to.alert
                        alert.accept()

                        time_of_success = time()
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

                            time_of_success = time()
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

                    # check modifications for example.com
                    driver.switch_to.window(example)
                    if example_source_code != driver.page_source:
                        driver.get(website)

                    # check modifications for extension
                    driver.switch_to.window(extension)
                    if extension_source_code != driver.page_source:
                        driver.get(url_path)

                except JavascriptException:
                    pass
                except (WebDriverException, ProtocolError, MaxRetryError) as e:
                    with rlock:
                        error_logging(source, f"{order} {e.__class__.__name__}")
                        driver.quit()
                        driver = Chrome(service=Service(), options=option)
                        driver.get(url_of_injection_example)
                        example_source_code = (
                            driver.page_source
                        )  # set new example page source
                        example = driver.current_window_handle  # set new example handle
                        driver.switch_to.new_window("tab")  # switch to new tab
                        driver.get(url_path)  # browse to new extension popup
                        extension = (
                            driver.current_window_handle
                        )  # set new extension handle
                        extension_source_code = (
                            driver.page_source
                        )  # set new extension page source

                except Exception as e:
                    error_logging(
                        source,
                        f"{e.__class__.__name__}[Thread {order} norm payload]: {e}",
                    )

            for payload_no, payload in enumerate(server_payloads[1]):
                progress_bar.update(1)
                payload = payload.replace(
                    "mhudogbhrqrjxjxelug",
                    f"http://127.0.0.1:8000/xss/{order}/{payload_no}",
                )
                try:
                    driver.switch_to.window(example)
                    driver.refresh()
                    # using javascript, change the SRC value of an oredefined image element
                    target_element = driver.find_element(By.ID, "srcUrl")
                    driver.execute_script(
                        f"document.getElementById('srcUrl').src = `{payload}`"
                    )

                    # get time of injection
                    time_of_injection = time()

                    # usage of contextMenu
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
                    sleep(1)
                    for _ in range(7):
                        with rlock:
                            subprocess.call(["xdotool", "key", "Down"])

                    # Simulate pressing the "Enter" key
                    with rlock:
                        subprocess.call(["xdotool", "key", "Return"])

                    driver.switch_to.window(extension)
                    driver.refresh()
                    driver.switch_to.window(example)

                    url = "http://127.0.0.1:8000/data/{}/{}".format(order, payload_no)
                    sleep(3)

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

                    # check modifications for example.com
                    driver.switch_to.window(example)
                    if example_source_code != driver.page_source:
                        driver.get(website)

                    # check modifications for extension
                    driver.switch_to.window(extension)
                    if extension_source_code != driver.page_source:
                        driver.get(url_path)

                except JavascriptException:
                    pass
                except (WebDriverException, ProtocolError, MaxRetryError) as e:
                    with rlock:
                        error_logging(source, f"{order} {e.__class__.__name__}")
                        driver.quit()
                        driver = Chrome(service=Service(), options=option)
                        driver.get(url_of_injection_example)
                        example_source_code = (
                            driver.page_source
                        )  # set new example page source
                        example = driver.current_window_handle  # set new example handle
                        driver.switch_to.new_window("tab")  # switch to new tab
                        driver.get(url_path)  # browse to new extension popup
                        extension = (
                            driver.current_window_handle
                        )  # set new extension handle
                        extension_source_code = (
                            driver.page_source
                        )  # set new extension page source
                except Exception as e:
                    error_logging(
                        source,
                        f"{e.__class__.__name__}[Thread {order} svr payload]: {e}",
                    )

        except Exception as e:
            error_logging(source, f"{e.__class__.__name__}[Thread {order} ended]: {e}")
        finally:
            driver.quit()

    # new contextMenu.frameUrl (works for jerald but not for me. smlj)
    def context_menu_frame_url_N(
        rlock,
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
    ):
        source = "contextMenu.frameUrl"

        driver = Chrome(service=Service(), options=option)

        try:
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

            for payload in payloads[1]:
                # update progress bar
                progress_bar.update(1)
                cases = {
                    r'var frameElement = document.getElementById("frameUrl"); frameElement.src = `https://www.example_xss.com/XSS?q={payload}`;': f'var frameElement = document.getElementById("frameUrl"); frameElement.src = `https://www.example_xss.com/XSS?q={payload}`',
                    r'var frameElement = document.getElementById("frameUrl"); frameElement.src = `https://www.example_xss.com/XSS#{payload}`;': f'var frameElement = document.getElementById("frameUrl"); frameElement.src = `https://www.example_xss.com/XSS#{payload}`',
                }

                for i, j in cases.items():
                    try:
                        driver.switch_to.window(example)

                        # using selenium to find element by ID
                        iframeElement = driver.find_element(By.ID, "frameUrl")

                        driver.execute_script(j)
                        script = i
                        # get time of injection
                        time_of_injection = time()

                        # usage of context menu
                        # # perform right click to open context menu
                        actions = ActionChains(driver)
                        actions.move_to_element(iframeElement)
                        actions.context_click().perform()

                        # navigate to extension context menu option

                        for _ in range(8):
                            with rlock:
                                subprocess.call(["xdotool", "key", "Down"])

                        # Simulate pressing the "Enter" key
                        with rlock:
                            subprocess.call(["xdotool", "key", "Return"])

                        # observe behavior after payload injection
                        # 1) Check for alerts in example.com
                        driver.switch_to.window(example)

                        try:
                            # wait 2 seconds to see if alert is detected
                            WebDriverWait(driver, 2).until(EC.alert_is_present())
                            alert = driver.switch_to.alert
                            alert.accept()

                            time_of_success = time()
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

                                time_of_success = time()
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
                        # [1] check modifications for example.com
                        driver.switch_to.window(example)
                        if example_source_code != driver.page_source:
                            driver.get(website)

                        # [2] check modifications for extension
                        driver.switch_to.window(extension)
                        if extension_source_code != driver.page_source:
                            driver.get(url_path)

                    except JavascriptException:
                        pass
                    except (WebDriverException, ProtocolError, MaxRetryError) as e:
                        with rlock:
                            error_logging(source, f"{order} {e.__class__.__name__}")
                            driver.quit()
                            driver = Chrome(service=Service(), options=option)
                            driver.get(url_of_injection_example)
                            example_source_code = (
                                driver.page_source
                            )  # set new example page source
                            example = (
                                driver.current_window_handle
                            )  # set new example handle
                            driver.switch_to.new_window("tab")  # switch to new tab
                            driver.get(url_path)  # browse to new extension popup
                            extension = (
                                driver.current_window_handle
                            )  # set new extension handle
                            extension_source_code = (
                                driver.page_source
                            )  # set new extension page source

                    except Exception as e:
                        error_logging(
                            source,
                            f"{e.__class__.__name__}[Thread {order} norm payload]: {e}",
                        )

            for payload_no, payload in enumerate(server_payloads[1]):
                progress_bar.update(1)
                payload = payload.replace(
                    "mhudogbhrqrjxjxelug",
                    f"http://127.0.0.1:8000/xss/{order}/{payload_no}",
                )

                try:
                    driver.switch_to.window(example)
                    iframeElement = driver.find_element(By.ID, "frameUrl")
                    driver.execute_script(
                        f'var frameElement = document.getElementById("frameUrl"); frameElement.src = `https://www.example_xss.com/XSS?q={payload}`'
                    )
                    # get time of injection
                    time_of_injection = time()

                    # usage of context menu
                    # # perform right click to open context menu
                    actions = ActionChains(driver)
                    actions.move_to_element(iframeElement)
                    actions.context_click().perform()

                    # navigate to extension context menu option

                    for _ in range(8):
                        with rlock:
                            subprocess.call(["xdotool", "key", "Down"])

                    # Simulate pressing the "Enter" key
                    with rlock:
                        subprocess.call(["xdotool", "key", "Return"])

                    driver.switch_to.window(extension)
                    driver.refresh()
                    driver.switch_to.window(example)

                    url = "http://127.0.0.1:8000/data/{}/{}".format(order, payload_no)
                    sleep(3)

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

                    # check for any modifications (snapshot back to original)
                    # [1] check modifications for example.com
                    driver.switch_to.window(example)
                    if example_source_code != driver.page_source:
                        driver.get(website)

                    # [2] check modifications for extension
                    driver.switch_to.window(extension)
                    if extension_source_code != driver.page_source:
                        driver.get(url_path)

                except JavascriptException:
                    pass
                except (WebDriverException, ProtocolError, MaxRetryError) as e:
                    with rlock:
                        error_logging(source, f"{order} {e.__class__.__name__}")
                        driver.quit()
                        driver = Chrome(service=Service(), options=option)
                        driver.get(url_of_injection_example)
                        example_source_code = (
                            driver.page_source
                        )  # set new example page source
                        example = driver.current_window_handle  # set new example handle
                        driver.switch_to.new_window("tab")  # switch to new tab
                        driver.get(url_path)  # browse to new extension popup
                        extension = (
                            driver.current_window_handle
                        )  # set new extension handle
                        extension_source_code = (
                            driver.page_source
                        )  # set new extension page source
                except Exception as e:
                    error_logging(
                        source,
                        f"{e.__class__.__name__}[Thread {order} svr payload]: {e}",
                    )

        except Exception as e:
            error_logging(source, f"{e.__class__.__name__}[Thread {order} ended]: {e}")
        finally:
            driver.quit()

    # new contextMenu.pageUrl (works)
    def context_menu_pageUrl_N(
        rlock,
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
    ):
        source = "contextMenu.pageUrl"

        driver = Chrome(service=Service(), options=option)

        try:
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

            for payload in payloads[1]:
                # update progress bar
                progress_bar.update(1)

                # url encode xss payload
                encoded_payload = urllib.parse.quote(payload)

                cases = {
                    r"window.history.replaceState(null, null, `{website}?qureyParam={encoded_payload}`);": f"window.history.replaceState(null, null, `{website}?qureyParam={encoded_payload}`)",
                    r"window.history.replaceState(null, null, `{website}#{encoded_payload}`);": f"window.history.replaceState(null, null, `{website}#{encoded_payload}`)",
                }

                for i, j in cases.items():
                    try:
                        driver.switch_to.window(example)
                        driver.execute_script(j)
                        script = i
                        # get time of injection
                        time_of_injection = time()

                        PageUrlElement = driver.find_element(By.ID, "pageUrl")
                        # usage of context menu
                        # # perform right click to open context menu
                        actions = ActionChains(driver)
                        actions.move_to_element(PageUrlElement)
                        actions.context_click().perform()

                        for _ in range(8):
                            with rlock:
                                subprocess.call(["xdotool", "key", "Down"])

                        # Simulate pressing the "Enter" key
                        with rlock:
                            subprocess.call(["xdotool", "key", "Return"])

                        # observe behavior after payload injection
                        # 1) Check for alerts in example.com
                        driver.switch_to.window(example)
                        try:
                            # wait 2 seconds to see if alert is detected
                            WebDriverWait(driver, 2).until(EC.alert_is_present())
                            alert = driver.switch_to.alert
                            alert.accept()

                            time_of_success = time()
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

                                time_of_success = time()
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
                        # [1] check modifications for example.com
                        driver.switch_to.window(example)
                        if example_source_code != driver.page_source:
                            driver.get(website)

                        # [2] check modifications for extension
                        driver.switch_to.window(extension)
                        if extension_source_code != driver.page_source:
                            driver.get(url_path)

                    except JavascriptException:
                        pass
                    except (WebDriverException, ProtocolError, MaxRetryError) as e:
                        with rlock:
                            error_logging(source, f"{order} {e.__class__.__name__}")
                            driver.quit()
                            driver = Chrome(service=Service(), options=option)
                            driver.get(url_of_injection_example)
                            example_source_code = (
                                driver.page_source
                            )  # set new example page source
                            example = (
                                driver.current_window_handle
                            )  # set new example handle
                            driver.switch_to.new_window("tab")  # switch to new tab
                            driver.get(url_path)  # browse to new extension popup
                            extension = (
                                driver.current_window_handle
                            )  # set new extension handle
                            extension_source_code = (
                                driver.page_source
                            )  # set new extension page source

                    except Exception as e:
                        error_logging(
                            source,
                            f"{e.__class__.__name__}[Thread {order} norm payload]: {e}",
                        )

            for payload_no, payload in enumerate(server_payloads[1]):
                progress_bar.update(1)
                payload = payload.replace(
                    "mhudogbhrqrjxjxelug",
                    f"http://127.0.0.1:8000/xss/{order}/{payload_no}",
                )

                try:
                    driver.switch_to.window(example)
                    driver.execute_script(
                        f"window.history.replaceState(null, null, `{website}?qureyParam={payload}`)"
                    )
                    # get time of injection
                    time_of_injection = time()

                    PageUrlElement = driver.find_element(By.ID, "pageUrl")

                    # usage of context menu
                    # # perform right click to open context menu
                    actions = ActionChains(driver)
                    actions.move_to_element(PageUrlElement)
                    actions.context_click().perform()

                    for _ in range(8):
                        with rlock:
                            subprocess.call(["xdotool", "key", "Down"])

                    # Simulate pressing the "Enter" key
                    with rlock:
                        subprocess.call(["xdotool", "key", "Return"])

                    driver.switch_to.window(extension)
                    driver.refresh()
                    driver.switch_to.window(example)

                    url = "http://127.0.0.1:8000/data/{}/{}".format(order, payload_no)
                    sleep(3)

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
                    # [1] check modifications for example.com
                    driver.switch_to.window(example)
                    if example_source_code != driver.page_source:
                        driver.get(website)

                    # [2] check modifications for extension
                    driver.switch_to.window(extension)
                    if extension_source_code != driver.page_source:
                        driver.get(url_path)

                except JavascriptException:
                    pass
                except (WebDriverException, ProtocolError, MaxRetryError) as e:
                    with rlock:
                        error_logging(source, f"{order} {e.__class__.__name__}")
                        driver.quit()
                        driver = Chrome(service=Service(), options=option)
                        driver.get(url_of_injection_example)
                        example_source_code = (
                            driver.page_source
                        )  # set new example page source
                        example = driver.current_window_handle  # set new example handle
                        driver.switch_to.new_window("tab")  # switch to new tab
                        driver.get(url_path)  # browse to new extension popup
                        extension = (
                            driver.current_window_handle
                        )  # set new extension handle
                        extension_source_code = (
                            driver.page_source
                        )  # set new extension page source
                except Exception as e:
                    error_logging(
                        source,
                        f"{e.__class__.__name__}[Thread {order} svr payload]: {e}",
                    )

        except Exception as e:
            error_logging(source, f"{e.__class__.__name__}[Thread {order} ended]: {e}")
        finally:
            driver.quit()

    source = result["taintsource"]
    match source:
        case "selectionText":
            return context_menu_selectionText_N(**args)
        case "linkUrl":
            return context_menu_link_url_N(**args)
        case "srcUrl":
            return context_menu_src_url_N(**args)
        case "frameUrl":
            return context_menu_frame_url_N(**args)
        case "pageUrl":
            return context_menu_pageUrl_N(**args)
        case _:
            progress_bar.update(payloads[0] + server_payloads[0])
            return


# combined chromeTabQuery
def chromeTabQuery(
    rlock,
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
):
    # save args
    args = locals()
    relative_path = "DYNAMIC_ANALYSIS/miscellaneous/example.html"
    url_of_injection_example = "file://" + os.path.abspath(relative_path)

    # new chromeTabsQuery.title (works)
    def chromeTabsQuery_title_N(
        rlock,
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
    ):
        source = "chromeTabsQuery.title"

        driver = Chrome(service=Service(), options=option)

        try:
            # get www.example.com
            driver.get(url_of_injection_example)

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
                try:
                    # change to example.com to change document.title property
                    driver.switch_to.window(example)
                    driver.refresh()
                    driver.execute_script(f"document.title = `{payload}`;")

                    # get time of injection
                    time_of_injection = time()

                    # observe behavior after payload injection
                    # 1) Check for alerts in example
                    driver.switch_to.window(example)
                    try:
                        # wait 2 seconds to see if alert is detected
                        WebDriverWait(driver, 2).until(EC.alert_is_present())
                        alert = driver.switch_to.alert
                        alert.accept()

                        time_of_success = time()
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

                            time_of_success = time()
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

                    # check modifications for example.com
                    driver.switch_to.window(example)
                    if example_source_code != driver.page_source:
                        driver.get("https://www.example.com")

                    # check modifications for extension
                    driver.switch_to.window(extension)
                    if extension_source_code != driver.page_source:
                        driver.get(url_path)

                except JavascriptException:
                    pass
                except (WebDriverException, ProtocolError, MaxRetryError) as e:
                    with rlock:
                        error_logging(source, f"{order} {e.__class__.__name__}")
                        driver.quit()
                        driver = Chrome(service=Service(), options=option)
                        driver.get(url_of_injection_example)
                        example_source_code = (
                            driver.page_source
                        )  # set new example page source
                        example = driver.current_window_handle  # set new example handle
                        driver.switch_to.new_window("tab")  # switch to new tab
                        driver.get(url_path)  # browse to new extension popup
                        extension = (
                            driver.current_window_handle
                        )  # set new extension handle
                        extension_source_code = (
                            driver.page_source
                        )  # set new extension page source

                except Exception as e:
                    error_logging(
                        source,
                        f"{e.__class__.__name__}[Thread {order} norm payload]: {e}",
                    )

            for payload_no, payload in enumerate(server_payloads[1]):
                progress_bar.update(1)
                payload = payload.replace(
                    "mhudogbhrqrjxjxelug",
                    f"http://127.0.0.1:8000/xss/{order}/{payload_no}",
                )

                try:
                    driver.switch_to.window(example)
                    driver.refresh()
                    driver.execute_script(f"document.title = `{payload}`;")
                    # get time of injection
                    time_of_injection = time()

                    driver.switch_to.window(extension)
                    driver.refresh()
                    driver.switch_to.window(example)

                    url = "http://127.0.0.1:8000/data/{}/{}".format(order, payload_no)
                    sleep(3)

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

                    # check modifications for example.com
                    driver.switch_to.window(example)
                    if example_source_code != driver.page_source:
                        driver.get("https://www.example.com")

                    # check modifications for extension
                    driver.switch_to.window(extension)
                    if extension_source_code != driver.page_source:
                        driver.get(url_path)

                except JavascriptException:
                    pass
                except (WebDriverException, ProtocolError, MaxRetryError) as e:
                    with rlock:
                        error_logging(source, f"{order} {e.__class__.__name__}")
                        driver.quit()
                        driver = Chrome(service=Service(), options=option)
                        driver.get(url_of_injection_example)
                        example_source_code = (
                            driver.page_source
                        )  # set new example page source
                        example = driver.current_window_handle  # set new example handle
                        driver.switch_to.new_window("tab")  # switch to new tab
                        driver.get(url_path)  # browse to new extension popup
                        extension = (
                            driver.current_window_handle
                        )  # set new extension handle
                        extension_source_code = (
                            driver.page_source
                        )  # set new extension page source
                except Exception as e:
                    error_logging(
                        source,
                        f"{e.__class__.__name__}[Thread {order} svr payload]: {e}",
                    )

        except Exception as e:
            error_logging(source, f"{e.__class__.__name__}[Thread {order} ended]: {e}")
        finally:
            driver.quit()

    # new chromeTabQuery.url (works)
    def chromeTabQuery_url_N(
        rlock,
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
    ):
        source = "chromeTabQuery.url"

        driver = Chrome(service=Service(), options=option)

        # Case Secnario for chromeTabQuery_url_new
        try:
            # Navigate to example.com
            driver.get(url_of_injection_example)
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

                try:
                    # change to example.com to change url property
                    driver.switch_to.window(example)
                    driver.execute_script(
                        f"location.href = `https://www.example.com/?p={payload}`"
                    )

                    # get time of injection
                    time_of_injection = time()

                    # observe behavior after payload injection
                    # 1) Check for alerts in example
                    try:
                        # wait 2 seconds to see if alert is detected
                        WebDriverWait(driver, 2).until(EC.alert_is_present())
                        alert = driver.switch_to.alert
                        alert.accept()

                        time_of_success = time()
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

                            time_of_success = time()
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

                    # check modifications for example.com
                    driver.switch_to.window(example)
                    if example_source_code != driver.page_source:
                        driver.get("https://www.example.com")

                    # check modifications for extension
                    driver.switch_to.window(extension)
                    if extension_source_code != driver.page_source:
                        driver.get(url_path)

                except JavascriptException:
                    pass
                except (WebDriverException, ProtocolError, MaxRetryError) as e:
                    with rlock:
                        error_logging(source, f"{order} {e.__class__.__name__}")
                        driver.quit()
                        driver = Chrome(service=Service(), options=option)
                        driver.get(url_of_injection_example)
                        example_source_code = (
                            driver.page_source
                        )  # set new example page source
                        example = driver.current_window_handle  # set new example handle
                        driver.switch_to.new_window("tab")  # switch to new tab
                        driver.get(url_path)  # browse to new extension popup
                        extension = (
                            driver.current_window_handle
                        )  # set new extension handle
                        extension_source_code = (
                            driver.page_source
                        )  # set new extension page source

                except Exception as e:
                    error_logging(
                        source,
                        f"{e.__class__.__name__}[Thread {order} norm payload]: {e}",
                    )

            for payload_no, payload in enumerate(server_payloads[1]):
                progress_bar.update(1)
                payload = payload.replace(
                    "mhudogbhrqrjxjxelug",
                    f"http://127.0.0.1:8000/xss/{order}/{payload_no}",
                )

                try:
                    driver.switch_to.window(example)
                    driver.refresh()
                    driver.execute_script(
                        f"location.href = `https://www.example.com/?p={payload}`"
                    )

                    # get time of injection
                    time_of_injection = time()

                    driver.switch_to.window(extension)
                    driver.refresh()
                    driver.switch_to.window(example)

                    url = "http://127.0.0.1:8000/data/{}/{}".format(order, payload_no)
                    sleep(3)

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

                    # check modifications for example.com
                    driver.switch_to.window(example)
                    if example_source_code != driver.page_source:
                        driver.get("https://www.example.com")

                    # check modifications for extension
                    driver.switch_to.window(extension)
                    if extension_source_code != driver.page_source:
                        driver.get(url_path)

                except JavascriptException:
                    pass
                except (WebDriverException, ProtocolError, MaxRetryError) as e:
                    with rlock:
                        error_logging(source, f"{order} {e.__class__.__name__}")
                        driver.quit()
                        driver = Chrome(service=Service(), options=option)
                        driver.get(url_of_injection_example)
                        example_source_code = (
                            driver.page_source
                        )  # set new example page source
                        example = driver.current_window_handle  # set new example handle
                        driver.switch_to.new_window("tab")  # switch to new tab
                        driver.get(url_path)  # browse to new extension popup
                        extension = (
                            driver.current_window_handle
                        )  # set new extension handle
                        extension_source_code = (
                            driver.page_source
                        )  # set new extension page source
                except Exception as e:
                    error_logging(
                        source,
                        f"{e.__class__.__name__}[Thread {order} svr payload]: {e}",
                    )

        except Exception as e:
            error_logging(source, f"{e.__class__.__name__}[Thread {order} ended]: {e}")
        finally:
            driver.quit()

    # new chromeTabQuery.favIconUrl (works)
    def chromeTabQuery_favIconUrl_N(
        rlock,
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
    ):
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

                try:
                    driver.switch_to.window(example)
                    # change filename to payloads
                    rename_file_with_payloads(payload)

                    payload = payload.strip()
                    # use filename as payload in ext
                    # remove current favIconUrl
                    driver.execute_script(
                        """
                    var linkElement = document.querySelector('link[rel="icon"]');
                    if (linkElement) {
                    linkElement.parentNode.removeChild(linkElement);
                    }
                    """
                    )

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

                    # get time of injection
                    time_of_injection = time()

                    driver.switch_to.window(example)
                    # observe behavior after payload injection
                    # 1) Check for alerts in example.com
                    try:
                        # wait 2 seconds to see if alert is detected
                        WebDriverWait(driver, 2).until(EC.alert_is_present())
                        alert = driver.switch_to.alert
                        alert.accept()

                        time_of_success = time()
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

                            time_of_success = time()
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

                    # check modifications for example
                    driver.switch_to.window(example)
                    if example_source_code != driver.page_source:
                        driver.get(website)

                    # check modifications for extension
                    driver.switch_to.window(extension)
                    if extension_source_code != driver.page_source:
                        driver.get(url_path)

                except JavascriptException:
                    pass
                except (WebDriverException, ProtocolError, MaxRetryError) as e:
                    with rlock:
                        error_logging(source, f"{order} {e.__class__.__name__}")
                        driver.quit()
                        driver = Chrome(service=Service(), options=option)
                        driver.get(url_of_injection_example)
                        example_source_code = (
                            driver.page_source
                        )  # set new example page source
                        example = driver.current_window_handle  # set new example handle
                        driver.switch_to.new_window("tab")  # switch to new tab
                        driver.get(url_path)  # browse to new extension popup
                        extension = (
                            driver.current_window_handle
                        )  # set new extension handle
                        extension_source_code = (
                            driver.page_source
                        )  # set new extension page source

                except Exception as e:
                    error_logging(
                        source,
                        f"{e.__class__.__name__}[Thread {order} norm payload]: {e}",
                    )

        except Exception as e:
            error_logging(source, f"{e.__class__.__name__}[Thread {order} ended]: {e}")
        finally:
            driver.quit()

    source = result["taintsource"]
    match source:
        case "title":
            return chromeTabsQuery_title_N(**args)
        case "faviconUrl":
            return chromeTabQuery_favIconUrl_N(**args)
        case "url":
            return chromeTabQuery_url_N(**args)
        case _:
            progress_bar.update(payloads[0] + server_payloads[0])
            return


# new location.search (works)
def location_search_N(
    rlock,
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
):
    source = "location.search"
    relative_path = "DYNAMIC_ANALYSIS/miscellaneous/example.html"
    url_of_injection_example = "file://" + os.path.abspath(relative_path)

    driver = Chrome(service=Service(), options=option)
    try:
        # navigate to example.com
        driver.get(url_of_injection_example)

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
            # with rlock:
            # update progress bar
            progress_bar.update(1)
            try:
                # navigate to example.com
                driver.switch_to.window(example)

                # get time of injection
                time_of_injection = time()

                # define a query parameter
                driver.execute_script(f"window.location.search=`?q={payload}`")
                try:
                    # wait 2 seconds to see if alert is detected
                    WebDriverWait(driver, 2).until(EC.alert_is_present())
                    alert = driver.switch_to.alert
                    alert.accept()

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
                        time(),
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
                        # 2) Check for alerts in example after refreshing extension
                        driver.switch_to.window(extension)
                        driver.refresh()
                        driver.switch_to.window(example)

                        # wait 2 seconds to see if alert is detected
                        WebDriverWait(driver, 2).until(EC.alert_is_present())
                        alert = driver.switch_to.alert
                        alert.accept()

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
                            time(),
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

                # check modifications for example
                driver.switch_to.window(example)
                if example_source_code != driver.page_source:
                    driver.get(url_of_injection_example)

                # check modifications for extension
                driver.switch_to.window(extension)
                if extension_source_code != driver.page_source:
                    driver.get(url_path)

            except JavascriptException:
                pass
            except (WebDriverException, ProtocolError, MaxRetryError) as e:
                with rlock:
                    error_logging(source, f"{order} {e.__class__.__name__}")
                    driver.quit()
                    driver = Chrome(service=Service(), options=option)
                    driver.get(url_of_injection_example)
                    example_source_code = (
                        driver.page_source
                    )  # set new example page source
                    example = driver.current_window_handle  # set new example handle
                    driver.switch_to.new_window("tab")  # switch to new tab
                    driver.get(url_path)  # browse to new extension popup
                    extension = driver.current_window_handle  # set new extension handle
                    extension_source_code = (
                        driver.page_source
                    )  # set new extension page source
            except Exception as e:
                error_logging(
                    source, f"{e.__class__.__name__}[Thread {order} norm payload]: {e}"
                )

        for payload_no, payload in enumerate(server_payloads[1]):
            # with rlock:
            # update progress bar
            progress_bar.update(1)
            payload = payload.replace(
                "mhudogbhrqrjxjxelug", f"http://127.0.0.1:8000/xss/{order}/{payload_no}"
            )

            # get time of injection
            time_of_injection = time()
            try:
                driver.switch_to.window(example)
                driver.refresh()
                driver.execute_script(f"window.location.search=`?q={payload}`")

                driver.switch_to.window(extension)
                driver.refresh()
                driver.switch_to.window(example)

                url = "http://127.0.0.1:8000/data/{}/{}".format(order, payload_no)
                sleep(3)

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

                # check modifications for example.com
                driver.switch_to.window(example)
                if example_source_code != driver.page_source:
                    driver.get("https://www.example.com")

                # check modifications for extension
                driver.switch_to.window(extension)
                if extension_source_code != driver.page_source:
                    driver.get(url_path)

            except JavascriptException:
                pass
            except (WebDriverException, ProtocolError, MaxRetryError) as e:
                with rlock:
                    error_logging(source, f"{order} {e.__class__.__name__}")
                    driver.quit()
                    driver = Chrome(service=Service(), options=option)
                    driver.get(url_of_injection_example)
                    example_source_code = (
                        driver.page_source
                    )  # set new example page source
                    example = driver.current_window_handle  # set new example handle
                    driver.switch_to.new_window("tab")  # switch to new tab
                    driver.get(url_path)  # browse to new extension popup
                    extension = driver.current_window_handle  # set new extension handle
                    extension_source_code = (
                        driver.page_source
                    )  # set new extension page source
            except Exception as e:
                error_logging(
                    source,
                    f"{e.__class__.__name__}[Thread {order} svr payload]: {e}",
                )

    except Exception as e:
        error_logging(source, f"{e.__class__.__name__}[Thread {order} ended]: {e}")
    finally:
        driver.quit()


# combined chromeDebugger
def chromeDebugger(
    rlock,
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
):
    # save args
    args = locals()
    relative_path = "DYNAMIC_ANALYSIS/miscellaneous/example.html"
    url_of_injection_example = "file://" + os.path.abspath(relative_path)

    # new chrome.Debugger.GetTargets (works)
    def chromeDebugger_title_N(
        rlock,
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
    ):
        source = "chromeDebugger.GetTargets.title"

        driver = Chrome(service=Service(), options=option)

        try:
            # navigate to example.com
            driver.get(url_of_injection_example)
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
                try:
                    # change to example.com to change document.title property
                    driver.switch_to.window(example)
                    driver.refresh()

                    driver.execute_script(f"document.title = `{payload}`;")

                    # get time of injection
                    time_of_injection = time()

                    with rlock:
                        # Press the F12 key to open the developer tools
                        subprocess.call(["xdotool", "keydown", "F12"])
                        subprocess.call(["xdotool", "keyup", "F12"])

                    # observe behavior after payload injection
                    # 1) Check for alerts in example.com
                    driver.switch_to.window(example)
                    try:
                        # wait 2 seconds to see if alert is detected
                        WebDriverWait(driver, 2).until(EC.alert_is_present())
                        alert = driver.switch_to.alert
                        alert.accept()

                        time_of_success = time()
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

                            time_of_success = time()
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

                    # [1] check modifications for example.com
                    driver.switch_to.window(example)
                    if example_source_code != driver.page_source:
                        driver.get(url_of_injection_example)

                    # [2] check modifications for extension
                    driver.switch_to.window(extension)
                    if extension_source_code != driver.page_source:
                        driver.get(url_path)

                except JavascriptException:
                    pass
                except (WebDriverException, ProtocolError, MaxRetryError) as e:
                    with rlock:
                        error_logging(source, f"{order} {e.__class__.__name__}")
                        driver.quit()
                        driver = Chrome(service=Service(), options=option)
                        driver.get(url_of_injection_example)
                        example_source_code = (
                            driver.page_source
                        )  # set new example page source
                        example = driver.current_window_handle  # set new example handle
                        driver.switch_to.new_window("tab")  # switch to new tab
                        driver.get(url_path)  # browse to new extension popup
                        extension = (
                            driver.current_window_handle
                        )  # set new extension handle
                        extension_source_code = (
                            driver.page_source
                        )  # set new extension page source

                except Exception as e:
                    error_logging(
                        source,
                        f"{e.__class__.__name__}[Thread {order} norm payload]: {e}",
                    )

            for payload_no, payload in enumerate(server_payloads[1]):
                progress_bar.update(1)

                payload = payload.replace(
                    "mhudogbhrqrjxjxelug",
                    f"http://127.0.0.1:8000/xss/{order}/{payload_no}",
                )

                try:
                    driver.switch_to.window(example)
                    driver.refresh()
                    driver.execute_script(f"document.title = `{payload}`;")

                    # get time of injection
                    time_of_injection = time()

                    with rlock:
                        # Press the F12 key to open the developer tools
                        subprocess.call(["xdotool", "keydown", "F12"])
                        subprocess.call(["xdotool", "keyup", "F12"])

                    driver.switch_to.window(extension)
                    driver.refresh()
                    driver.switch_to.window(example)

                    url = "http://127.0.0.1:8000/data/{}/{}".format(order, payload_no)
                    sleep(3)

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

                    # [1] check modifications for example.com
                    driver.switch_to.window(example)
                    if example_source_code != driver.page_source:
                        driver.get(url_of_injection_example)

                    # [2] check modifications for extension
                    driver.switch_to.window(extension)
                    if extension_source_code != driver.page_source:
                        driver.get(url_path)

                except JavascriptException:
                    pass
                except (WebDriverException, ProtocolError, MaxRetryError) as e:
                    with rlock:
                        error_logging(source, f"{order} {e.__class__.__name__}")
                        driver.quit()
                        driver = Chrome(service=Service(), options=option)
                        driver.get(url_of_injection_example)
                        example_source_code = (
                            driver.page_source
                        )  # set new example page source
                        example = driver.current_window_handle  # set new example handle
                        driver.switch_to.new_window("tab")  # switch to new tab
                        driver.get(url_path)  # browse to new extension popup
                        extension = (
                            driver.current_window_handle
                        )  # set new extension handle
                        extension_source_code = (
                            driver.page_source
                        )  # set new extension page source
                except Exception as e:
                    error_logging(
                        source,
                        f"{e.__class__.__name__}[Thread {order} svr payload]: {e}",
                    )

        except Exception as e:
            error_logging(source, f"{e.__class__.__name__}[Thread {order} ended]: {e}")
        finally:
            driver.quit()

    # new chrome.Debugger.GetTargets (works)
    def chromeDebugger_url_N(
        rlock,
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
    ):
        source = "chromeTabQuery.url"

        driver = Chrome(service=Service(), options=option)
        try:
            # Navigate to example.com
            driver.get(url_of_injection_example)
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
                try:
                    # change to example.com to change url property
                    driver.switch_to.window(example)
                    driver.refresh()

                    driver.execute_script(
                        f"location.href = `https://www.example.com/?p={payload}`"
                    )

                    # get time of injection
                    time_of_injection = time()

                    # Press the F12 key to open the developer tools
                    with rlock:
                        subprocess.call(["xdotool", "keydown", "F12"])
                        subprocess.call(["xdotool", "keyup", "F12"])

                    # observe behavior after payload injection
                    # 1) Check for alerts in example
                    try:
                        # wait 2 seconds to see if alert is detected
                        WebDriverWait(driver, 2).until(EC.alert_is_present())
                        alert = driver.switch_to.alert
                        alert.accept()

                        time_of_success = time()
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

                            time_of_success = time()
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

                    # check modifications for example.com
                    driver.switch_to.window(example)
                    if example_source_code != driver.page_source:
                        driver.get("https://www.example.com")

                    # check modifications for extension
                    driver.switch_to.window(extension)
                    if extension_source_code != driver.page_source:
                        driver.get(url_path)

                except JavascriptException:
                    pass
                except (WebDriverException, ProtocolError, MaxRetryError) as e:
                    with rlock:
                        error_logging(source, f"{order} {e.__class__.__name__}")
                        driver.quit()
                        driver = Chrome(service=Service(), options=option)
                        driver.get(url_of_injection_example)
                        example_source_code = (
                            driver.page_source
                        )  # set new example page source
                        example = driver.current_window_handle  # set new example handle
                        driver.switch_to.new_window("tab")  # switch to new tab
                        driver.get(url_path)  # browse to new extension popup
                        extension = (
                            driver.current_window_handle
                        )  # set new extension handle
                        extension_source_code = (
                            driver.page_source
                        )  # set new extension page source

                except Exception as e:
                    error_logging(
                        source,
                        f"{e.__class__.__name__}[Thread {order} norm payload]: {e}",
                    )

            for payload_no, payload in enumerate(server_payloads[1]):
                progress_bar.update(1)
                payload = payload.replace(
                    "mhudogbhrqrjxjxelug",
                    f"http://127.0.0.1:8000/xss/{order}/{payload_no}",
                )

                try:
                    driver.switch_to.window(example)
                    driver.refresh()
                    driver.execute_script(
                        f"location.href = `https://www.example.com/?p={payload}`"
                    )

                    # get time of injection
                    time_of_injection = time()

                    # Press the F12 key to open the developer tools
                    with rlock:
                        subprocess.call(["xdotool", "keydown", "F12"])
                        subprocess.call(["xdotool", "keyup", "F12"])

                    driver.switch_to.window(extension)
                    driver.refresh()
                    driver.switch_to.window(example)

                    url = "http://127.0.0.1:8000/data/{}/{}".format(order, payload_no)
                    sleep(3)

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

                    # check modifications for example.com
                    driver.switch_to.window(example)
                    if example_source_code != driver.page_source:
                        driver.get("https://www.example.com")

                    # check modifications for extension
                    driver.switch_to.window(extension)
                    if extension_source_code != driver.page_source:
                        driver.get(url_path)

                except JavascriptException:
                    pass
                except (WebDriverException, ProtocolError, MaxRetryError) as e:
                    with rlock:
                        error_logging(source, f"{order} {e.__class__.__name__}")
                        driver.quit()
                        driver = Chrome(service=Service(), options=option)
                        driver.get(url_of_injection_example)
                        example_source_code = (
                            driver.page_source
                        )  # set new example page source
                        example = driver.current_window_handle  # set new example handle
                        driver.switch_to.new_window("tab")  # switch to new tab
                        driver.get(url_path)  # browse to new extension popup
                        extension = (
                            driver.current_window_handle
                        )  # set new extension handle
                        extension_source_code = (
                            driver.page_source
                        )  # set new extension page source
                except Exception as e:
                    error_logging(
                        source,
                        f"{e.__class__.__name__}[Thread {order} svr payload]: {e}",
                    )

        except Exception as e:
            error_logging(source, f"{e.__class__.__name__}[Thread {order} ended]: {e}")
        finally:
            driver.quit()

    # new chromeDebugger_favIconUrl (works)
    def chromeDebugger_favIconUrl_N(
        rlock,
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
    ):
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

                try:
                    driver.switch_to.window(example)
                    # change filename to payloads
                    rename_file_with_payloads(payload)

                    payload = payload.strip()
                    # use filename as payload in ext
                    driver.execute_script(
                        """
                    var linkElement = document.querySelector('link[rel="icon"]');
                    if (linkElement) {
                    linkElement.parentNode.removeChild(linkElement);
                    }
                    """
                    )

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

                    # get time of injection
                    time_of_injection = time()

                    with rlock:
                        # Press the F12 key to open the developer tools
                        subprocess.call(["xdotool", "keydown", "F12"])
                        subprocess.call(["xdotool", "keyup", "F12"])

                    # observe behavior after payload injection
                    # 1) Check for alerts in example.com
                    driver.switch_to.window(example)
                    try:
                        # wait 2 seconds to see if alert is detected
                        WebDriverWait(driver, 2).until(EC.alert_is_present())
                        alert = driver.switch_to.alert
                        alert.accept()

                        time_of_success = time()
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

                            time_of_success = time()
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

                    # check modifications for example.com
                    driver.switch_to.window(example)
                    if example_source_code != driver.page_source:
                        driver.get(website)

                    # check modifications for extension
                    driver.switch_to.window(extension)
                    if extension_source_code != driver.page_source:
                        driver.get(url_path)

                except JavascriptException:
                    pass
                except (WebDriverException, ProtocolError, MaxRetryError) as e:
                    with rlock:
                        error_logging(source, f"{order} {e.__class__.__name__}")
                        driver.quit()
                        driver = Chrome(service=Service(), options=option)
                        driver.get(url_of_injection_example)
                        example_source_code = (
                            driver.page_source
                        )  # set new example page source
                        example = driver.current_window_handle  # set new example handle
                        driver.switch_to.new_window("tab")  # switch to new tab
                        driver.get(url_path)  # browse to new extension popup
                        extension = (
                            driver.current_window_handle
                        )  # set new extension handle
                        extension_source_code = (
                            driver.page_source
                        )  # set new extension page source

                except Exception as e:
                    error_logging(
                        source,
                        f"{e.__class__.__name__}[Thread {order} norm payload]: {e}",
                    )

        except Exception as e:
            error_logging(source, f"{e.__class__.__name__}[Thread {order} ended]: {e}")
        finally:
            driver.quit()

    source = result["taintsource"]
    match source:
        case "title":
            return chromeDebugger_title_N(**args)
        case "favIconUrl":
            return chromeDebugger_favIconUrl_N(**args)
        case "url":
            return chromeDebugger_url_N(**args)
        case _:
            progress_bar.update(payloads[0] + server_payloads[0])
            return


# new window.addEventListernerMessage (shd work (old ver))
def windowAddEventListenerMessage(
    rlock,
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
):
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

            payload = payload.strip()
            taintsink = result["sink"]
            script = nomagic(taintsink, payload, {})
            cases = (
                f"window.postMessage({script},'*')",
                f"window.postMessage(`{payload}`,'*')",
            )

            for i in cases:
                try:
                    driver.switch_to.window(example)
                    driver.refresh()
                    driver.execute_script(i)
                    # get time of injection
                    time_of_injection = time()

                    # observe behavior after payload injection
                    # check for alerts in example
                    try:
                        # wait 2 seconds to see if alert is detected
                        WebDriverWait(driver, 2).until(EC.alert_is_present())
                        alert = driver.switch_to.alert
                        alert.accept()
                        # print('[example] + Alert Detected +')

                        # get time of success [1) example]
                        time_of_success = time()
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
                            time_of_success = time()
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

                    # check modifications for example.com
                    driver.switch_to.window(example)
                    if example_source_code != driver.page_source:
                        driver.get(website)

                    # check modifications for extension
                    driver.switch_to.window(extension)
                    if extension_source_code != driver.page_source:
                        driver.get(url_path)
                except JavascriptException:
                    pass
                except (WebDriverException, ProtocolError, MaxRetryError) as e:
                    with rlock:
                        error_logging(source, f"{order} {e.__class__.__name__}")
                        driver.quit()
                        driver = Chrome(service=Service(), options=option)
                        driver.get(url_of_injection_example)
                        example_source_code = (
                            driver.page_source
                        )  # set new example page source
                        example = driver.current_window_handle  # set new example handle
                        driver.switch_to.new_window("tab")  # switch to new tab
                        driver.get(url_path)  # browse to new extension popup
                        extension = (
                            driver.current_window_handle
                        )  # set new extension handle
                        extension_source_code = (
                            driver.page_source
                        )  # set new extension page source

                except Exception as e:
                    error_logging(
                        source,
                        f"{e.__class__.__name__}[Thread {order} norm payload]: {e}",
                    )

        for payload_no, payload in enumerate(server_payloads[1]):
            progress_bar.update(1)
            payload = payload.replace(
                "mhudogbhrqrjxjxelug", f"http://127.0.0.1:8000/xss/{order}/{payload_no}"
            )

            taintsink = result["sink"]
            script = nomagic(taintsink, payload, {})
            cases = (
                f"window.postMessage({script},'*')",
                f"window.postMessage(`{payload}`,'*')",
            )

            for i in cases:
                try:
                    driver.switch_to.window(example)
                    driver.refresh()
                    driver.execute_script(i)
                    # get time of injection
                    time_of_injection = time()

                    driver.switch_to.window(extension)
                    driver.refresh()
                    driver.switch_to.window(example)

                    url = "http://127.0.0.1:8000/data/{}/{}".format(order, payload_no)
                    sleep(3)

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

                    # check modifications for example.com
                    driver.switch_to.window(example)
                    if example_source_code != driver.page_source:
                        driver.get(website)

                    # check modifications for extension
                    driver.switch_to.window(extension)
                    if extension_source_code != driver.page_source:
                        driver.get(url_path)

                except JavascriptException:
                    pass
                except (WebDriverException, ProtocolError, MaxRetryError) as e:
                    with rlock:
                        error_logging(source, f"{order} {e.__class__.__name__}")
                        driver.quit()
                        driver = Chrome(service=Service(), options=option)
                        driver.get(url_of_injection_example)
                        example_source_code = (
                            driver.page_source
                        )  # set new example page source
                        example = driver.current_window_handle  # set new example handle
                        driver.switch_to.new_window("tab")  # switch to new tab
                        driver.get(url_path)  # browse to new extension popup
                        extension = (
                            driver.current_window_handle
                        )  # set new extension handle
                        extension_source_code = (
                            driver.page_source
                        )  # set new extension page source
                except Exception as e:
                    error_logging(source, f"{e.__class__.__name__}: {e}")

    except Exception as e:
        error_logging(source, f"{e.__class__.__name__}[Thread {order} ended]: {e}")
    finally:
        driver.quit()


def form(
    rlock,
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
):
    source = "form"

    # obtain path to ext (where form is present)
    path = result["path"][23 + len(ext_name) :]
    url_path = f"chrome-extension://{ext_id}{path}"

    # automatically populate server_progressbar
    progress_bar.update(server_payloads[0])

    url_of_injection_example = "DYNAMIC_ANALYSIS/miscellaneous/example.html"
    website = "file://" + os.path.abspath(url_of_injection_example)
    driver = Chrome(service=Service(), options=option)

    try:
        # get www.example.com
        driver.get(website)

        # set handler for example.com
        example = driver.current_window_handle

        # get page source code of example.com
        example_source_code = driver.page_source

        # get extension popup.html (! OR INTERPRETE THE VULNRABILITY LOCATION)
        driver.switch_to.new_window("tab")
        extension = driver.current_window_handle
        driver.get(url_path)

        # get page source code of extension
        extension_source_code = driver.page_source

        driver.switch_to.window(extension)

        test = []
        # Find all <input> elements
        test.extend(driver.find_elements(By.TAG_NAME, "input"))
        # Find all <textarea> elements
        test.extend(driver.find_elements(By.TAG_NAME, "textarea"))
        # Find all <select> elements
        test.extend(driver.find_elements(By.TAG_NAME, "select"))
        # Find all <form> elements
        test.extend(driver.find_elements(By.TAG_NAME, "form"))

        if test:
            for payload in payloads[1]:
                progress_bar.update(1)

                try:
                    driver.switch_to.window(extension)

                    # get time of injection
                    time_of_injection = time()

                    form_elements = []
                    form_elements.extend(driver.find_elements(By.TAG_NAME, "form"))

                    elements = []
                    # Find all <input> elements
                    elements.extend(driver.find_elements(By.TAG_NAME, "input"))
                    # Find all <textarea> elements
                    elements.extend(driver.find_elements(By.TAG_NAME, "textarea"))
                    # Find all <select> elements
                    elements.extend(driver.find_elements(By.TAG_NAME, "select"))

                    for form in form_elements:
                        for element in elements:
                            match element.get_attribute("type"):
                                case "text" | "textarea" | "password" | "search":
                                    element.send_keys(payload)
                                case "checkbox":
                                    if not element.is_selected():
                                        element.click()
                                case "radio":
                                    if not element.is_selected():
                                        element.click()
                                case "date":
                                    # some random date
                                    element.send_keys("2023-08-16")
                                case "time":
                                    # some random time
                                    element.send_keys("15:30")
                                case "number":
                                    # some random number
                                    element.send_keys("69")
                                case "email":
                                    # some random email
                                    element.send_keys("scanext@gmail.com")
                                case "url":
                                    # some random url
                                    element.send_keys("https://scanext.com")
                                case "tel":
                                    # some random tel
                                    element.send_keys("999")
                                case "month":
                                    # some random month
                                    element.send_keys("2023-08")
                                case "week":
                                    # some random week
                                    element.send_keys("2023-W33")
                                case "datetime-local":
                                    # some random month
                                    element.send_keys("2023-08-16T15:30")
                                case "select-one":
                                    Select(element).select_by_index(0)
                                case _:
                                    pass

                        # submit form
                        form.submit()

                    try:
                        # wait 2 seconds to see if alert is detected
                        WebDriverWait(driver, 2).until(EC.alert_is_present())
                        alert = driver.switch_to.alert
                        alert.accept()
                        payload_logging(
                            "SUCCESS",
                            source,
                            ext_id,
                            ext_name,
                            url_of_injection_example,
                            "normal",
                            payload,
                            "[Automated Pentesting Input Fields with Selenium]",
                            time_of_injection,
                            time(),
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
                            "[Automated Pentesting Input Fields with Selenium]",
                            time_of_injection,
                            "nil",
                            payload_file,
                            "nil",
                        )

                        try:
                            # 2) Check for alerts in example after refreshing extension
                            driver.switch_to.window(extension)
                            driver.refresh()
                            driver.switch_to.window(example)

                            # wait 2 seconds to see if alert is detected
                            WebDriverWait(driver, 2).until(EC.alert_is_present())
                            alert = driver.switch_to.alert
                            alert.accept()

                            payload_logging(
                                "SUCCESS",
                                source,
                                ext_id,
                                ext_name,
                                url_of_injection_example,
                                "normal",
                                payload,
                                "[Automated Pentesting Input Fields with Selenium]",
                                time_of_injection,
                                time(),
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
                                "[Automated Pentesting Input Fields with Selenium]",
                                time_of_injection,
                                "nil",
                                payload_file,
                                "nil",
                            )

                    # check modifications for example
                    driver.switch_to.window(example)
                    if example_source_code != driver.page_source:
                        driver.get(website)

                    # check modifications for extension
                    driver.switch_to.window(extension)
                    if extension_source_code != driver.page_source:
                        driver.get(url_path)

                except (JavascriptException, InvalidArgumentException):
                    pass
                except (WebDriverException, ProtocolError, MaxRetryError) as e:
                    with rlock:
                        error_logging(source, f"{order} {e.__class__.__name__}")
                        driver.quit()
                        driver = Chrome(service=Service(), options=option)
                        driver.get(website)
                        example_source_code = (
                            driver.page_source
                        )  # set new example page source
                        example = driver.current_window_handle  # set new example handle
                        driver.switch_to.new_window("tab")  # switch to new tab
                        driver.get(url_path)  # browse to new extension popup
                        extension = (
                            driver.current_window_handle
                        )  # set new extension handle
                        extension_source_code = (
                            driver.page_source
                        )  # set new extension page source
                except Exception as e:
                    error_logging(
                        source,
                        f"{e.__class__.__name__}[Thread {order} norm payload]: {e}",
                    )
        else:
            error_logging(
                source, f"[Thread {order}]: No inputs or textareas or selects found"
            )
            progress_bar.update(payloads[0])

    except Exception as e:
        error_logging(source, f"{e.__class__.__name__}[Thread {order} ended]: {e}")
    finally:
        driver.quit()


# store functions in dict
sourcelist = {
    "chrome_contextMenu_create": context_menu,
    "chrome_contextMenu_onClicked_addListener": context_menu,
    "chrome_contextMenu_update": context_menu,
    "chrome_cookies_get": cookie_get,
    "chrome_cookies_getAll": cookie_get,
    "chrome_debugger_getTargets": chromeDebugger,
    "chrome_runtime_onConnect": runtime_onC,
    "chrome_runtime_onConnectExternal": runtime_onCE,
    "chrome_runtime_onMessage": runtime_onM,
    "chrome_runtime_onMessageExternal": runtime_onME,
    "chrome_tabs_get": chromeTabQuery,
    "chrome_tabs_getCurrent": chromeTabQuery,
    "chrome_tabs_query": chromeTabQuery,
    "location_hash": location_hash,
    "location_href": location_href_N,
    "location_search": location_search_N,
    "window_addEventListener_message": windowAddEventListenerMessage,
    "window_name": window_name_N,
    "form": form,
}
