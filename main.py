import subprocess

print("start of program")


# auto semgrep scan
def run_semgrep():
    command = [
        "semgrep",
        "scan",
        "--config=STATIC_ANALYSIS/semgrep_rules",
        "STATIC_ANALYSIS/test_codes",  # replace 
        # "h1-replacer(v3)",
        "--output",
        "STATIC_ANALYSIS/semgrep_results.json",
        "--json",
        "--quiet",  # turn off verbose
    ]
    try:
        subprocess.run(command, check=True)
        print("Semgrep scan successful.")
        print("Scan results JSON found in STATIC_ANALYSIS/semgrep_results.json")
    except subprocess.CalledProcessError as e:
        print(f"Error running semgrep command: {e}")


if __name__ == "__main__":
    run_semgrep()


# auto selenium
