from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from os import path
import hashlib
from selenium.common.exceptions import NoAlertPresentException
from multiprocessing import Pool
from functools import partial


def get_ext_id(path_to_extension):
    abs_path = path.abspath(path_to_extension)
    m = hashlib.sha256()
    m.update(abs_path.encode("utf-8"))
    ext_id = "".join([chr(int(i, base=16) + 97) for i in m.hexdigest()][:32])
    url_path = f"chrome-extension://{ext_id}/popup.html"
    return url_path, abs_path



def process_payload(payloads, url_path, abs_path):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', True)
    load_ext_arg = "load-extension=" + abs_path
    options.add_argument(load_ext_arg)
    options.add_argument("--enable-logging")
    driver = webdriver.Chrome('./chromedriver', options=options)
    
    # get www.example.com
    driver.get('https://www.example.com')
    example = driver.current_window_handle

    # get extension popup.html
    driver.switch_to.new_window('tab')
    extension = driver.current_window_handle
    driver.get(url_path)


    for payload in payloads:
        driver.switch_to.window(extension)
        driver.refresh()
        driver.switch_to.window(example)

        
        driver.execute_script(f"window.name = '{payload}';")

        try:
            # wait 2 seconds to see if alert is detected
            WebDriverWait(driver, 2).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert.accept()
            print('+ Alert Detected +')
        except TimeoutException:
            print('= No alerts detected =')


def gui_window(extension_path):
    # get extension id and paths
    url_path, abs_path = get_ext_id(extension_path)

    def subset_payloads(file_path):
        payloads1 = []
        payloads2 = []
        payloads3 = []

        with open(file_path, 'r') as file:
            for line in file:
                payload = line.strip()  # Remove leading/trailing whitespace
                # Assign the payload to one of the subsets
                if len(payloads1) < len(payloads2) and len(payloads1) < len(payloads3):
                    payloads1.append(payload)
                elif len(payloads2) < len(payloads3):
                    payloads2.append(payload)
                else:
                    payloads3.append(payload)

        return payloads1, payloads2, payloads3

    payloads1, payloads2, payloads3 = subset_payloads('payloads/small_payload.txt')

    num_processes = 3  # Define the number of concurrent processes
    with Pool(num_processes) as pool:
        partial_process_payload = partial(process_payload, url_path=url_path, abs_path=abs_path)
        pool.map(partial_process_payload, [payloads1, payloads2, payloads3])



gui_window('Extensions/h1-replacer/h1-replacer(v3) window.name')









