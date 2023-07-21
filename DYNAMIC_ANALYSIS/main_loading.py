
from selenium.webdriver import ActionChains, Chrome, ChromeOptions, Keys
from os import path
import hashlib
from selenium import webdriver
from pyvirtualdisplay.display import Display
from concurrent.futures import ThreadPoolExecutor


from case_scenario_functions import *
from preconfigure import *


from os import cpu_count

from itertools import cycle

from tqdm import tqdm

# def test_window_name(args_tuple):
#     order, option, payloads, url_path, ext_id = args_tuple

#     global progress_bars


#     driver = Chrome(service=Service(), options=option)
#     source = 'window.name'
#     url_of_injection_example = 'https://www.example.com'
#     payload_file = 'small_payload.txt'

#     try:
#         # Navigate to example.com
#         driver.get('https://www.example.com')
#         example = driver.current_window_handle

#         # Wait up to 5 seconds for the title to become "Example Domain"
#         title_condition = EC.title_is('Example Domain')
#         WebDriverWait(driver, 5).until(title_condition)

#         # get page source code of example.com
#         example_source_code = driver.page_source

#         # get extension popup.html
#         driver.switch_to.new_window('tab')
#         driver.get(url_path)
#         extension = driver.current_window_handle

#         # get page source code of extension
#         extension_source_code = driver.page_source

#         for payload in payloads:
#             print(payload)
#             # since window.name is obtained from the website url, we will inject javascript to change the window.name
#             driver.switch_to.window(example)

#             try:
#                 driver.execute_script(f'window.name = `{payload}`;')

#                 # get time of injection
#                 time_of_injection = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")
#                 progress_bars[order].update(1)
#             except Exception as e:
#                 print(' !!!! PAYLOAD FAILLED !!!!')
#                 print('Error: ', str(e))
#                 progress_bars[order].update(1)
#                 continue

#             # observe behavior after payload injection
#             # check for alerts in example
#             try:
#                 # wait 2 seconds to see if alert is detected
#                 WebDriverWait(driver, 2).until(EC.alert_is_present())
#                 alert = driver.switch_to.alert
#                 alert.accept()
#                 print('[example] + Alert Detected +')

#                 # get time of success [1) example]
#                 time_of_success = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")
#                 payload_logging("SUCCESS", source, ext_id, 'h1-replacer(v3)', url_of_injection_example, 'normal', payload, time_of_injection, time_of_success, payload_file, 'nil')
            
#             except TimeoutException:
#                 print('[example] = No alerts detected =')
#                 payload_logging("FAILURE", source, ext_id, 'h1-replacer(v3)', url_of_injection_example, 'normal', payload, time_of_injection, 'nil', payload_file, 'nil')


#             # 2) Check for alerts in example after refreshing extension
#             driver.switch_to.window(extension)
#             driver.refresh()
#             driver.switch_to.window(example)

#             try:
#                 # wait 2 seconds to see if alert is detected
#                 WebDriverWait(driver, 2).until(EC.alert_is_present())
#                 alert = driver.switch_to.alert
#                 alert.accept()
#                 print('[example] + Alert Detected +')

#                 # get time of success [3) example]
#                 time_of_success = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")
#                 payload_logging("SUCCESS", source, ext_id, 'h1-replacer(v3)', url_of_injection_example, 'normal', payload, time_of_injection, time_of_success, payload_file, 'nil')
#             except TimeoutException:
#                 print('[example] = No alerts detected =')
#                 payload_logging("FAILURE", source, ext_id, 'h1-replacer(v3)', url_of_injection_example, 'normal', payload, time_of_injection, 'nil', payload_file, 'nil')

#             try: 
#                 # check modifications for example.com
#                 driver.switch_to.window(example)
#                 if example_source_code != driver.page_source:
#                     driver.get("https://www.example.com")
#                     print("Navigated back to 'https://www.example.com' due to page source changes")
#             except:
#                 print('error')

#             try: 
#                 # check modifications for extension
#                 driver.switch_to.window(extension)
#                 if extension_source_code != driver.page_source:
#                     driver.get(url_path)
#                     print(f"Navigated back to '{url_path}' due to extension page source changes")
#             except:
#                 print('error')

#     except TimeoutException:
#         # Handle TimeoutException when title condition is not met
#         print("Timeout: Title was not resolved to 'Example Domain'")

#     except Exception as e:
#         # Handle any other exceptions that occur
#         print("An error occurred:", str(e))


def main(path_to_extension, semgrep_results, n: int = 4):

    url_path, abs_path, ext_id = get_ext_id(path_to_extension)

    
    options = webdriver.ChromeOptions()
    # options.add_experimental_option("detach", True)
    load_ext_arg = "load-extension=" + abs_path
    options.add_argument(load_ext_arg)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--enable-logging")

    thread_count = cpu_count()
    if thread_count is None:
        print("Unable to determind the number of threads the CPU has.")
        print("Exiting ... ")
        exit()
    
    thread_count //= 3
    if n > thread_count:
        print(f"Warning, {n} instances requested is > than the {thread_count} recommended for your CPU.")
        print("Recommendation = CPU's thread count // 3.")
        print("Continuing ... ")

    def payloads_cycle(n: int, file_path: str):
        c = cycle(range(n))
        payloads = [[] for _ in range(n)]
        with open(file_path, "r") as file:
            for line in file:
                if line != "\n":
                    payloads[c.__next__()].append(line.rstrip())
        return [len(p) for p in payloads], tuple(tuple(s) for s in payloads)

    totals, payloads = payloads_cycle(n, 'DYNAMIC_ANALYSIS/payloads/normal_payload.txt')


    global progress_bars
    progress_bars = [
        tqdm(
            colour="#00ff00",
            total=totals[order],
            desc=f"Instance {order}",
            bar_format="{desc}: {bar} {percentage:3.0f}%|{n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]",
        )
        for order in range(n)
    ]

    args = [(progress_bars[order], order, options, payloads[order], url_path, ext_id) for order in range(n)]
    with ThreadPoolExecutor(n) as executor:
        for logs in executor.map(test_window_name, args):
            for level, log in logs:
                getattr(logging, level, log)








with open("DYNAMIC_ANALYSIS/window_name_w.json", "r") as file:
    semgrep_results = json.load(file)["results"]


if __name__ == '__main__':
    semgrep_results = ['123']

    path_to_extension = 'EXTENSIONS/h1-replacer(v3)_window.name'

    with Display() as disp:
        main(path_to_extension, semgrep_results)