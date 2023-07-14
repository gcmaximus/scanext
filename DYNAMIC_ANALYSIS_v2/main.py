
from selenium.webdriver import ActionChains, Chrome, ChromeOptions, Keys
from os import path
import hashlib
from pyvirtualdisplay.display import Display
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
import logging

from selenium.webdriver.support import expected_conditions as EC
import json





import logging

from case_secnario_functions import *







def main(path_to_extension):

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
    
    url_path, abs_path, ext_id = get_ext_id(path_to_extension)
    payload = payloads('DYNAMIC_ANALYSIS/dynamic/payloads/small_payload.txt')

    result = []

    with Display() as disp:
        options = ChromeOptions()
        options.add_experimental_option('detach', True)
        load_ext_arg = "load-extension=" + abs_path
        options.add_argument(load_ext_arg)
        options.add_argument("--enable-logging")
        options.add_argument("--disable-dev-shm-usage")
        driver = Chrome(service=Service(), options=options)


        x = location_href_new(driver, ext_id, url_path, payload, result)



main("DYNAMIC_ANALYSIS/wm_donttouch/Extensions/h1-replacer/h1-replacer(v3)_window.name")