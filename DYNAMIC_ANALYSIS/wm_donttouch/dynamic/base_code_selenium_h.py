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

        # driver.execute_script(f'document.getElementById("h1_element").innerHTML = `{payload}`')

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


        driver.switch_to.window(extension)
        driver.save_screenshot('ss.png')
        time.sleep(2)



        driver.switch_to.window(example)
        driver.save_screenshot('ss.png')
        time.sleep(2)
        


    time.sleep(1)


