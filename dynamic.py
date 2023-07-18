from selenium.webdriver import ActionChains, Chrome, ChromeOptions, Keys
from os import path
import hashlib
from pyvirtualdisplay.display import Display
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service


from DYNAMIC_ANALYSIS_v2.case_scenario_functions import *
from DYNAMIC_ANALYSIS_v2.preconfigure import *

import logging
from os import cpu_count
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

def setup_logger(log_file):
    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(logging.ERROR)

    # Create a file handler and set the log level
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.CRITICAL)

    # Create a formatter and add it to the handlers
    log_format = '%(message)s'
    formatter = logging.Formatter(log_format)
    file_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)

    return logger



def main(config, path_to_extension, semgrep_results, n: int = 4):
    # logs
    logger = setup_logger('DYNAMIC_ANALYSIS_v2/Logs/dynamic_logsV2.txt')


    # obtain relevant extension information
    url_path, abs_path, ext_id = get_ext_id(path_to_extension)

    # obtain payloads
    # payload = payloads('DYNAMIC_ANALYSIS/wm_donttouch/payloads/extra_small_payload.txt')
    
    # new payloads
    totals, payloads = payloads_cycle(n, config["percentage_of_payloads"], 'DYNAMIC_ANALYSIS_v2/payloads/payload.txt')

    # preconfiguration (set active to false)
    preconfigure(path_to_extension)

    # interprete semgrep scan results
    # interpreted_results = interpreter(semgrep_results)

    interpreted_results = [123]

    # define source list (map source to case_scenario function)
    # sourcelist = {
    #     "chrome_contextMenu_create":".",
    #     "chrome_contextMenu_onClicked_addListener":".",
    #     "chrome_contextMenu_update":".",
    #     "chrome_cookies_get":cookie_get,
    #     "chrome_cookies_getAll":cookie_get,
    #     "chrome_debugger_getTargets":".",
    #     "chrome_runtime_onConnect":runtime_onC,
    #     "chrome_runtime_onConnectExternal":runtime_onCE,
    #     "chrome_runtime_onMessage":runtime_onM,
    #     "chrome_runtime_onMessageExternal":runtime_onME,
    #     "chrome_tabs_get":".",
    #     "chrome_tabs_getCurrent":".",
    #     "chrome_tabs_query":".",
    #     "location_hash":location_hash,
    #     "location_href":location_href,
    #     "location_search":locationSearch,
    #     "window_addEventListener_message":windowAddEventListenerMessage,
    #     "window_name":window_name_new,
    # }


    for result in interpreted_results:
        # initialize chrome driver
        try:
            with Display() as disp:
                options = ChromeOptions()
                options.add_experimental_option('detach', True)
                load_ext_arg = "load-extension=" + abs_path
                options.add_argument(load_ext_arg)
                options.add_argument("--enable-logging")
                options.add_argument("--disable-dev-shm-usage")


                # source = result["message"].split(";")[0][7:]
                # print('SOURCE: ', source)
                # sourcelist[source](driver,ext_id,url_path,payload,result)

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
                    for logs in executor.map(location_href_N, args):
                        for log in logs:
                            logger.critical(log)    

        except Exception as e:
            print("Error while initializing headless chrome driver ")
            print(str(e))
    
        

with open("DYNAMIC_ANALYSIS_v2/window_name_w.json", "r") as file:
    semgrep_results = json.load(file)["results"]


if __name__ == '__main__':
    semgrep_results = ['123']


    window_name_path = 'EXTENSIONS/h1-replacer(v3)_window.name'
    location_herf_path = 'DYNAMIC_ANALYSIS/wm_donttouch/Extensions/h1-replacer/h1-replacer(v3)_location.href'
    context_menu_path = '' 

    path_to_extension = location_herf_path

    config = {
        "percentage_of_payloads" : 10
    }



    main(config, path_to_extension, semgrep_results, 3)
