import subprocess
from pathlib import Path

from constants import *
from spinner import main as spinner


# run Semgrep scan for static analysis
def main(extension: Path):

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
        output_file,
    ]
    spinner_event, spinner_thread = spinner(extension.name)
    try: 
        spinner_event.set()
        spinner_thread.start()
        subprocess.run(command)
    except KeyboardInterrupt:
        spinner_event.clear()
        spinner_thread.join()
        print(f"Scanning {extension.name} for vulnerabilities ... {CROSS}  ")
        print("Exiting programme ...")
        exit()
    spinner_event.clear()
    spinner_thread.join()
    print(f"Scanning {extension.name} for vulnerabilities ... {TICK}")
    return output_file

if __name__ == '__main__':
    main(Path())