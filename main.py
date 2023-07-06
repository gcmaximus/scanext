import json
import shutil
import subprocess
from os import makedirs
from pathlib import Path
from zipfile import ZipFile
from DYNAMIC_ANALYSIS.headless_cases import main as dynamic
from email.utils import formatdate
import jsbeautifier
from bs4 import BeautifulSoup


# extract extensions and format the extracted files
def extraction():
    extension_dir = "SHARED/EXTENSIONS"
    extraction_dir = "SHARED/EXTRACTED"

    types = ("*.zip", "*.crx")
    extensions = []
    for type in types:
        extensions.extend(Path(extension_dir).glob(type))

    opts = jsbeautifier.default_options()
    opts.end_with_newline = True
    opts.wrap_line_length = 80
    opts.space_after_anon_function = True

    status = Path(extraction_dir).exists()
    print(f"Checking existence of {extraction_dir} ... {status}")
    if status:
        print(f"Removing existing {extraction_dir} ...")
        shutil.rmtree(extraction_dir)
    print(f"Making {extraction_dir} ...")
    makedirs(extraction_dir)

    for extension in extensions:
        extension: Path
        indi_dir = Path(extraction_dir, extension.stem)
        makedirs(indi_dir)
        with ZipFile(extension, "r") as zip:
            zip.extractall(indi_dir)
        for file in indi_dir.glob("**/*.*"):
            if file.is_file():
                pretty = jsbeautifier.beautify_file(file, opts)
                local_options = jsbeautifier.BeautifierOptions()
                local_options.keep_quiet = True
                jsbeautifier.write_beautified_output(
                    pretty, local_options, str(file)
                )
    return Path(extraction_dir).glob('*')


    

def static_analysis(extension: Path, soup):
    # Config rules
    rules = "STATIC_ANALYSIS/semgrep_rules/"

    # Output file
    output_file = "STATIC_ANALYSIS/semgrep_results.json"

    # Command to run on CLI
    command = [
        "semgrep",
        "scan",
        f"--config={rules}",
        str(extension),
        "--quiet",
        "--json", 
        "--output",
        output_file
    ]

    try:
        subprocess.run(command, check=True)
        print("Semgrep scan successful")
        print(f"JSON scan results of `{extension.name}` found in `{output_file}`")
    except subprocess.CalledProcessError as e:
        print(f"Error running semgrep command: {e}")
        exit()

    # read the static results
    with open(output_file, "r") as static_result_file:
        results = json.load(static_result_file)["results"]
        sorted_results = sorted(results, key=lambda e: e["path"])
        sorted_results = sorted(sorted_results, key=lambda e: e["check_id"])



    # Retrieving information from Static Analysis for report

    # Name of folder scanned
    folder_scanned = extension.name

    # Information from manifest.json
    path_to_manifest = tuple(Path(extension).glob("**/manifest.json"))[0]

    with open(path_to_manifest, 'r') as f:
        content = json.load(f)

        # Extract information
        ext_name = str(content["name"])
        ext_version = str(content["version"])
        manifest_version = str(content["manifest_version"])


    # No of vulnerabilities found
    no_of_vulns = str(len(results))
    
    # No of POCs
    # no_of_pocs = 


    html_scanned_folder = soup.find(id="scanned-folder")
    html_scanned_folder.string = folder_scanned

    html_ext_name = soup.find(id="ext-name")
    html_ext_name.string = ext_name

    html_ext_version = soup.find(id="ext-version")
    html_ext_version.string = ext_version

    html_manifest_version = soup.find(id="manifest-version")
    html_manifest_version.string = manifest_version

    html_vulns = soup.find(id="vulns")
    html_vulns.string = no_of_vulns + ' found'

    # html_pocs = soup.find(id="pocs")
    # html_pocs.string = 

    # append semgrep info to report
    if len(results) == 0:
        print("sibei secure")

    else:
        # loop through & append 1 card for each result
        for result in results:
            # source = result['extra']['dataflow_trace']['taint_source'][1][1]
            # print('source: '+source)
            # sink = result['extra']['dataflow_trace']['taint_sink'][1][1]
            # print('sink: '+sink)
            vuln_id = result['check_id'].split('.')[-1]
            vuln_file = result['extra']['dataflow_trace']['intermediate_vars'][0]['location']['path'].split('SHARED/EXTRACTED/')[1]

            source, sink = vuln_id.replace('_','.').split('-')

            # find desc for source & sink
            with open("SHARED/descriptions.json", "r") as f:
                content = json.load(f)
                source_desc = content["sources"][source]
                sink_desc = content["sinks"][sink]

            print(f'{source}: {source_desc}\n{sink}: {sink_desc}')
            





    with open("test_report.html", "w") as file:
        file.write(str(soup))





def dynamic_analysis(extracted: Path):
    dynamic()
    pass


if __name__ == "__main__":
    print("Start of program")



    
    for extension in extraction():



        # # Initialise report name
        # report_name = f'{extension.name} ({scan_start}).html'


        with open('SHARED/REPORTS/report_template.html', 'r') as f:
            html_content = f.read()

        # Parse HTML content
        soup = BeautifulSoup(html_content, "html.parser")

        # Get scan date
        scan_start = formatdate(localtime=True)

        # Update scan date in report
        html_scan_date = soup.find(id="scan-date")
        html_scan_date.string = scan_start

        # Start static analysis
        static_analysis(extension,soup)


        # dynamic_anaylsis(extension)
