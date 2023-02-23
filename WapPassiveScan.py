import requests
from prettytable import PrettyTable
from os import getenv
from bs4 import BeautifulSoup
import argparse

class bcolors:
	OK = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	RESET = '\033[0m'
	INFO = '\033[94m'

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--url", help="Target a single url", type=str)
parser.add_argument("-l", "--list", help="Target a list of urls", type=str)
parser.add_argument("-o", "--output", help="Output file", type=str)
args= parser.parse_args()

API=getenv('WAPPALYZER')
endpoint = 'https://api.wappalyzer.com/lookup/v2/?urls='
headers = {'x-api-key' : API}
tab = PrettyTable(['Technology','Version','Category'])

def banner():
	print('''
			           __             __         
			|  | _  _ |__)_  _ _.   _(_  _ _  _  
			|/\|(_||_)|  (_|_)_)|\/(-__)(_(_|| ) 
			       |by S1rN3tZ                   

	''')



def APICall(url):
	print(bcolors.INFO+"[*] "+bcolors.RESET+"Calling API.\n")
	target = endpoint+url
	rt = requests.get(target, headers=headers)
	response = rt.json()
	return response
 

def ResultParsing(json):
	techlist=[]
	vlist=[]
	for techno in json[0]['technologies']:
		technology=techno['name']
		techlist.append(technology)
		version = ', '.join(techno['versions'])
		if techno['versions']:
			vlist.append(version)
		else:
			vlist.append('')
		for category in techno['categories']:
			categ=category['name']
			tab.add_row([technology, version, categ])
	return techlist, vlist

def TechVersionConcat(techlist, vlist):
	concatlist=[]
	for techno, version in zip(techlist, vlist):
			if version:
				version=version.replace(" ", "+")
				concat=techno+'+'+version
				concatlist.append(concat)
	return concatlist

def CVEcheck(techversion):
	SearchUrl = 'https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword='+techversion
	CheckRequest = requests.get(SearchUrl)
	response = CheckRequest.text
	CVEList=[]

	soup = BeautifulSoup(response, 'html.parser')
	for link in soup.find_all('a', href=lambda href: href and '/cgi-bin/cvename.cgi?name=' in href):
		print(bcolors.OK+"[+] "+bcolors.RESET+"Associated CVE: ", link.string, "link: ", "https://cve.mitre.org"+link.get('href'))
		CVE = "Associated CVE: "+link.string+" link: "+" https://cve.mitre.org"+link.get('href')+'\n'
		CVEList.append(CVE)
	return CVEList
	
def main():
	if args.output:
		file = args.output
		log = open(file, "w")
	if args.url:
		response = APICall(args.url)
		ResultParsing(response)
		print(tab)
		techlist, vlist = ResultParsing(response)
		TechVersionList = TechVersionConcat(techlist, vlist)
		print(bcolors.INFO+"\n[*] "+bcolors.RESET+'Looking for CVEs with MITRE:\n')
		for techversion in TechVersionList:
			print(bcolors.INFO+"\n[*] "+bcolors.RESET+'Checking for CVEs on',techversion,'\n')
			CVEcheck(techversion)
			if args.output:
				cveList = CVEcheck(techversion)
				tech = '\nCVE check for '+techversion+':\n\n'
				log.write(tech)
				for cve in cveList:
					log.write(cve)
		if args.output:
			log.close()
	elif args.list:
		with open(args.list, "r") as urls:
			for url in urls:
				print(bcolors.INFO+"\n\n[*] "+bcolors.RESET+'Result for',url)
				if args.output:
					log.write(url)
				response = APICall(url)
				ResultParsing(response)
				print(tab)
				techlist, vlist = ResultParsing(response)
				TechVersionList = TechVersionConcat(techlist, vlist)
				print(bcolors.INFO+"\n[*] "+bcolors.RESET+'Looking for CVEs with MITRE:\n')
				for techversion in TechVersionList:
					print(bcolors.INFO+"\n[*] "+bcolors.RESET+'Checking for CVEs on',techversion,'\n')
					CVEcheck(techversion)
					if args.output:
						cveList = CVEcheck(techversion)
						tech = '\nCVE check for '+techversion+':\n\n'
						log.write(tech)
						for cve in cveList:
							log.write(cve)
			if args.output:
				log.close()
	print('\n')

	credits = 'https://api.wappalyzer.com/v2/credits/balance/'
	rcred = requests.get(credits, headers=headers)
	respcred = rcred.json()

	print(bcolors.WARNING+"[-] "+bcolors.RESET+str(respcred['credits']),'credits remaining.\n')

try:
	banner()
	main()
except KeyboardInterrupt:
        print(bcolors.FAIL+"[!] "+bcolors.RESET+"Script canceled.")
except Exception as e:
	print(bcolors.FAIL+"[!] "+bcolors.RESET+"Error info:")
	print(e)

