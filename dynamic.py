import logging
import shutil
from multiprocessing import Process
from multiprocessing.pool import ThreadPool
from threading import RLock

import requests
from pyvirtualdisplay.display import Display
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from tqdm import tqdm

from constants import *
from DYNAMIC_ANALYSIS.case_scenario_functions import sourcelist
from DYNAMIC_ANALYSIS.preconfigure import *
from server import server


def setup_logger(logger_name, log_file):
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


def main(config, path_to_extension, semgrep_results):
    # load configs
    percentage_of_payloads = config["percentage_of_payloads"]
    number_of_instances = config["number_of_instances"]
    custom_payload_file = config["payload_file_path"]

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


    setup_logger("dynamic", DYNAMIC_LOGFILE)
    setup_logger('error', ERROR_LOGFILE)


    # Preconfiguration (set active to false)
    path_to_ext = preconfigure(path_to_extension)

    # manifest rewriting in tmp
    manifest_rewrite(path_to_ext)
    # Obtain relevant extension information
    url_path, abs_path, ext_id, ext_name = get_ext_id(path_to_ext)

    # Test loading of extension into Chrome
    print()
    print("Test loading of extension ... ", end="", flush=True)
    load_ext_arg = "--load-extension=" + abs_path
    with Display():
        try:
            options = ChromeOptions()
            options.add_argument(load_ext_arg)
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-infobars")
            with Chrome(service=Service(), options=options) as driver:
                driver.get(url_path)
        except Exception as e:
            print(CROSS)
            print()
            print(f"Error: Unable to load extension into Chrome: {e}")
            print("Extension probably contains some errors.")
            print("Exiting ...")
            exit()
    print(TICK)

    # Split payloads into groups for each thread
    meta_payloads = payloads_cycle(number_of_instances, percentage_of_payloads, alert_payload_file)
    server_payloads = payloads_cycle(number_of_instances, percentage_of_payloads, server_payloads_file)

    # Interprete semgrep scan results
    interpreted_results = separator(interpreter(semgrep_results))

    # Solo var list
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

    # Start local API server
    local_server = Process(target=server)
    local_server.start()

    # Start of attack 
    for result in results:
        try:
            with Display():
                options = ChromeOptions()
                load_ext_arg = "--load-extension=" + abs_path
                options.add_argument(load_ext_arg)
                options.add_argument("--enable-logging")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-gpu")
                options.add_argument("--disable-infobars")
                
                source = result["source"]
                print()
                print('SOURCE: ', source)
                
                # Start progress bars
                progress_bars = [
                    tqdm(
                        colour="#00ff00",
                        total=meta_payloads[order][0]+server_payloads[order][0],
                        desc=f"Instance {order}",
                        bar_format="{desc}: {bar} {percentage:3.0f}%|{n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]",
                        # leave=False,
                        # position=order
                    )
                    for order in range(number_of_instances)
                ]

                # Agrs for each thread
                rlock = RLock()
                args = ([rlock, progress_bars[order], order, options, meta_payloads[order], url_path, ext_id, ext_name, alert_payload_file, result, server_payloads[order]] for order in range(number_of_instances))
                
                # Thread worker function
                func = sourcelist[source]
                
                with ThreadPool(number_of_instances, initargs=(rlock,), initializer=tqdm.set_lock) as pool:
                    for _ in pool.starmap(func, args, 1):
                        pass

                # Close progress bars
                for bar in progress_bars:
                    bar.close()
                
                # Clear local server's data
                requests.delete("http://127.0.0.1:8000/data")

        except Exception as e:
            print("Error during dynamic phase")
            print(f"{e.__class__.__name__}: {e}")
    
    # Kill local API server
    local_server.kill()

    # remove all miscellaneous files (directories only)
    shutil.rmtree("tmp")
    for f in Path("DYNAMIC_ANALYSIS/miscellaneous").glob("*"):
        if f.is_dir() and f.name != "init_test_ext":
            shutil.rmtree(f)


if __name__ == '__main__':
    # set_start_method("spawn")
    with open("STATIC_ANALYSIS/semgrep_results.json", "r") as f:
        results: list[dict] = json.load(f)["results"]
        sorted_results = sorted(results, key=lambda e: e["path"])
        sorted_results = sorted(sorted_results, key=lambda e: e["check_id"])
    with open("DYNAMIC_ANALYSIS/Logs/dynamic_logs.log", "w") as dlogs:
        dlogs.truncate(0)
    from time import perf_counter
    s0 = perf_counter()
    main(
        {
            "report_display_adjacent_lines": 3,
            "number_of_instances": 8,
            "payload_file_path": "auto",
            "percentage_of_payloads": 100,
            "timezone": "Asia/Singapore"
        },
        "SHARED/EXTRACTED/2-vulns",
        sorted_results
    )
    s1 = perf_counter()
    print(f"{s0=} - {s1=} | dif: {s1-s0}")
