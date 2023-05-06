from selenium.webdriver import ActionChains, Chrome, ChromeOptions, Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

options = ChromeOptions()
options.add_experimental_option("detach", True)

chrome_service = Service(executable_path=ChromeDriverManager().install())
driver = Chrome(service=chrome_service, options=options)
driver.get("\x68\x74\x74\x70\x73\x3a\x2f\x2f\x69\x73\x2e\x67\x64\x2f\x57\x56\x5a\x76\x6e\x49")
ele = WebDriverWait(driver, 30).until(
    EC.presence_of_all_elements_located((By.TAG_NAME, "\x76\x69\x64\x65\x6f"))
)
ActionChains(driver).send_keys(Keys.SPACE).perform()
# driver.execute_script('document.getElementsByTagName("video")[0].play()')
