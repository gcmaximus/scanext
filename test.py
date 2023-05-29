# test codes for selenium

import time

from selenium import webdriver
from selenium.webdriver import ActionChains, Chrome, ChromeOptions, Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager
from pyvirtualdisplay import Display

with Display(backend="xvfb") as display:
    print(display.is_alive())
print(display.is_alive())

options = webdriver.ChromeOptions()
# options.add_experimental_option('detach', True)
options.add_extension('./extension_2_0_13_0.crx')
# options.add_argument('load-extension=../test/gtranslateext')

chrome_service = Service(executable_path=ChromeDriverManager().install())
driver = Chrome(service=chrome_service, options=options)

# driver = webdriver.Chrome('./chromedriver', options=options)

# extensions = driver.execute_script("return chrome.runtime.getManifest();")

# print(extensions)
time.sleep(2)
# id = driver.execute_script("return chrome.runtime.id;")
# print(id)

# driver.get("chrome://system")


# trust
driver.get("chrome-extension://aapbdbdomjkkjkaonfhkkikfgjllcleb/popup.html")

# driver.get("https://www.411-spyware.com/de/es-ist-die-ungesetzliche-tatigkeit-enthullt-bundespolizei-virus-entfernen")

input_field = driver.find_element(By.ID, 'text-input')

time.sleep(5)

input_field.send_keys('酒')

time.sleep(5)
# Find the button by its ID and click on it
button = driver.find_element(By.CLASS_NAME, 'goog-inline-block')
button.click()

print(driver.page_source)
# fun = driver.find_element(By.ID, 'funstuff')
display.stop()