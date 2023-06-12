from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from pyvirtualdisplay import Display

display = Display(backend="xvfb")
print(display.is_alive())

display.start()
print(display.is_alive())

chrome_options = Options()

# chrome_options.add_extension("extension_2_0_13_0.crx")

driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', chrome_options=chrome_options)
time.sleep(3)
driver.get("https://ipinfo.io/json")
print(driver.page_source)
driver.close()

display.stop()