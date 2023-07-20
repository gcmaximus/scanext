import json
import shutil
from email.utils import formatdate
from pathlib import Path
from zipfile import ZipFile

import jsbeautifier
from bs4 import BeautifulSoup

# from headless_cases import main as dynamic
from dynamic import main as dynamic
from static import main as static
from banners import get_banner
import report_gen
from constants import *





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
            print(f"{CROSS} manifest.json not found in root", end="")
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

    report_gen.static_results_report(sorted_results, extension, soup, config, report_path)

    return sorted_results

# conduct dynamic analysis using Selenium 
def dynamic_analysis(results, extension: Path, soup: BeautifulSoup, config, report_path):

    print()
    print('Conducting dynamic analysis ...')

    # call selenium main.py
    dynamic(config, extension, results)

    print()
    print('Dynamic analysis complete.')
    
    # Retrieve information from log file
    logs_obj = []

    # dynamic_logfile = 'dynamic_logs.txt'
    dynamic_logfile = 'DYNAMIC_ANALYSIS_v2/Logs/dynamic_logsV2.txt'


    with open(dynamic_logfile, 'r') as f:
        for line in f:
            logs_obj.append(json.loads(line))

    # Sort by source (window.name, etc.)
    source_sorted_logs = sorted(logs_obj, key=lambda x: x['source'])

    report_gen.dynamic_results_report(source_sorted_logs, extension, soup, config, report_path)


# load configurations set by user
def load_config():


    # Load config
    with open('SHARED/config.json') as f:
        config = json.loads(f.read())


    # Check validity of config [int]
    def isValidInt(key, min, max=None):
        user_value = config[key]

        # check if int
        if not isinstance(user_value, int):
            print(f"Error: {key} ({user_value}) is not an integer.")
            print('Exiting program...')
            exit() 

        # if int, check if within range of min and max

        # check if max is set
        if max:
            if user_value < min or user_value > max:
                print(f"Error: {key} ({user_value}) must be an integer between {min} and {max}.")
                print('Exiting program...')
                exit()
        # max not set
        else:
            if user_value < min:
                print(f"Error: {key} ({user_value}) must be an integer more than {min}.")
                print('Exiting program...')
                exit()


        return True

    # Check validity of config [payload file]
    def isValidFile(key):
        user_file = config[key]

        # Check if set to default "nil"
        if user_file != "nil":

            # Check if file exists inside SHARED
            file_path = Path(f'SHARED/{user_file}')
            if not file_path.exists():
                print(f'Error: {key} ({file_path}) does not exist.')
                print('Exiting program...')
                exit()

            # Check if file ends with .txt
            if not str(file_path).endswith('.txt'):
                print(f'Error: {key} ({file_path}) does not end with .txt')
                print('Exiting program...')
                exit()

            # Check if file is at least 1 payload long
            if file_path.stat().st_size == 0:
                print(f'Error: {key} ({file_path}) is empty.')
                print('Exiting program...')
                exit()

        return True


    if isValidInt(key='report_display_adjacent_lines',min=0) and isValidInt(key='number_of_instances',min=1) and isValidInt(key='percentage_of_payloads',min=1,max=100) and isValidFile('custom_payload_file'): 
        return config

# main program
def main():
    print(get_banner())

    config = load_config()
    
    for extension in extraction():
        print()

        # Parse report template HTML content
        with open("report_template.html", "r") as f:
            soup = BeautifulSoup(f, "html.parser")

        # Get scan date
        scan_start = formatdate(localtime=True)

        # Update scan date in report
        soup.find(id="scan-date").string = scan_start

        # Initialise report path
        report_path = Path(f"SHARED/REPORTS/{extension.name} ({scan_start.replace(':','-')}).html")

        # Start static analysis
        results = static_analysis(extension, soup, config, report_path)

        # If static analysis found vulns, start dynamic analysis
        if results:
           
            dynamic_analysis(results, extension, soup, config, report_path)

if __name__ == "__main__":
    main()
