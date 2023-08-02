import json
import shutil
from datetime import datetime as dt
from email.utils import format_datetime as fdt
from os import cpu_count
from pathlib import Path
from zipfile import ZipFile

import jsbeautifier
from bs4 import BeautifulSoup
from pytz import timezone as tz
from pyvirtualdisplay.display import Display
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service

from report_gen import static_results_report, dynamic_results_report
from banners import get_banner
from constants import *
from dynamic import main as dynamic
from static import main as static


# return CROSS or TICK icon
def icon(boolean: bool):
    if boolean:
        return TICK
    return CROSS


# extract extensions and format the extracted files
def extraction():
    extension_dir = Path("SHARED/EXTENSIONS")
    extraction_dir = Path("SHARED/EXTRACTED")

    types = ("*.zip", "*.crx")
    extensions: list[Path] = []
    for t in types:
        extensions.extend(extension_dir.glob(t))

    opts = jsbeautifier.default_options()
    opts.end_with_newline = True
    opts.wrap_line_length = 80
    opts.space_after_anon_function = True

    status = extraction_dir.exists()
    print(f"Checking existence of {extraction_dir} ... {icon(status)}")
    if status:
        print(f"Removing existing {extraction_dir} ... ", end="")
        shutil.rmtree(extraction_dir)
        print(TICK)
    print(f"Making {extraction_dir} ... ", end="")
    extraction_dir.mkdir()
    print(TICK)

    for extension in extensions:
        indi_dir = Path(extraction_dir, extension.stem)
        print(f"Making {indi_dir} ... ", end="")
        indi_dir.mkdir()
        print(TICK)

        with ZipFile(extension, "r") as zip:
            print(f"Extracting {extension.name} ... ", end="")
            zip.extractall(indi_dir)
        manifest_exists = Path(indi_dir, "manifest.json").exists()
        print(icon(manifest_exists))
        if not manifest_exists:
            print(f"{CROSS} manifest.json not found in root")
            shutil.rmtree(indi_dir)
        for file in indi_dir.glob("**/*.js"):
            pretty = jsbeautifier.beautify_file(file, opts)
            local_options = jsbeautifier.BeautifierOptions()
            local_options.keep_quiet = True
            jsbeautifier.write_beautified_output(pretty, local_options, str(file))
    return Path(extraction_dir).glob("*")


# conduct static analysis using Semgrep
def static_analysis(extension: Path, soup: BeautifulSoup, config, report_path):
    output_file = static(extension)

    # read the static results
    with open(output_file, "r") as static_result_file:
        results: list[dict] = json.load(static_result_file)["results"]
        sorted_results = sorted(results, key=lambda e: e["path"])
        sorted_results = sorted(sorted_results, key=lambda e: e["check_id"])

    static_results_report(
        sorted_results, extension, soup, config, report_path
    )

    return sorted_results


# conduct dynamic analysis using Selenium
def dynamic_analysis(
    results, extension: Path, soup: BeautifulSoup, config, report_path
):
    print()
    print("Conducting dynamic analysis ...")

    # call selenium main.py
    dynamic(config, extension, results)

    print()
    print("Dynamic analysis complete.")

    # Retrieve information from log file
    logs_obj = []

    with open(DYNAMIC_LOGFILE, "r") as f:
        for line in f:
            logs_obj.append(json.loads(line))
    

    # Filter by ext name
    filtered_logs = filter(lambda ext: ext["extensionName"] == extension.name, logs_obj)

    # Sort by source (window.name, etc.)
    source_sorted_logs = sorted(filtered_logs, key=lambda x: x["source"])

    dynamic_results_report(
        source_sorted_logs, soup, report_path
    )


# load configurations set by user
def load_config():
    # Load config
    with open("SHARED/config.json") as f:
        config: dict = json.load(f)

    # Check thread count requested
    def isThreadValid(key):
        number_of_instances = config[key]
        thread_count = cpu_count()
        if thread_count is None:
            print("Error: Unable to determine the number of threads the CPU has.")
            print("Exiting ... ")
            exit()
        if number_of_instances == "auto":
            config[key] = thread_count // 4
            return True
        isValidInt(key=key, min=1)
        if number_of_instances > round(0.5 * thread_count):
            print(
                f"Error: {number_of_instances} instances requested is > than 50% of your CPU's thread count."
            )
            print("Exiting ... ")
            exit()
        thread_count //= 4
        if number_of_instances > thread_count:
            print(
                f"Warning: {number_of_instances} instances requested is > than the {thread_count} recommended for your CPU."
            )
            print("Recommendation = CPU's thread count // 4")
            print("Unexpected errors may occur.")
            print("Continuing ...")
        return True

    # Check validity of config [int]
    def isValidInt(key, min, max=None):
        user_value = config[key]

        # check if int
        if not isinstance(user_value, int):
            print(f"Error: {key} ({user_value}) is not an integer.")
            print("Exiting program...")
            exit()

        # if int, check if within range of min and max

        # check if max is set
        if max:
            if user_value < min or user_value > max:
                print(
                    f"Error: {key} ({user_value}) must be an integer between {min} and {max}."
                )
                print("Exiting program...")
                exit()
        # max not set
        else:
            if user_value < min:
                print(
                    f"Error: {key} ({user_value}) must be an integer more than {min}."
                )
                print("Exiting program...")
                exit()

        return True

    # Check validity of config [payload file]
    def isValidFile(key):
        user_file = config[key]

        # Check if set to default "nil"
        if user_file != "auto":
            # Check if file exists inside SHARED
            file_path = Path(f"SHARED/{user_file}")
            if not file_path.exists():
                print(f"Error: {key} ({file_path}) does not exist.")
                print("Exiting program...")
                exit()

            # Check if file ends with .txt
            if file_path.suffix != ".txt":
                print(f"Error: {key} ({file_path}) does not end with .txt")
                print("Exiting program...")
                exit()

            # Check if file is at least 1 payload long
            if file_path.stat().st_size == 0:
                print(f"Error: {key} ({file_path}) is empty.")
                print("Exiting program...")
                exit()

        return True

    # Check validity of config [datetime]
    def isValidTimezone(key):
        user_timezone = config[key]

        try:
            fdt(dt.now(tz(user_timezone)))
        except:
            print(f"Error: {key} ({user_timezone}) is not a valid timezone.")
            print("Exiting program...")
            exit()

        return True

    tests = (
        isValidInt(key="report_display_adjacent_lines", min=0),
        isValidInt(key="percentage_of_payloads", min=1, max=100),
        isValidFile(key="payload_file_path"),
        isValidTimezone(key="timezone"),
        isThreadValid(key="number_of_instances"),
    )
    if all(tests):
        return config


# Test selenium / cache driver
def test_selenium():
    print("Testing Selenium ... ", end="")
    with Display():
        try:
            options = ChromeOptions()
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--no-sandbox")
            with Chrome(service=Service(), options=options) as driver:
                webpage_url = "file://" + str(Path("DYNAMIC_ANALYSIS/miscellaneous/xss_website.html").absolute())
                driver.get(webpage_url)
                if driver.title != "Xss Website":
                    print(CROSS)
                    print("Error: Selenium test failed!")
                    print("Exiting ...")
                    exit()
        except Exception as e:
            print(CROSS)
            print(f"Error: Selenium test error: {e}")
            print("Exiting ...")
            exit()
    print(TICK)
    return True


# main program
def main():
    print(get_banner())
    config = load_config()
    test_selenium()
    dynamic_logfile = Path(DYNAMIC_LOGFILE)
    error_logfile = Path(ERROR_LOGFILE)


    # clear log file before logging
    if dynamic_logfile.exists():
        with dynamic_logfile.open("w") as f:
            f.truncate(0)
    if error_logfile.exists():
        with error_logfile.open("w") as f:
            f.truncate(0)
    
    timezone = config["timezone"]
    whole_scan_start = fdt(dt.now(tz(timezone)))

    for extension in extraction():
        print()

        # Parse report template HTML content
        with open("report_template.html", "r") as f:
            soup = BeautifulSoup(f, "html.parser")

        # Get scan date
        scan_start = fdt(dt.now(tz(timezone)))

        # Update scan date in report
        soup.find(id="scan-date").string = scan_start

        # Initialise report path
        report_path = Path(
            f"SHARED/REPORTS/{extension.name} ({scan_start.replace(':','-')}).html"
        )

        # Start static analysis
        results = static_analysis(extension, soup, config, report_path)

        # If static analysis found vulns, start dynamic analysis
        if results:
            dynamic_analysis(results, extension, soup, config, report_path)

    # Copy log files to SHARED

    # Initialise user dynamic logfile path
    shared_log_file = Path(f"SHARED/LOGS/{whole_scan_start.replace(':','-')}.log")

    shared_log_dir = Path("SHARED/LOGS")
    if not shared_log_dir.exists():
        shared_log_dir.mkdir()
    shutil.copyfile(dynamic_logfile, shared_log_file)
    print()
    print(f"Logs from this scan are available in `{shared_log_file}`")


if __name__ == "__main__":
    main()
