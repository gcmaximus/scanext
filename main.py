import json
import shutil
import subprocess
from email.utils import formatdate
from pathlib import Path
from zipfile import ZipFile
import time
import threading
import html

import jsbeautifier
from bs4 import BeautifulSoup

from DYNAMIC_ANALYSIS.headless_cases import main as dynamic
from banners import get_banner


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
    print(f"Checking existence of {extraction_dir} ... {status}")
    if status:
        print(f"Removing existing {extraction_dir} ...")
        shutil.rmtree(extraction_dir)
    print(f"Making {extraction_dir} ...")
    extraction_dir.mkdir()

    for extension in extensions:
        indi_dir = Path(extraction_dir, extension.stem)
        print(f"Making {indi_dir} ...")
        indi_dir.mkdir()
        with ZipFile(extension, "r") as zip:
            print(f"Extracting {extension.name} ...", end=" ")
            zip.extractall(indi_dir)
        if not Path(indi_dir, "manifest.json").exists():
            print(f"manifest.json not found in root", end="")
            shutil.rmtree(indi_dir)
        print()
        for file in indi_dir.glob("**/*.js"):
            pretty = jsbeautifier.beautify_file(file, opts)
            local_options = jsbeautifier.BeautifierOptions()
            local_options.keep_quiet = True
            jsbeautifier.write_beautified_output(pretty, local_options, str(file))
    return Path(extraction_dir).glob("*")


def static_analysis(extension: Path, soup: BeautifulSoup):

    # Name of folder scanned
    scanned_dir = extension.name

    # Loading spinner
    def loading_spinner(scanned_dir):
        while spinner_running:
            for char in ['\\', '|', '/', '-']:
                print(f"Scanning {scanned_dir} ... {char}", end="\r")
                time.sleep(0.1)
    global spinner_running 
    spinner_running = True
    spinner_thread = threading.Thread(target=loading_spinner,args=[scanned_dir])
    spinner_thread.start()


    # Config rules
    rules = "STATIC_ANALYSIS/semgrep_rules/"

    # Output file
    output_file = "STATIC_ANALYSIS/semgrep_results.json"

    # descriptions from Tarnish
    descs = "SHARED/descriptions.json"

    # Command to run on CLI
    command = [
        "semgrep",
        "scan",
        f"--config={rules}",
        str(extension),
        "--quiet",
        "--json",
        "--output",
        output_file,
    ]

    try:
        
        subprocess.run(command, check=True)

        spinner_running = False
        spinner_thread.join()
        print(f"Scanning {scanned_dir} ... ")
        
        print("Static analysis complete.")
    except subprocess.CalledProcessError as err:
        print()
        print(f"Error running semgrep command: {err}")
        exit()

    # Skip scan for current folder
    except KeyboardInterrupt:
        
        spinner_running = False
        spinner_thread.join()
        print()
        print(f'Skipping scan for {scanned_dir}.')
        return

    # read the static results
    with open(output_file, "r") as static_result_file:
        results: list[dict] = json.load(static_result_file)["results"]
        sorted_results = sorted(results, key=lambda e: e["path"])
        sorted_results = sorted(sorted_results, key=lambda e: e["check_id"])

    # Retrieving information from Static Analysis for report

    # Information from manifest.json
    [manifest_path] = tuple(Path(extension).glob("**/manifest.json"))

    with manifest_path.open("r") as f:
        manifest = json.load(f)

        # Extract information
        ext_name = str(manifest["name"])
        ext_version = str(manifest["version"])
        manifest_version = str(manifest["manifest_version"])

    # No of vulnerabilities found
    vulns_len = len(results)

    # No of POCs (to be done after dynamic scan)
    # no_of_pocs =

    soup.find('title').string += f' - {scanned_dir}'

    soup.find(id="scanned-folder").string = scanned_dir
    soup.find(id="ext-name").string = ext_name
    soup.find(id="ext-version").string = ext_version
    soup.find(id="manifest-version").string = manifest_version
    soup.find(id="vulns").string = str(vulns_len) + " found"


    # html_pocs = soup.find(id="pocs")
    # html_pocs.string =

    # append semgrep info to report
    if vulns_len == 0:

        # no static results
        add = f"""
            <div class="card m-auto static-none border-success">
                <div class="card-header none-header">Result</div>
                <div class="card-body">
                    <h5 class="card-title">No vulnerable codes found</h5>
                    <p class="card-text">Our tool did not detect any vulnerable code segments or possible tainted data flows into vulnerable functions that could lead to XSS.</p>
                </div>
            </div>"""

        add_parsed = BeautifulSoup(add, "html.parser")
        soup.find(id="static-main").append(add_parsed)

        # no dynamic results
        add = f"""
            <div class="card m-auto dynamic-none border-success">
                <div class="card-header none-header">Result</div>
                <div class="card-body">
                    <h5 class="card-title">No POCs generated</h5>
                    <p class="card-text">Our tool did not find any payloads that can exploit potential vulnerabilities in the code.</p>
                </div>
            </div>"""
        
        add_parsed = BeautifulSoup(add, "html.parser")
        soup.find(id="dynamic-main").append(add_parsed)

    else:
        # loop through & append 1 card for each result
        result_no = 1
        for result in results:
            vuln_id = result["check_id"].split(".")[-1]
            vuln_file = Path(result["path"])

            source, sink = vuln_id.split("-")

            # find desc for source & sink
            with open(descs, "r") as f:
                content = json.load(f)
                source_desc = content["sources"][source.replace('_', '.')]
                sink_desc = content["sinks"][sink.replace('_', '.')]

            # find line no. of vuln + the line itself

            # get SS line numbers
            dataflow_trace: dict = result["extra"]["dataflow_trace"]
            source_line_no = dataflow_trace["taint_source"][1][0]["start"]["line"]
            sink_line_no = dataflow_trace["taint_sink"][1][0]["start"]["line"]

            # get source and sink lines
            vulnerable_lines = {}
            with vuln_file.open("r") as f:
                for i, line in enumerate(f):
                    if i == source_line_no - 1:
                        vulnerable_lines["source_line"] = line.strip()
                    if i == sink_line_no - 1:
                        vulnerable_lines["sink_line"] = line.strip()
                    if len(vulnerable_lines) == 2:
                        break
            source_line = vulnerable_lines.setdefault("source_line", "")
            sink_line = vulnerable_lines.setdefault("sink_line", "")
            line_diff = abs(source_line_no - sink_line_no)

            # check if:
            # 3. line difference < 1?
            code_segment = ""
            if line_diff < 1:
                code_segment = f"""
<pre class="code-block">
                    <code class="code-source">
    {source_line_no}&#9;&#9;<mark id="code-source-{result_no}">{source_line}</mark>&#9;<span class="code-comment">/* Source + Sink */</span></code>
                </pre>"""

            # 4. line difference == 1?
            elif line_diff == 1:
                code_segment = f"""
<pre class="code-block">
                    <code class="code-source">
    {source_line_no}&#9;&#9;<mark id="code-source-{result_no}">{source_line}</mark>&#9;<span class="code-comment">/* Source */</span></code><code>
    {sink_line_no}&#9;&#9;<mark id="code-sink-{result_no}">{sink_line}</mark>&#9;<span class="code-comment">/* Sink */</span></code>
                </pre>"""

            # 5. line difference > 1?
            elif line_diff > 1:
                code_segment = f"""
<pre class="code-block">
                    <code class="code-source">
    {source_line_no}&#9;&#9;<mark id="code-source-{result_no}">{source_line}</mark>&#9;<span class="code-comment">/* Source */</span></code><code>
    ...&#9;&#9;...</code><code class="code-sink">
    {sink_line_no}&#9;&#9;<mark id="code-sink-{result_no}">{sink_line}</mark>&#9;<span class="code-comment">/* Sink */</span></code>
                </pre>"""

            # 6. intermediate vars > 1? (detailed tainted path)
            inter_vars = dataflow_trace.get("intermediate_vars")
            vars_len = 0
            if inter_vars:
                vars_len = len(inter_vars)
                # print("No. of intermediate vars:", vars_len)

                if vars_len > 1:
                    tainted_lines = {}
                    line_numbers_ordered = []

                    for var in inter_vars:
                        # ignore first intermediate_vars obj
                        if inter_vars.index(var) == 0:
                            # print("ignoring")
                            pass

                        else:
                            # get tainted line numbers
                            line_no = var["location"]["start"]["line"]
                            line_numbers_ordered.append(line_no)
                            # print(line_no)
                            # get tainted lines
                            with vuln_file.open("r") as f:
                                for i, line in enumerate(f):
                                    if i == line_no - 1:
                                        tainted_lines[line_no] = line.strip()
                                        break

                    # print("Tainted Lines: ", tainted_lines)
                    # print("Line numbers ordered: ", line_numbers_ordered)
                    more_details = """
    <br>
    <h5><u>Tainted variables</u></h5>
    <pre class="code-block">"""

                    for i, line in enumerate(tainted_lines):
                        more_details += f"""<code class="code-taint">
    {line}&#9;&#9;<mark class="mark-taint" id="code-taint-{result_no}">{tainted_lines[line]}</mark>&#9;<span class="code-comment">/* Tainted */</span></code>"""
                        if len(line_numbers_ordered) - i != 1:
                            line_diff = abs(
                                line_numbers_ordered[i] - line_numbers_ordered[i + 1]
                            )
                            # print(line_diff)

                            if line_diff > 1:
                                more_details += """
    <code>...&#9;&#9;...</code>"""

                    more_details += """
                    </pre>"""
                    code_segment += more_details

            add = f"""
<!-- Source-Sink pair -->
        <div class="card static-result">
            <div class="card-header">

                <span class="float-start">
                    <i class="fa fa-file-code-o" style="font-size:20px"></i> <span
                        class="filename" id="vuln-file-{result_no}"><b>File:</b> {str(vuln_file).split('SHARED/EXTRACTED/')[1]}</span>
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
"""

            add_parsed = BeautifulSoup(add, "html.parser")
            soup.find(id="static-main").append(add_parsed)

            # Move on to append next result
            result_no += 1

    # Initialise report name
    report_path = Path(
        f"SHARED/REPORTS/{extension.name} ({scan_start.replace(':','-')}).html"
    )

    with open(report_path, "w") as file:
        file.write(str(soup))

    print(f"Report generated at `{report_path}`")


def dynamic_analysis(extension: Path, soup: BeautifulSoup):

    # i comment out first 
    # dynamic()
    
    # Retrieve information from log file
    dynamic_logfile = 'DYNAMIC_ANALYSIS/sample_logfile.txt'
    with open(dynamic_logfile, 'r') as f:
        logs = f.readlines()

    # No of logs for all sources
    log_len = len(logs)

    if log_len == 0:
        # no dynamic results
        add = f"""
            <div class="card m-auto dynamic-none border-success">
                <div class="card-header none-header">Result</div>
                <div class="card-body">
                    <h5 class="card-title">No POCs generated</h5>
                    <p class="card-text">Our tool did not find any payloads that can exploit potential vulnerabilities in the code.</p>
                </div>
            </div>"""
        
        add_parsed = BeautifulSoup(add, "html.parser")
        soup.find(id="dynamic-main").append(add_parsed)
    else:


        logs_obj = []
        for log in logs:
            # print('original log: ', log)
            log = json.loads(log)
            # print('modified log: ', log)
            # print()
            # print(type(log['packetInfo']))
            # print(log['packetInfo'])
            # input()

            # log['packetInfo'] = json.dumps()


            logs_obj.append(log)

        # Sort by source (window.name, etc.)
        source_sorted_logs = sorted(logs_obj, key=lambda x: x['source'])


        # creating dict of key(source) to value (list of objs with source)

        separated_objects = {}

        for obj in source_sorted_logs:
            source = obj['source']

            if source not in separated_objects:
                separated_objects[source] = []

            separated_objects[source].append(obj)


        '''
        {
            'window.name': [
                {'name': 'Object 1', 'source': 'window.name'},
                {'name': 'Object 3', 'source': 'window.name'}
            ],
            'location.hash': [
                {'name': 'Object 2', 'source': 'location.hash'},
                {'name': 'Object 4', 'source': 'location.hash'}
            ]
        }
        '''

        for source in separated_objects:

            results = separated_objects[source]

            # retrieve information for one source
            payload_list = results[0]['payload_fileName']
            tested_payloads = len(results)

            # Filter by outcome (only want SUCCESS)
            success_results = []
            for result in results:
                if result['outcome'] != 'SUCCESS':
                    pass
                else:
                    success_results.append(result)

            success_payloads = len(success_results)

            # print(payload_list)
            # print(tested_payloads)
            # print(success_payloads)


            payload_table = ''
            result_no = 1
            for result in success_results:

                # Retrieve information
                payload = html.escape(result['payload'])
                url = result['Url']
                time_of_injection = result['timeOfInjection']
                time_of_alert = result['timeOfAlert']

                # Format packet info for payloadType:"server"
                payload_type = result['payloadType']
                packet_info = result['packetInfo']

                if payload_type == 'server':
                    # print('packet_info: ', packet_info)
                    # print('type: ', type(packet_info))

                    packet_info_obj = json.loads(packet_info)
                    
                    # print(packet_info_obj)

                    packet_info = ""
                    for key in packet_info_obj:
                        packet_info += f'<b>{key}</b>: {packet_info_obj[key]}<br>'
                        # if key == ''

                    # packet_info = html.escape(packet_info)


                    #########################################
                    #            CONTINUE HERE              #
                    #########################################




                    print('packetinfo: ', packet_info)
                    
                else:
                    packet_info = "N.A."

                payload_table += f'''
<tr>
    <th scope="row" id="payload-no-1">{result_no}</th>
    <td class="consolas" id="payload-1">{payload}</td>
    <td class="consolas" id="payload-url-{result_no}">{url}</td>
    <td id="payload-start-{result_no}">{time_of_injection}</td>
    <td id="payload-end-{result_no}">{time_of_alert}</td>
    <td id="payload-packet-info={result_no}">{packet_info}</td>
</tr>
'''



            add = f'''
<!-- Source -->
<div class="card dynamic-result">
    <div class="card-header">
        <i class="fa fa-flag-checkered" style="font-size:20px"></i> <span
            style="font-size: 18px"><b>Source:</b> {source}</span>
    </div>
    <div class="card-body">
        <p class="card-text">
        <div class="row dynamic-info">

            <div class="row">
                <!-- Payload List -->
                <div class="col-4">
                    <i class="dynamic-info-icons fa fa-file-text-o" style="font-size:36px;"></i>
                    <h5><b>Payload list:</b></h5>
                    <code><u id="payload-list">{payload_list}</u></code>
                </div>

                <!-- No. of tested payloads -->
                <div class="col-4">
                    <i class="dynamic-info-icons fa fa-bomb" style="font-size:36px;"></i>
                    <h5><b>Tested:</b></h5>
                    <code><u id="tested-payloads">{tested_payloads} payloads</u></code>
                </div>

                <!-- No. of successful payloads -->
                <div class="col-4">
                    <i class="dynamic-info-icons fa fa-bug" style="font-size:36px;"></i>
                    <h5><b>Successful:</b></h5>
                    <code><u id="success-payloads">{success_payloads} payloads</u></code>
                </div>
            </div>



            <div class="row">
                <!-- List of successful payloads -->
                <table class="table table-bordered border-dark payload-table">
                    <thead>
                        <tr class="table-head">
                            <th scope="col">#</th>
                            <th scope="col">Payload</th>
                            <th scope="col">URL where payload was injected</th>
                            <th scope="col">Time of Injection</th>
                            <th scope="col">Time of Success</th>
                            <th scope="col">Packet Info</th>
                        </tr>
                    </thead>
                    <tbody>

                    {payload_table}

                    </tbody>

                </table>

            </div>
        </div>





        </p>

    </div>
</div>
'''
            add_parsed = BeautifulSoup(add, "html.parser")
            soup.find(id="dynamic-main").append(add_parsed)

            result_no += 1

        # Initialise report name
        report_path = Path(
            f"SHARED/REPORTS/{extension.name} ({scan_start.replace(':','-')}).html"
        )

        with open(report_path, "w") as file:
            file.write(str(soup))

        print(f"Report generated at `{report_path}`")
            
            
            




if __name__ == "__main__":
    print(get_banner())
    
    for extension in extraction():
        print()

        # Parse report template HTML content
        with open("SHARED/REPORTS/report_template.html", "r") as f:
            soup = BeautifulSoup(f, "html.parser")

        # Get scan date
        scan_start = formatdate(localtime=True)

        # Update scan date in report
        # html_scan_date = soup.find(id="scan-date")
        # assert type(html_scan_date) == Tag
        # html_scan_date.string = scan_start
        soup.find(id="scan-date").string = scan_start

        # Start static analysis
        # static_analysis(extension, soup)

        # Start dynamic analysis
        dynamic_analysis(extension, soup)
