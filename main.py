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
    # dynamic(extension, results)

    print('Dynamic analysis complete.')
    print()
    
    # Retrieve information from log file
    logs_obj = []

    # dynamic_logfile = 'dynamic_logs.txt'
    dynamic_logfile = 'DYNAMIC_ANALYSIS_v2/dynamic_logs.txt'


    with open(dynamic_logfile, 'r') as f:
        for line in f:
            logs_obj.append(json.loads(line))

    # Sort by source (window.name, etc.)
    source_sorted_logs = sorted(logs_obj, key=lambda x: x['source'])

    report_gen.dynamic_results_report(source_sorted_logs, extension, soup, config, report_path)

# check if int > 0
###################
###### TO DO ######
###################
def checkInt(target):

    # check if int
    if not isinstance(target, int):
        print(f"Please set {target} to be an integer, 0 or more!")
        exit() 

    # if int, check if < 0
    elif target < 0:
        print(f"Please set {target} to be an integer, 0 or more!")
        exit()

    return target


# load configurations set by user
def load_config():

    # Load config and check validity.
    with open('SHARED/config.json') as f:
        config = json.loads(f.read())
    

    ###################
    ###### TO DO ######
    ###################
    report_display_adjacent_lines = checkInt(config['report_display_adjacent_lines'])
    number_of_instances = checkInt(config['number_of_instances'])

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
