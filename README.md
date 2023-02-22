# WapPassiveScan
Passive Vulnerability Scanner working with Wappalyzer API and MITRE CVE search functionnality.

## Prerequisites:

- requests
- BeautifulSoup
- PrettyTable
- argparse

## Install:
```bash
$ git clone https://github.com/mathis2001/WapPassiveScan

$ cd WapPassiveScan

$ python3 WapPassiveScan.py
```
## Usage:

First, You will have to create an account on https://www.wappalyzer.com/. Then, go to https://www.wappalyzer.com/apikey/ and generate a new API key.
After that, all you have to do is creating a variable named 'WAPPALYZER' in your environment variables containing the key and starting using the tool like that:

```bash
./WapPassiveScan.py [-u url] [-l list of urls]
```


## Options:
```bash
  -h, --help  show this help message and exit
  
  -u, --url   target a single url
  
  -l, --list  target a list of urls in a file
 
```
## Screenshots:

![image](https://user-images.githubusercontent.com/40497633/220649892-64b5d5d0-2b23-46b3-a056-f0da637e8621.png)

![image](https://user-images.githubusercontent.com/40497633/220650116-e85c07b3-6102-4208-be58-2168a42d8e8d.png)
