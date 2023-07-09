import json
import shutil
import subprocess
from email.utils import formatdate
from pathlib import Path
from zipfile import ZipFile
import random

import jsbeautifier
from bs4 import BeautifulSoup

from DYNAMIC_ANALYSIS.headless_cases import main as dynamic


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
    # Config rules
    rules = "STATIC_ANALYSIS/semgrep_rules/"

    # Output file
    output_file = "STATIC_ANALYSIS/semgrep_results.json"

    # Name of folder scanned
    scanned_dir = extension.name

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
        print(f"Scanning {scanned_dir} ...")
        subprocess.run(command, check=True)
        print("Static analysis complete.")
        # print(f"JSON scan results of `{scanned_dir}` found in `{output_file}`")
    except subprocess.CalledProcessError as err:
        print(f"Error running semgrep command: {err}")
        exit()

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

    # No of POCs
    # no_of_pocs =

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
        print("extension sibei secure")
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

        # add no results for dynamic too?

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

            # print("Source Line: " + str(source_line_no))
            # print("Sink Line: " + str(sink_line_no))

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
            # print(vulnerable_lines)
            # print("line diff: ", line_diff)

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

                    # check for line diff between current tainted line and prev line (tainted OR source line)

                    # if line diff == 1:
                    #     dont add ...
                    # else:
                    #     add ...
                    # add tainted line

                    # check for line diff between sink and last tainted line (need add ...?)

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

            result_no += 1

    # Initialise report name
    report_path = Path(
        f"SHARED/REPORTS/{extension.name} ({scan_start.replace(':','-')}).html"
    )

    with open(report_path, "w") as file:
        file.write(str(soup))

    print(f"Report generated at `{report_path}`")


def dynamic_analysis(extension: Path):
    dynamic()
    pass

banner1 = """
   _____                 ______      _  
  / ____|               |  ____|    | |  
 | (___   ___ __ _ _ __ | |__  __  _| |_ 
  \___ \ / __/ _` | '_ \|  __| \ \/ / __|
  ____) | (_| (_| | | | | |____ >  <| |_ 
 |_____/ \___\__,_|_| |_|______/_/\_\\__|"""

banner2 = """
  .-')                ('-.         .-') _   ('-.  ) (`-.      .-') _    
 ( OO ).             ( OO ).-.    ( OO ) )_(  OO)  ( OO ).   (  OO) )   
(_)---\_)   .-----.  / . --. /,--./ ,--,'(,------.(_/.  \_)-./     '._  
/    _ |   '  .--./  | \-.  \ |   \ |  |\ |  .---' \  `.'  / |'--...__) 
\  :` `.   |  |('-..-'-'  |  ||    \|  | )|  |      \     /\ '--.  .--' 
 '..`''.) /_) |OO  )\| |_.'  ||  .     |/(|  '--.    \   \ |    |  |    
.-._)   \ ||  |`-'|  |  .-.  ||  |\    |  |  .--'   .'    \_)   |  |    
\       /(_'  '--'\  |  | |  ||  | \   |  |  `---. /  .'.  \    |  |    
 `-----'    `-----'  `--' `--'`--'  `--'  `------''--'   '--'   `--'   
"""

banner3 = """
   SSSSSSSSSSSSSSS                                                    EEEEEEEEEEEEEEEEEEEEEE                           tttt          
 SS:::::::::::::::S                                                   E::::::::::::::::::::E                        ttt:::t          
S:::::SSSSSS::::::S                                                   E::::::::::::::::::::E                        t:::::t          
S:::::S     SSSSSSS                                                   EE::::::EEEEEEEEE::::E                        t:::::t          
S:::::S               cccccccccccccccc aaaaaaaaaaaaa nnnn  nnnnnnnn     E:::::E       EEEEExxxxxxx      xxxxxxttttttt:::::ttttttt    
S:::::S             cc:::::::::::::::c a::::::::::::an:::nn::::::::nn   E:::::E             x:::::x    x:::::xt:::::::::::::::::t    
 S::::SSSS         c:::::::::::::::::c aaaaaaaaa:::::n::::::::::::::nn  E::::::EEEEEEEEEE    x:::::x  x:::::x t:::::::::::::::::t    
  SS::::::SSSSS   c:::::::cccccc:::::c          a::::nn:::::::::::::::n E:::::::::::::::E     x:::::xx:::::x  tttttt:::::::tttttt    
    SSS::::::::SS c::::::c     ccccccc   aaaaaaa:::::a n:::::nnnn:::::n E:::::::::::::::E      x::::::::::x         t:::::t          
       SSSSSS::::Sc:::::c              aa::::::::::::a n::::n    n::::n E::::::EEEEEEEEEE       x::::::::x          t:::::t          
            S:::::c:::::c             a::::aaaa::::::a n::::n    n::::n E:::::E                 x::::::::x          t:::::t          
            S:::::c::::::c     cccccca::::a    a:::::a n::::n    n::::n E:::::E       EEEEEE   x::::::::::x         t:::::t    tttttt
SSSSSSS     S:::::c:::::::cccccc:::::a::::a    a:::::a n::::n    n::::EE::::::EEEEEEEE:::::E  x:::::xx:::::x        t::::::tttt:::::t
S::::::SSSSSS:::::Sc:::::::::::::::::a:::::aaaa::::::a n::::n    n::::E::::::::::::::::::::E x:::::x  x:::::x       tt::::::::::::::t
S:::::::::::::::SS  cc:::::::::::::::ca::::::::::aa:::an::::n    n::::E::::::::::::::::::::Ex:::::x    x:::::x        tt:::::::::::tt
 SSSSSSSSSSSSSSS      cccccccccccccccc aaaaaaaaaa  aaaannnnnn    nnnnnEEEEEEEEEEEEEEEEEEEEExxxxxxx      xxxxxxx         ttttttttttt  """

banner4 = """

░██████╗░█████╗░░█████╗░███╗░░██╗███████╗██╗░░██╗████████╗
██╔════╝██╔══██╗██╔══██╗████╗░██║██╔════╝╚██╗██╔╝╚══██╔══╝
╚█████╗░██║░░╚═╝███████║██╔██╗██║█████╗░░░╚███╔╝░░░░██║░░░
░╚═══██╗██║░░██╗██╔══██║██║╚████║██╔══╝░░░██╔██╗░░░░██║░░░
██████╔╝╚█████╔╝██║░░██║██║░╚███║███████╗██╔╝╚██╗░░░██║░░░
╚═════╝░░╚════╝░╚═╝░░╚═╝╚═╝░░╚══╝╚══════╝╚═╝░░╚═╝░░░╚═╝░░░"""

banner5 = """
                                                                 
 ▄█▀▀▀█▄█                           ▀███▀▀▀███            ██   
▄██    ▀█                             ██    ▀█            ██   
▀███▄    ▄██▀██ ▄█▀██▄ ▀████████▄     ██   █  ▀██▀   ▀██▀█████ 
  ▀█████▄█▀  ████   ██   ██    ██     ██████    ▀██ ▄█▀   ██   
▄     ▀███      ▄█████   ██    ██     ██   █  ▄   ███     ██   
██     ███▄    ▄█   ██   ██    ██     ██     ▄█ ▄█▀ ██▄   ██   
█▀█████▀ █████▀▀████▀██▄████  ████▄ ▄████████████▄   ▄██▄ ▀████"""

banners = [banner1,banner2,banner3,banner4,banner5]
if __name__ == "__main__":
    random.shuffle(banners)
    print(banners[-1], end="\n\n")
    
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
        static_analysis(extension, soup)

        # Start dynamic analysis
        dynamic_analysis(extension)
