# ScanExt
![alt text](https://raw.githubusercontent.com/gcmaximus/chrome-ext-scanner/main/logo.png?raw=true) 
<br><br>
## What is ScanExt?
<b>ScanExt</b> is an open-source Chrome extension scanner which automatically detects XSS vulnerabilities in Chrome extensions using Manifest V3. Static and dynamic analysis techniques are used by ScanExt.
<br><br>
<b>Semgrep</b> is utilised for static analysis of the extension's source code, using taint analysis to identify vulnerabilities in the code that attackers could exploit.
<br><br>
<b>Selenium</b> is utilised for dynamic analysis, where payloads are automatically injected into the vulnerable code segments. Payloads which execute successfully provides 100% confirmation that the flagged code segment is vulnerable to XSS.
<br><br>
A report will be generated for you, providing comprehensive information about the vulnerabilities detected in the code so that you can patch security flaws and secure your Chrome extension!

## Usage
There are 2 ways of running ScanExt:
1. Build and run on docker


```
docker build . -t <name>
docker run <name>
```

2. Run main python program directly

```
py main.py
```
