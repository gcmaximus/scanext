from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoAlertPresentException

from os import path
import hashlib

from pathlib import Path
import time

def initialize(path_to_extension):
    # obtain relevant extension information'
    def get_ext_id(path_to_extension):
        abs_path = path.abspath(path_to_extension)
        m = hashlib.sha256()
        m.update(abs_path.encode("utf-8"))
        ext_id = "".join([chr(int(i, base=16) + 97) for i in m.hexdigest()][:32])
        url_path = f"chrome-extension://{ext_id}/popup.html"
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

    url_path, abs_path = get_ext_id(path_to_extension)
    payloads = payloads('payloads/small_payload.txt')

    # initialize selenium and load extension
    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', True)
    load_ext_arg = "load-extension=" + abs_path
    options.add_argument(load_ext_arg)
    options.add_argument("--enable-logging")
    driver = webdriver.Chrome('./chromedriver', options=options)




    # case 1:
    # window_name(driver, abs_path, url_path, payloads)

    # case 2:
    location_href(driver, abs_path, url_path, payloads)







################
# Case Scenario#
################

# 1) Window_name Entry Point
def window_name(driver, abs_path, url_path, payloads):

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
def location_href(driver, abs_path, url_path, payloads):
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




initialize('Extensions/h1-replacer/h1-replacer(v3)_location.href')