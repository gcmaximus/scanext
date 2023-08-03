import logging
import shutil
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Process

import requests
from pyvirtualdisplay.display import Display
from selenium.webdriver import ChromeOptions
from tqdm import tqdm

from constants import *
from DYNAMIC_ANALYSIS.case_scenario_functions import *
from DYNAMIC_ANALYSIS.preconfigure import *
from server import main as server


def setup_logger(logger_name, log_file, timezone):
    match logger_name:
        case "dynamic":
            # define log level
            log_level = logging.CRITICAL

            # Create a formatter
            formatter = logging.Formatter('%(message)s')
            
        case "error":
            # define log level
            log_level = logging.ERROR

            # Create a formatter
            formatter = logging.Formatter('%(asctime)s - [%(name)s] - %(message)s')

        case _:
            raise Exception(f"{logger_name} must be 'dynamic' or 'error'")

    # Create a logger with a specific name
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)

    # Clear any existing handlers 
    if (logger.hasHandlers()):
        logger.handlers.clear()

    # Set a file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    setattr(logger, "timezone", timezone)


def main(config, path_to_extension, semgrep_results):
    # load configs
    percentage_of_payloads = config["percentage_of_payloads"]
    number_of_instances = config["number_of_instances"]
    custom_payload_file = config["payload_file_path"]
    timezone = config["timezone"]

    # set payload file
    if custom_payload_file == "auto":
        # default file
        alert_payload_file = ALERT_PAYLOAD_FILE
    else:
        # user file
        alert_payload_file = f"SHARED/{custom_payload_file}"

    server_payloads_file = SERVER_PAYLAOD_FILE
    print(f"Using payload file (check for alerts): {alert_payload_file}")
    print(f"Using payload file (check for HTTP requests): {server_payloads_file}")


    setup_logger("dynamic", DYNAMIC_LOGFILE, timezone)
    setup_logger('error', ERROR_LOGFILE, timezone)


    # preconfiguration (set active to false)
    path_to_extension = preconfigure(path_to_extension)


    # obtain relevant extension information
    url_path, abs_path, ext_id, ext_name = get_ext_id(path_to_extension)

    
    # Split payloads into groups for each thread
    meta_payloads = payloads_cycle(number_of_instances, percentage_of_payloads, alert_payload_file)
    server_payloads = payloads_cycle(number_of_instances, percentage_of_payloads, server_payloads_file)

    # interprete semgrep scan results
    interpreted_results = separator(interpreter(semgrep_results))

    # solo var list
    sololist = [
        "chrome_cookies_get",
        "chrome_cookies_getAll",
        "location_hash",
        "location_href",
        "location_search",
        "window_name",
        "chrome_contextMenu_create",
        "chrome_contextMenu_onClicked_addListener",
        "chrome_contextMenu_update",
        "chrome_debugger_getTargets",
        "chrome_tabs_get",
        "chrome_tabs_getCurrent",
        "chrome_tabs_query",
        "window_addEventListener_message"
    ]
    results = []
    for result, occurences in interpreted_results.items():
        if result in sololist:
            results.append(occurences[0])
        else:
            for occurence in occurences:
                results.append(occurence)

    sourcelist = {
        "chrome_contextMenu_create":context_menu,
        "chrome_contextMenu_onClicked_addListener":context_menu,
        "chrome_contextMenu_update":context_menu,
        "chrome_cookies_get":cookie_get,
        "chrome_cookies_getAll":cookie_get,
        "chrome_debugger_getTargets":chromeDebugger,
        "chrome_runtime_onConnect":runtime_onC,
        "chrome_runtime_onConnectExternal":runtime_onCE,
        "chrome_runtime_onMessage":runtime_onM,
        "chrome_runtime_onMessageExternal":runtime_onME,
        "chrome_tabs_get":chromeTabQuery,
        "chrome_tabs_getCurrent":chromeTabQuery,
        "chrome_tabs_query":chromeTabQuery,
        "location_hash":location_hash,
        "location_href":location_href_N,
        "location_search":location_search_N,
        "window_addEventListener_message":windowAddEventListenerMessage,
        "window_name":window_name_N,
    }
    
    local_server = Process(target=server)
    local_server.start()

    for result in results:
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
                # options.add_argument("--disable-gpu")

                source = result["source"]
                print()
                print('SOURCE: ', source)
                
                progress_bars = [
                    tqdm(
                        colour="#00ff00",
                        total=meta_payloads[order][0]+server_payloads[order][0],
                        desc=f"Instance {order}",
                        bar_format="{desc}: {bar} {percentage:3.0f}%|{n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]",
                    )
                    for order in range(number_of_instances)
                ]

                # 10 args
                args = [(progress_bars[order], order, options, meta_payloads[order], url_path, ext_id, ext_name, alert_payload_file, result, server_payloads[order]) for order in range(number_of_instances)]

                
                with ThreadPoolExecutor(number_of_instances) as executor:
                    for _ in executor.map(sourcelist[source], args):
                        pass

                for bar in progress_bars:
                    bar.close()
                
                # Clear local server's data
                requests.delete("http://127.0.0.1:8000/data")

        except Exception as e:
            print("Error while initializing headless chrome driver ")
            print(str(e))
    
    local_server.terminate()

    # remove all miscellaneous files (directories only)
    shutil.rmtree("tmp")
    for f in Path("DYNAMIC_ANALYSIS/miscellaneous").glob("*"):
        if f.is_dir():
            shutil.rmtree(f)

    
        

if __name__ == '__main__':
    print("testing")
