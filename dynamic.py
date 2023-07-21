import logging
import shutil
from concurrent.futures import ThreadPoolExecutor
from email.utils import format_datetime as fdt
from os import cpu_count

from pytz import timezone as tz
from pyvirtualdisplay.display import Display
from selenium.webdriver import ChromeOptions
from tqdm import tqdm

from DYNAMIC_ANALYSIS.case_scenario_functions import *
from DYNAMIC_ANALYSIS.preconfigure import *


def setup_loggerV2(log_file):
    # Create a logger with a specific name (using an empty string for the root logger)
    logger = logging.getLogger('dynamic')
    logger.setLevel(logging.ERROR)

    # Create a file handler and set the log level
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.CRITICAL)

    # Create a formatter and add it to the handler
    log_format = '%(message)s'
    formatter = logging.Formatter(log_format)
    file_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(file_handler)

    return logger



def main(config, path_to_extension, semgrep_results):

    # load configs
    percentage_of_payloads = config["percentage_of_payloads"]
    number_of_instances = config["number_of_instances"]
    custom_payload_file = config["custom_payload_file"]
    timezone = config["timezone"]

    # set payload file
    if custom_payload_file == "nil":
        # default file
        payload_file = "DYNAMIC_ANALYSIS/payloads/big_payload.txt"
    else:
        # user file
        payload_file = f"SHARED/{custom_payload_file}"

    print(f"Using payload file: {payload_file}")

    dynamic_logger = setup_loggerV2('DYNAMIC_ANALYSIS/Logs/dynamic_logsV2.txt')


    # preconfiguration (set active to false)
    path_to_extension = preconfigure(path_to_extension)


    # obtain relevant extension information
    url_path, abs_path, ext_id = get_ext_id(path_to_extension)

    
    # new payloads
    # meta_payloads = payloads_cycle(number_of_instances, percentage_of_payloads, 'DYNAMIC_ANALYSIS/payloads/payload.txt')
    # meta_payloads = payloads_cycle(number_of_instances, percentage_of_payloads, 'DYNAMIC_ANALYSIS/payloads/test.txt')
    meta_payloads = payloads_cycle(number_of_instances, percentage_of_payloads, payload_file)


    # interprete semgrep scan results
    interpreted_results = separater(interpreter(semgrep_results))

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
        "chrome_tabs_query"
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
        "chrome_debugger_getTargets":".",
        "chrome_runtime_onConnect":runtime_onC,
        "chrome_runtime_onConnectExternal":runtime_onCE,
        "chrome_runtime_onMessage":runtime_onM,
        "chrome_runtime_onMessageExternal":runtime_onME,
        "chrome_tabs_get":chromeTabQuery,
        "chrome_tabs_getCurrent":chromeTabQuery,
        "chrome_tabs_query":chromeTabQuery,
        "location_hash":location_hash,
        "location_href":location_href_N,
        "location_search":locationSearch_N,
        "window_addEventListener_message":windowAddEventListenerMessage,
        "window_name":window_name_N,
    }
    
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

                source = result["source"]
                print('SOURCE: ', source)

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
                    for logs in executor.map(sourcelist[source], args):
                        for log in logs:
                            a, b = log["timeOfInjection"], log["timeOfAlert"]
                            if a != "nil":
                                a = fdt(a.astimezone(tz(timezone)))
                            if b != "nil":
                                b = fdt(b.astimezone(tz(timezone)))
                            dynamic_logger.critical(json.dumps(log))

        except Exception as e:
            print("Error while initializing headless chrome driver ")
            print(str(e))

    # remove all miscellaneous files (directories only)
    shutil.rmtree("tmp")
    for f in Path("DYNAMIC_ANALYSIS/miscellaneous").glob("*"):
        if f.is_dir():
            shutil.rmtree(f)
        

if __name__ == '__main__':
    
    # testing
    with open(" semgrep_results.json", "r") as file:
        semgrep_results = json.load(file)["results"]

    window_name_path = 'EXTENSIONS/h1-replacer(v3)_window.name'
    location_href_path = 'DYNAMIC_ANALYSIS/wm_donttouch/Extensions/h1-replacer/h1-replacer(v3)_location.href'
    context_menu_path = 'DYNAMIC_ANALYSIS/wm_donttouch/Extensions/h1-replacer/h1-replacer(v3)_context_menu' 
    context_menu_path_test_path = 'DYNAMIC_ANALYSIS/wm_donttouch/Extensions/h1-replacer/test'
    chromeTabQuery_path = 'DYNAMIC_ANALYSIS/wm_donttouch/Extensions/h1-replacer/h1-replacer(v3)_chrome_tab_query'
    location_search_path = 'DYNAMIC_ANALYSIS/wm_donttouch/Extensions/h1-replacer/h1-replacer(v3)_location_search'
    chromeDebugGetTarget_path = 'DYNAMIC_ANALYSIS/wm_donttouch/Extensions/h1-replacer/h1-replacer(v3)_chromeDebuggerGetTarget'
    windowAddEventListenerMessage_path = 'DYNAMIC_ANALYSIS/wm_donttouch/Extensions/h1-replacer/h1-replacer(v3)_window.addEventListernerMessage'


    path_to_extension = chromeTabQuery_path

    config = {
        "percentage_of_payloads" : 0.5,
        "number_of_instances": 1,
        "custom_payload_file": 'nil',
        'timezone': 'nil'
    }

    main(config, path_to_extension, semgrep_results)
