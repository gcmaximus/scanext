# test codes for selenium

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)
# options.add_extension('C:/Users/pearl/Desktop/DISM/.DISM Y3/S1/extension_0_0_9_7.crx')
options.add_argument('load-extension=C:/Users/pearl/AppData/Local/Google/Chrome/User Data/Default/Extensions/gighmmpiobklfepjocnamgkkbiglidom/5.4.1_0')

driver = webdriver.Chrome('./chromedriver', options=options)

# driver.implicitly_wait(1000)
driver.get("chrome://extensions")



elem = driver.find_element(By.CLASS_NAME, 'chrome-extension-input')
# elem.send_keys()
# elem.submit()

# element = WebDriverWait(driver,3600000).until(
#     EC.presence_of_element_located((By.CLASS_NAME, 'manifest-dashboard'))
# )


# print (driver.title)

