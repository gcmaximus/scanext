
from selenium.webdriver import ActionChains, Chrome, ChromeOptions, Keys
from os import path
import hashlib
from pyvirtualdisplay.display import Display
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service

from case_scenario_functions import *
from preconfigure import *


from os import cpu_count
import tqdm
from itertools import cycle



def main(path_to_extension, semgrep_results, n: int = 4):
    
    url_path, abs_path, ext_id = get_ext_id(path_to_extension)

    with Display() as disp:
        options = ChromeOptions()
        options.add_experimental_option('detach', True)
        load_ext_arg = "load-extension=" + abs_path
        options.add_argument(load_ext_arg)
        options.add_argument("--enable-logging")
        options.add_argument("--disable-dev-shm-usage")

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

        totals, payloads = payloads_cycle(n, 'DYNAMIC_ANALYSIS_v2/payloads/normal_payload.txt')


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

        args = [(order, options, payloads[order], url_path) for order in range(n)]


        window_name_new(args, ext_id, url_path, payloads, result)












with open("DYNAMIC_ANALYSIS_v2/window_name_w.json", "r") as file:
    semgrep_results = json.load(file)["results"]


if __name__ == '__main__':
    semgrep_results = ['123']

    path_to_extension = 'EXTENSIONS/h1-replacer(v3)_window.name'

    main(path_to_extension, semgrep_results)