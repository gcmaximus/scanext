import time
import threading


def main(scanned_dir):
    # Loading spinner
    def loading_spinner(scanned_dir, event):
        while event.is_set():
            for char in ['\\', '|', '/', '-']:
                print(f"Scanning {scanned_dir} for vulnerabilities ... {char}", end="\r")
                time.sleep(0.1)
    event = threading.Event()
    return event, threading.Thread(target=loading_spinner,args=[scanned_dir, event])
