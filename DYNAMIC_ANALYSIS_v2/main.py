
from selenium.webdriver import ActionChains, Chrome, ChromeOptions, Keys
from os import path
import hashlib
from pyvirtualdisplay.display import Display
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service


from case_secnario_functions import *
from preconfigure import *



def main(path_to_extension, semgrep_results):
    # obtain relevant extension information
    url_path, abs_path, ext_id = get_ext_id(path_to_extension)

    # obtain payloads
    payload = payloads('DYNAMIC_ANALYSIS/wm_donttouch/payloads/extra_small_payload.txt')

    # preconfiguration (set active to false)
    preconfigure(path_to_extension)

    # interprete semgrep scan results
    interpreted_results = interpreter(semgrep_results)

    # define source list (map source to case_secnario function)
    sourcelist = {
        "chrome_contextMenu_create":".",
        "chrome_contextMenu_onClicked_addListener":".",
        "chrome_contextMenu_update":".",
        "chrome_cookies_get":cookie_get,
        "chrome_cookies_getAll":cookie_get,
        "chrome_debugger_getTargets":".",
        "chrome_runtime_onConnect":runtime_onC,
        "chrome_runtime_onConnectExternal":runtime_onCE,
        "chrome_runtime_onMessage":runtime_onM,
        "chrome_runtime_onMessageExternal":runtime_onME,
        "chrome_tabs_get":".",
        "chrome_tabs_getCurrent":".",
        "chrome_tabs_query":".",
        "location_hash":location_hash,
        "location_href":location_href_new,
        "location_search":locationSearch,
        "window_addEventListener_message":windowAddEventListenerMessage,
        "window_name":location_href_new,
    }


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
                driver = Chrome(service=Service(), options=options)


                source = result["message"].split(";")[0][7:]
                print('SOURCE: ', source)
                sourcelist[source](driver,ext_id,url_path,payload,result)



        except Exception as e:
            print("Error while initializing haedless chrome driver ")
            print(str(e))
    


with open("DYNAMIC_ANALYSIS_v2/window_name_w.json", "r") as file:
    semgrep_results = json.load(file)["results"]



main("DYNAMIC_ANALYSIS/wm_donttouch/Extensions/h1-replacer/h1-replacer(v3)_window.name", semgrep_results)