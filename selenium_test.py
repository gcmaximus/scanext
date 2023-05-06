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
driver.get("https://is.gd/WVZvnI")
try:
    ele = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (
                By.CLASS_NAME,
                "y\x74p-\x6car\x67e-play-\x62u\x74\x74on",
            )
        )
    )
except:
    print("not found")
    ActionChains(driver).send_keys("k").perform()
else:
    print("found")
    ele.click()
# driver.find_element(By.NAME, "\x50\x6c\x61\x79").click()
# print(driver.find_elements(By.CLASS_NAME,"ytp-large-play-button"))
# driver.execute_script('document.getElementsByTagName("video")[0].play()')
