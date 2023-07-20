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
import shutil

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



def main(config, path_to_extension, semgrep_results):

    # load configs
    percentage_of_payloads = config["percentage_of_payloads"]
    number_of_instances = config["number_of_instances"]

    # logs
    logger = setup_logger('DYNAMIC_ANALYSIS_v2/Logs/dynamic_logsV2.txt')


    # obtain relevant extension information
    url_path, abs_path, ext_id = get_ext_id(path_to_extension)

    
    # new payloads
    # meta_payloads = payloads_cycle(number_of_instances, percentage_of_payloads, 'DYNAMIC_ANALYSIS_v2/payloads/payload.txt')
    # meta_payloads = payloads_cycle(number_of_instances, percentage_of_payloads, 'DYNAMIC_ANALYSIS_v2/payloads/test.txt')
    meta_payloads = payloads_cycle(number_of_instances, percentage_of_payloads, 'DYNAMIC_ANALYSIS_v2/payloads/big_payload.txt')


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
                # options.add_experimental_option('detach', True)
                load_ext_arg = "load-extension=" + abs_path
                options.add_argument(load_ext_arg)
                options.add_argument("--enable-logging")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--no-sandbox")

                # source = result["message"].split(";")[0][7:]
                # print('SOURCE: ', source)
                # sourcelist[source](driver,ext_id,url_path,payload,result)

                thread_count = cpu_count()
                if thread_count is None:
                    print("Unable to determind the number of threads the CPU has.")
                    print("Exiting ... ")
                    exit()

                thread_count //= 3
                if number_of_instances > thread_count:
                    print(f"Warning, {number_of_instances} instances requested is > than the {thread_count} recommended for your CPU.")
                    print("Recommendation = CPU's thread count // 3.")
                    print("Continuing ... ")


                progress_bars = [
                    tqdm(
                        colour="#00ff00",
                        total=meta_payloads[order][0],
                        desc=f"Instance {order}",
                        bar_format="{desc}: {bar} {percentage:3.0f}%|{n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]",
                    )
                    for order in range(number_of_instances)
                ]

                args = [(progress_bars[order], order, options, meta_payloads[order][1], url_path, ext_id, result) for order in range(number_of_instances)]
                
                with ThreadPoolExecutor(number_of_instances) as executor:
                    for logs in executor.map(chromeDebugger_favIconUrl_N, args):
                        for log in logs:
                            logger.critical(log)    

        except Exception as e:
            print("Error while initializing headless chrome driver ")
            print(str(e))
    shutil.rmtree("tmp")
    for f in Path("DYNAMIC_ANALYSIS_v2/miscellaneous").glob("*"):
        if f.is_dir():
            shutil.rmtree(f)
        

with open("DYNAMIC_ANALYSIS_v2/window_name_w.json", "r") as file:
    semgrep_results = json.load(file)["results"]


if __name__ == '__main__':
    semgrep_results = ['123']


    window_name_path = 'EXTENSIONS/h1-replacer(v3)_window.name'
    location_herf_path = 'DYNAMIC_ANALYSIS/wm_donttouch/Extensions/h1-replacer/h1-replacer(v3)_location.href'
    context_menu_path = 'DYNAMIC_ANALYSIS/wm_donttouch/Extensions/h1-replacer/h1-replacer(v3)_context_menu' 
    context_menu_path_test_path = 'DYNAMIC_ANALYSIS/wm_donttouch/Extensions/h1-replacer/test'
    chromeTabQuery_path = 'DYNAMIC_ANALYSIS/wm_donttouch/Extensions/h1-replacer/h1-replacer(v3)_chrome_tab_query'
    location_search_path = 'DYNAMIC_ANALYSIS/wm_donttouch/Extensions/h1-replacer/h1-replacer(v3)_location_search'
    chromeDebugGetTarget_path = 'DYNAMIC_ANALYSIS/wm_donttouch/Extensions/h1-replacer/h1-replacer(v3)_chromeDebuggerGetTarget'


    path_to_extension = chromeDebugGetTarget_path

    config = {
        "percentage_of_payloads" : 100,
        "number_of_instances": 1
    }



    main(config, path_to_extension, semgrep_results)
