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
ele = WebDriverWait(driver, 30).until(
    EC.presence_of_all_elements_located((By.TAG_NAME, "video"))
)
ActionChains(driver).send_keys(Keys.SPACE).perform()
# driver.execute_script('document.getElementsByTagName("video")[0].play()')
