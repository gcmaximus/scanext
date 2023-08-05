# ScanExt
![alt text](https://github.com/gcmaximus/scanext/blob/main/logo.png?raw=true) 
<br><br>
## What is ScanExt?
<b>ScanExt</b> is an open-source Chrome extension scanner which automatically detects XSS vulnerabilities in Chrome extensions using Manifest V3. Static and dynamic analysis techniques are used by ScanExt.
<br><br>
<b>Semgrep</b> is utilised for static analysis of the extension's source code, using taint analysis to identify vulnerabilities in the code that attackers could exploit.
<br><br>
<b>Selenium</b> is utilised for dynamic analysis, where payloads are automatically injected into the vulnerable code segments. Payloads that executed successfully provides 100% confirmation that the flagged code segment is vulnerable to XSS.
<br><br>
A report will be generated for you, providing comprehensive information about the vulnerabilities detected in the code so that you can patch security flaws and secure your Chrome extension!

## Usage
There are 2 ways of running ScanExt:
1. Build and run on docker

For Linux/macOS:
```
chmod +x setup_lnx.sh
./setup_lnx.sh PATH_TO_SHARED_DIR
docker exec -it scanext_cont python3 main.py
```

For Windows:
```
setup_win.bat PATH_TO_SHARED_DIR
docker exec -it scanext_cont python3 main.py
```

2. Run main python program directly

```
python3 main.py
```
