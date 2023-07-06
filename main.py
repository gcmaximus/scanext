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
        result_no = 1
        for result in results:
            print()
            vuln_id = result['check_id'].split('.')[-1]
            vuln_file = result['path'].split('SHARED/EXTRACTED/')[1]

            source, sink = vuln_id.replace('_','.').split('-')

            # find desc for source & sink
            with open("SHARED/descriptions.json", "r") as f:
                content = json.load(f)
                source_desc = content["sources"][source]
                sink_desc = content["sinks"][sink]


            # find line no. of vuln + the line itself

            # get SS line numbers
            source_line_no = result['extra']['dataflow_trace']['taint_source'][1][0]['start']['line']

            sink_line_no = result['extra']['dataflow_trace']['taint_sink'][1][0]['start']['line']

            print("Source Line: " + str(source_line_no))
            print("Sink Line: " + str(sink_line_no))

            # get SS lines
            file = open(f'SHARED/EXTRACTED/{vuln_file}')

            vulnerable_lines = {
                "source_line": "",
                "sink_line": ""
            }
            for i, line in enumerate(file):
                if i == source_line_no-1:
                    vulnerable_lines["source_line"] = line.strip()
                
                if i == sink_line_no-1:
                    vulnerable_lines["sink_line"] = line.strip()

            print(vulnerable_lines)

            line_diff = abs(source_line_no - sink_line_no)

            print('line diff: ', line_diff)
            

            # check if:
            # 3. line difference < 1?
            if line_diff < 1:
                code_segment = f'''
<pre class="code-block">
                    <code class="code-source">
    {source_line_no}&#9;&#9;<mark id="code-source-{result_no}">{vulnerable_lines['source_line']}</mark>&#9;<span class="code-comment">/* Source + Sink */</span></code>
                </pre>'''

            # 4. line difference == 1?
            elif line_diff == 1:
                code_segment = f'''
<pre class="code-block">
                    <code class="code-source">
    {source_line_no}&#9;&#9;<mark id="code-source-{result_no}">{vulnerable_lines['source_line']}</mark>&#9;<span class="code-comment">/* Source */</span></code><code>
    {sink_line_no}&#9;&#9;<mark id="code-sink-{result_no}">{vulnerable_lines['sink_line']}</mark>&#9;<span class="code-comment">/* Sink */</span></code>
                </pre>'''

            # 5. line difference > 1?
            elif line_diff > 1:
                code_segment = f'''
<pre class="code-block">
                    <code class="code-source">
    {source_line_no}&#9;&#9;<mark id="code-source-{result_no}">{vulnerable_lines['source_line']}</mark>&#9;<span class="code-comment">/* Source */</span></code><code>
    ...&#9;&#9;...</code><code class="code-sink">
    {sink_line_no}&#9;&#9;<mark id="code-sink-{result_no}">{vulnerable_lines['sink_line']}</mark>&#9;<span class="code-comment">/* Sink */</span></code>
                </pre>'''

            # 6. intermediate vars > 1? (detailed tainted path)
            try:
                vars = result['extra']['dataflow_trace']['intermediate_vars']
                no_of_vars = len(vars)
                print("No. of intermediate vars:", no_of_vars)
            except:
                print("NO INTERMEDIATE VARS")
                no_of_vars = 0
            
            if no_of_vars > 1:
                tainted_lines = {}
                line_numbers_ordered = []

                for var in vars:

                    # ignore first intermediate_vars obj
                    if vars.index(var) == 0:
                        print('ignoring')

                    else:

                        # get tainted line numbers
                        line_no = var['location']['start']['line']
                        line_numbers_ordered.append(line_no)
                        print(line_no)
                        # get tainted lines
                        file = open(f'SHARED/EXTRACTED/{vuln_file}')
                        for i, line in enumerate(file):
                            if i == line_no-1:
                                tainted_lines[line_no] = line.strip()

                print("Tainted Lines: ", tainted_lines)
                print("Line numbers ordered: ", line_numbers_ordered)
                more_details = '''
<br>
<h5><u>More details on tainted variables</u></h5>
<pre class="code-block">'''

                counter = 0
                for line in tainted_lines:
                    more_details += f'''<code class="code-taint">
    {line}&#9;&#9;<mark class="mark-taint" id="code-taint-{result_no}">{tainted_lines[line]}</mark>&#9;<span class="code-comment">/* Tainted */</span></code>'''
                    if len(line_numbers_ordered) - counter != 1:
                        line_diff = abs(line_numbers_ordered[counter] - line_numbers_ordered[counter+1])
                        print(line_diff)


                        if line_diff > 1:
                            more_details += '''
    <code>...&#9;&#9;...</code>'''
                            
                    
                            
                    counter += 1

                    
                
                more_details += '''
                </pre>'''
                code_segment += more_details

                #check for line diff between current tainted line and prev line (tainted OR source line)




                # if line diff == 1:
                #     dont add ...
                # else:
                #     add ...
                # add tainted line

                #check for line diff between sink and last tainted line (need add ...?)


                        

                

            add = f'''
<!-- Source-Sink pair -->
        <div class="card static-result">
            <div class="card-header">
                <i class="fa fa-search" style="font-size:20px"></i> <span class="consolas" id="vuln-id-{result_no}">{vuln_id}</span>

                <span class="float-end">
                    <i class="fa fa-file-code-o" style="font-size:20px"></i> <span
                        class="consolas" id="vuln-file-{result_no}">{vuln_file}</span>
                </span>
            </div>
            <div class="card-body">
                <p class="card-text">
                <div class="row">
                    <div class="col-6 source-desc">
                        <!-- Source -->
                        <h5><u>Source ID: <code id="source-{result_no}">{source}</code></u></h5>
                        <p id="source-desc-{result_no}">{source_desc}</p>
                    </div>

                    <div class="col-6 sink-desc">
                        <!-- Sink -->
                        <h5><u>Sink ID: <code id="sink-{result_no}">{sink}</code></u></h5>
                        <p id="sink-desc-{result_no}">{sink_desc}</p>
                    </div>

                </div>
                <br><br>





                <!-- Location -->
                <h5><u>Location of vulnerability</u></h5>

                {code_segment}

                <i>*This code has been beautified by js-beautify.</i>


                </p>

            </div>
        </div>
'''
            
            add_parsed = BeautifulSoup(add, "html.parser")
            html_static_main = soup.find(id='static-main')
            html_static_main.append(add_parsed)

            result_no += 1


            



    # Initialise report name
    report_name = f'{extension.name} ({scan_start}).html'

    with open(f"SHARED/REPORTS/{report_name}", "w") as file:
        file.write(str(soup))





def dynamic_analysis(extracted: Path):
    dynamic()
    pass


if __name__ == "__main__":
    print("Start of program")



    
    for extension in extraction():






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
