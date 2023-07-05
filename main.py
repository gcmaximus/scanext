import subprocess
import json
import zipfile


# Config rules
rules = "STATIC_ANALYSIS/semgrep_rules/"
# rules = "STATIC_ANALYSIS/semgrep_rules/window_name"
# rules = "auto"

# Codes to be scanned
filename = "SHARED/EXTENSIONS"
# filename = "STATIC_ANALYSIS/semgrep_rules/window_name/test_codes/semgrep_test.js"
# filename = "EXTENSIONS/h1-replacer(v3)"
# filename = "EXTENSIONS/emailextractor"
# filename = "EXTENSIONS/google

# Output file
output_file = "STATIC_ANALYSIS/semgrep_results.json"


# auto semgrep scan
def static_analysis():
    command = [
        "semgrep",
        "scan",
        f"--config={rules}",
        filename,
        "--output",
        output_file,
        "--json",
    ]
    try:
        subprocess.run(command, check=True)
        print("Semgrep scan successful.")
        print(f"JSON scan results of `{filename}` found in `{output_file}`")
    except subprocess.CalledProcessError as e:
        print(f"Error running semgrep command: {e}")
        exit()

    # read the static results
    with open(output_file, "r") as static_result_file:
        results = json.load(static_result_file)["results"]
        sorted_results = sorted(results, key=lambda e: e["path"])
        sorted_results = sorted(sorted_results, key=lambda e: e["check_id"])


def dynamic_anaylsis():
    pass


if __name__ == "__main__":
    print("start of program")
    static_analysis()
    dynamic_anaylsis()


# auto selenium
# import something
