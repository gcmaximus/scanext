import json
import shutil
import subprocess
from email.utils import formatdate
from pathlib import Path
from zipfile import ZipFile
import html

import jsbeautifier
from bs4 import BeautifulSoup

from headless_cases import main as dynamic
from banners import get_banner
from spinner import main as spinner


cross = "⤫"
tick = "✓"


def icon(boolean: bool):
    if boolean:
        return tick
    return cross


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
        print(tick)
    print(f"Making {extraction_dir} ... ", end="")
    extraction_dir.mkdir()
    print(tick)

    for extension in extensions:
        indi_dir = Path(extraction_dir, extension.stem)
        print(f"Making {indi_dir} ... ", end="")
        indi_dir.mkdir()
        print(tick)

        with ZipFile(extension, "r") as zip:
            print(f"Extracting {extension.name} ... ", end="")
            zip.extractall(indi_dir)
        manifest_exists = Path(indi_dir, "manifest.json").exists()
        print(icon(manifest_exists))
        if not manifest_exists:
            print(f"{cross} manifest.json not found in root", end="")
            shutil.rmtree(indi_dir)
        for file in indi_dir.glob("**/*.js"):
            pretty = jsbeautifier.beautify_file(file, opts)
            local_options = jsbeautifier.BeautifierOptions()
            local_options.keep_quiet = True
            jsbeautifier.write_beautified_output(pretty, local_options, str(file))
    return Path(extraction_dir).glob("*")


def static_analysis(extension: Path, soup: BeautifulSoup, config):

    # Name of folder scanned
    scanned_dir = extension.name


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
        spinner_event, spinner_thread = spinner(scanned_dir)
        spinner_event.set()
        spinner_thread.start()
        subprocess.run(command)
    except KeyboardInterrupt:
        spinner_event.clear()
        spinner_thread.join()
        print(f"Scanning {scanned_dir} for vulnerabilities ... {cross}  ")
        print("Terminating program ...")
        exit()
    spinner_event.clear()
    spinner_thread.join()
    print(f"Scanning {scanned_dir} for vulnerabilities ... {tick}")

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

    soup.find('title').string += f' - {scanned_dir}'

    soup.find(id="scanned-folder").string = scanned_dir
    soup.find(id="ext-name").string = ext_name
    soup.find(id="ext-version").string = ext_version
    soup.find(id="manifest-version").string = manifest_version
    soup.find(id="vulns").string = str(vulns_len) + " found"

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
                        vulnerable_lines["source_line"] = html.escape(line.rstrip())
                    if i == sink_line_no - 1:
                        vulnerable_lines["sink_line"] = html.escape(line.rstrip())
                    if len(vulnerable_lines) == 2:
                        break
            source_line = vulnerable_lines.setdefault("source_line", "")
            sink_line = vulnerable_lines.setdefault("sink_line", "")
            line_diff = abs(source_line_no - sink_line_no)


            


            # check if:
            # line difference < 1?
            code_segment = ""
            if line_diff < 1:
                code_segment = f"""
<pre class="code-block" id="code-block-{result_no}"><code class="code-source">
    {source_line_no}&#9;&#9;<mark id="code-source-{result_no}">{source_line}</mark>&#9;<span class="code-comment">/* Source + Sink */</span></code></pre>"""

            # line difference == 1?
            elif line_diff == 1:
                code_segment = f"""
<pre class="code-block" id="code-block-{result_no}"><code class="code-source">
    {source_line_no}&#9;&#9;<mark id="code-source-{result_no}">{source_line}</mark>&#9;<span class="code-comment">/* Source */</span></code><code>
    {sink_line_no}&#9;&#9;<mark id="code-sink-{result_no}">{sink_line}</mark>&#9;<span class="code-comment">/* Sink */</span></code></pre>"""

            # line difference > 1?
            elif line_diff > 1:
                code_segment = f"""
<pre class="code-block" id="code-block-{result_no}"><code class="code-source">
    {source_line_no}&#9;&#9;<mark id="code-source-{result_no}">{source_line}</mark>&#9;<span class="code-comment">/* Source */</span></code><code>
    ...&#9;&#9;...</code><code class="code-sink">
    {sink_line_no}&#9;&#9;<mark id="code-sink-{result_no}">{sink_line}</mark>&#9;<span class="code-comment">/* Sink */</span></code></pre>"""

            # intermediate vars > 1? (provide detailed tainted path)
            inter_vars = dataflow_trace.get("intermediate_vars")
            vars_len = 0
            if inter_vars:
                vars_len = len(inter_vars)

                if vars_len > 1:
                    tainted_lines = {}
                    line_numbers_ordered = []

                    for var in inter_vars:
                        # ignore first intermediate_vars obj
                        if inter_vars.index(var) == 0:
                            pass
                        else:
                            # get tainted line numbers
                            line_no = var["location"]["start"]["line"]
                            line_numbers_ordered.append(line_no)

                            # get tainted lines
                            with vuln_file.open("r") as f:
                                for i, line in enumerate(f):
                                    if i == line_no - 1:
                                        tainted_lines[line_no] = html.escape(line.rstrip())
                                        break

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

                            if line_diff > 1:
                                more_details += """
    <code>...&#9;&#9;...</code>"""

                    more_details += """
                    </pre>"""
                    code_segment += more_details

            
            



            soup_code_segment = BeautifulSoup(code_segment, "html.parser")

            # check file length
            with open(vuln_file, 'r') as f:
                total_file_len = len(f.readlines())

            # {line no:line content}
            report_display_adjacent_lines = config['report_display_adjacent_lines']
            prepend_lines = {source_line_no - x - 1: "" for x in range(report_display_adjacent_lines) if source_line_no - x - 1 > 0}
            append_lines = {sink_line_no + x + 1: "" for x in range(report_display_adjacent_lines) if sink_line_no + x + 1 <= total_file_len}

            with open(vuln_file, 'r') as f:
                for i, line in enumerate(f):
                    if i+1 in prepend_lines.keys():
                        prepend_lines[i+1] = html.escape(line.rstrip())
                    if i+1 in append_lines.keys():
                        append_lines[i+1] = html.escape(line.rstrip())
                        
            prepend_lines = dict(sorted(prepend_lines.items(), reverse=True))

            # Prepending lines
            for line_no, line in prepend_lines.items():
                soup_prepend_content = BeautifulSoup(f"""<code>
    {line_no}&#9;&#9;{line}</code>""", 'html.parser')
                soup_code_segment.find(id=f'code-block-{result_no}').insert(0, soup_prepend_content)
                


            # Appending lines
            for line_no, line in append_lines.items():
                soup_append_content = BeautifulSoup(f"""<code>
    {line_no}&#9;&#9;{line}</code>""", 'html.parser')
                soup_code_segment.find(id=f'code-block-{result_no}').append(soup_append_content)

                # if last line, append one more newline in <pre>
                if line_no == max(append_lines.keys()):
                    soup_code_segment.find(id=f'code-block-{result_no}').append("""

""")


            
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

                {str(soup_code_segment)}

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




def dynamic_analysis(extension: Path, soup: BeautifulSoup, config):

    print()
    print('Conducting dynamic analysis ...')

    # call selenium main.py
    # dynamic()

    print('Dynamic analysis complete.')
    print()
    
    # Retrieve information from log file
    logs_obj = []

    # to change during integration
    dynamic_logfile = 'DYNAMIC_ANALYSIS/sample_logfile.txt'

    with open(dynamic_logfile, 'r') as f:
        for line in f:
            logs_obj.append(json.loads(line))

    # Sort by source (window.name, etc.)
    source_sorted_logs = sorted(logs_obj, key=lambda x: x['source'])


    # creating dict of key(source) to value (list of objs with source)

    separated_objects = {}
    succ_counter = 0
    for obj in source_sorted_logs:
        source = obj['source']
        separated_objects.setdefault(source, {"results":[], "total number": 0, "total success":0})
        source_dict = separated_objects[source]
        source_dict["total number"] += 1
        if obj["outcome"] == "SUCCESS":
            source_dict["results"].append(obj)
            source_dict["total success"] += 1
            succ_counter += 1

    # Update no. of POCs found
    soup.find(id='pocs').string = str(succ_counter) + ' found'
    
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

    if succ_counter == 0:
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
        # loop through dynamic results
        add = ""
        source_no = 1
        for source in separated_objects:
            source_dict: dict = separated_objects[source]

            if not source_dict["total success"]:
                continue
            results: list = source_dict["results"]

            # retrieve information for one source
            payload_list = results[0]['payload_fileName']
            tested_payloads: int = source_dict["total number"]
            success_payloads: int = source_dict["total success"]

            payload_table = ''
            
            for i, result in enumerate(results):

                # Retrieve information
                payload = html.escape(result['payload'])
                url = result['Url']
                time_of_injection = result['timeOfInjection']
                time_of_alert = result['timeOfAlert']

                # Format packet info for payloadType:"server"
                payload_type = result['payloadType']
                packet_info_obj = result['packetInfo'][0]

                if payload_type == 'server':

                    packet_info = ""
                    for key in packet_info_obj:
                        packet_info += f'<b>{key}</b>: {packet_info_obj[key]}; '

                        #########################################
                        #            DO NICER STYLING           #
                        #########################################


                    
                else:
                    packet_info = "N.A."

                payload_table += f'''
    <!-- Payload Info -->

    <h3 id="payload-no-1"><u><b>Payload #{i + 1}</b></u></h3>
    <table class="table border-dark payload-table mb-3">
    <tbody>
        <tr class="table-head">
            <th>Payload</th>
            <th>Location of Injection</th>
        </tr>

        <tr>
            <td id="payload-{i + 1}" class="consolas">{payload}</td>
            <td id="payload-url-{i + 1}" class="consolas">{url}</td>
        </tr>

        <tr class="table-head">
            <th>Time of Injection</th>
            <th>Time of Alert</th>
        </tr>

        <tr>
            <td id="payload-start-{i + 1}">{time_of_injection}</td>
            <td id="payload-end-{i + 1}">{time_of_alert}</td>
        </tr>

        <tr class="table-head">
            <th colspan="2">Packet Info</th>
        </tr>

        <tr>
            <td colspan="2" id="payload-packet-info-{i + 1}">{packet_info}</td>
        </tr>
    </tbody>

    </table>
    '''



            add += f'''
    <!-- Source -->
    <div class="card dynamic-result">
    <div class="card-header">
        <i class="fa fa-flag-checkered" style="font-size:20px"></i> <span
            style="font-size: 18px"><b>Source {source_no} :</b> <u>{source}</u></span>
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



            <div class="row table-row">


            {payload_table}


            </div>
        </div>





        </p>

    </div>
    </div>
    '''
            
            

            source_no += 1





        add_parsed = BeautifulSoup(add, "html.parser")
        soup.find(id="dynamic-main").append(add_parsed)

    

    # Initialise report name
    report_path = Path(
        f"SHARED/REPORTS/{extension.name} ({scan_start.replace(':','-')}).html"
    )

    with open(report_path, "w") as file:
        file.write(str(soup))

    print(f"Report generated at `{report_path}`")
            
            
            
def load_config():
    # Load and check validity of config.

    # Get number of adjacent lines to display in report
    with open('SHARED/config.json') as f:
        config = json.loads(f.read())
    
    # initialise
    report_display_adjacent_lines = config['report_display_adjacent_lines']

    # validate if value not int
    if not isinstance(report_display_adjacent_lines, int):
        print("Please set display_adjacent_lines to be an integer, 0 or more!")
        exit() 

    # if int, check if < 0
    elif report_display_adjacent_lines < 0:
        print("Please set display_adjacent_lines to be an integer, 0 or more!")
        exit()


    return config
    

if __name__ == "__main__":
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

        # Start static analysis
        static_analysis(extension, soup, config)

        # Start dynamic analysis
        dynamic_analysis(extension, soup, config)
