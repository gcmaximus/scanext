import json
import shutil
import subprocess
from os import makedirs
from pathlib import Path
from zipfile import ZipFile
from DYNAMIC_ANALYSIS.headless_cases import main as dynamic
from email.utils import formatdate
import jsbeautifier


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


    



# auto semgrep scan
def static_analysis(extension: Path):
    # Config rules
    rules = "STATIC_ANALYSIS/semgrep_rules/"
    # rules = "STATIC_ANALYSIS/semgrep_rules/window_name"
    # rules = "auto"

    # Codes to be scanned
    # print("FKKKKKKKKK",filename)
    # filename = "STATIC_ANALYSIS/semgrep_rules/window_name/test_codes/semgrep_test.js"
    # filename = "EXTENSIONS/h1-replacer(v3)"
    # filename = "EXTENSIONS/emailextractor"
    # filename = "EXTENSIONS/google

    # Output file
    output_file = "STATIC_ANALYSIS/semgrep_results.json"


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
        ext_name = content["name"]
        ext_version = content["version"]
        manifest_version = content["manifest_version"]
        
    print(ext_name, ext_version, manifest_version)


    # No of vulnerabilities found
    no_of_vulns = len(results)
    
    # No of POCs
    # no_of_pocs = 


    # print()





def dynamic_analysis(extracted: Path):
    dynamic()
    pass


if __name__ == "__main__":
    print("Start of program")



    
    for extension in extraction():

        # Get scan start time and append to report
        scan_start = formatdate(localtime=True)
        
        print(f'{extension.name} ({scan_start}).html')

        # with open(f'{extension.name}_{scan_start}.html', 'w') as f:

            



        static_analysis(extension)
        # dynamic_anaylsis(extension)
