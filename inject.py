#!/usr/bin/python3
"""
Description:
	Tries to inject hidden common parameters to basic HTTP requests. Reveals any hidden parameters if any
	were accepted and changed the content of the page.
"""
from   bs4         import BeautifulSoup
from   core.colors import *
import argparse
import requests
import json


# Defines the parser:
parser = argparse.ArgumentParser(
	description = 'Tries to inject random parameters from a word-list to a URL\s in order to reveal any hidden parameters.')

# Arguments that can be supplied:
parser.add_argument('-u',        help = 'Target URL.',                  dest = 'url')
parser.add_argument('-o',        help = 'Path for the output file (No need to type extension. Saving as JSON file. '
                                 'Default: '
                                 'accepted_params.json)',                          dest = 'output_path',
                    default = 'accepted_params.json')
parser.add_argument('-f',        help = 'Wordlist Path.',               dest = 'wordlist',    default =
'common-params.txt')
parser.add_argument('--urls',    help = 'File Containing Target URLs.', dest = 'url_file')
parser.add_argument('--headers', help = 'Add Headers.',                 dest = 'headers', nargs = '?', const = True)
parser.add_argument('--json',    help = 'Treat POST Data as JSON',      dest = 'jsonData', action = 'store_true')
args = parser.parse_args()

# Arguments to be parsed:
url         = args.url
url_file    = args.url_file
headers     = args.headers
jsonData    = args.jsonData
wordlist    = args.wordlist
output_path = args.output_path



urls = []
def urls_list_maker():
	"""Creates a list of URLs to run on from a file with a list of URLs."""
	print(f'%s Listing all URLs from: %s{url_file}%s.' % (run, bold, end))
	try:
		with open(url_file, 'r', encoding = "utf8") as file:
			for line in file:
				urls.append(line.strip('\n'))
	except FileNotFoundError as e:
		exit(f'%s%s [ERROR] The specified file for URLs doesn\'t exist:%s\n{e}' % (bad, red, end))


paramList = []
def param_list_maker():
	"""Creates a lst of parameters to inject to the URL\s from a file with a list of parameters."""
	print(f'%s Listing all parameters from: %s{wordlist}%s.' % (run, bold, end))
	try:
		with open(wordlist, 'r', encoding = "utf8") as file:
			for line in file:
				paramList.append(line.strip('\n'))
	except FileNotFoundError as e:
		exit(f'%s%s [ERROR] The specified file for parameters word list doesn\'t exist:%s\n{e}' %(bad, red,
		                                                                                         end))
	

def original_length(url: str) -> int:
	"""url = url that's getting injected with params.
Return the length (int) of the response from the specified URL."""
	r = requests.get(url, headers = headers)
	content = BeautifulSoup(r.content, "lxml").text
	return len(content)
	

final_results = {}
def start():
	"""Defines final_results dictionary: {key: [value]} Example: {url: [list of found_params]}
Sets the value of key to the found_params list.
Outputs found_params to console."""
	global url
	print('%s %sStarting parameters injection...%s' % (run, bold, end))
	if url:
		final_results[url] = []
		try:
			final_results[url] = inject(url, headers)
			if final_results[url]:
				print(f"%s Inject found parameters for: %s{url}%s:" %(good, bold, end))
				for result in final_results[url]:
					print(tab + good + ' ' + bold + green + result + end)
			else:
				print(f"{tab}%s Couldn't find any hidden parameters." % bad)
		except ConnectionError as e:
			exit(f'%s%s[ERROR] Target encountered connection error:%s\n{e}' %(bad, red, end))
	elif urls:
		for url in urls:
			final_results[url] = []
			try:
				final_results[url] = inject(url, headers)
				if final_results[url]:
					print(f"%s Inject found parameters for: %s{url}%s:" % (good, bold, end))
					for result in final_results[url]:
						print(tab + good + ' ' + green + bold + result + end)
				else:
					print(f"{tab}%s Couldn't find any hidden parameters." % bad)
			except ConnectionError as e:
				exit(f'%s%s[ERROR] Target encountered connection error:%s\n{e}' % (bad, red, end))
				print(f'%s[INFO] Passing injection to: {url}...' % info)
				pass
    

def inject(url: str, headers: dict) -> list:
	"""url = url that's getting injected with params.
headers = Default headers or headers from parser if specified.
Injects parameters to the URL\s specified. Comparing length of the content of the response with the param.
If length was changed - appends the param to found_params.
Returns found_params list."""
	found_params = []
	print(f'\n%s Injecting to: %s{url}%s...' %(run, bold, end))
	for param in paramList:
		r = requests.get(url, headers = headers, params = {param: 1})
		content = BeautifulSoup(r.content, "lxml").text
		length = len(content)
		if length != original_length(url):
			print(f"{tab}%s Accepted Parameter: %s{param}%s" % (good, bold, end))
			found_params.append(param)
	return found_params


def output() -> json:
	"""Finally, saves final_results to JSON file."""
	global output_path
	if ".json" in output_path:
		with open(str(output_path), 'w', encoding = "utf8") as json_output:
			json.dump(final_results, json_output, sort_keys = True, indent = 4)
		print(f'%s Final results saved to JSON file as: %s{output_path}%s' % (info, bold, end))
	else:
		output_path = output_path + '.json'
		output()
	

if __name__ == "__main__":
	if not url and not url_file:
		exit('%s%s%s Please specify URL (-u) or URLs list file (--urls).%s' % (bad, red, bold, end))
	if jsonData:
		headers['Content-type'] = 'application/json'
	if type(headers) == bool:
		headers = extractHeaders(prompt())
	elif type(headers) == str:
		headers = extractHeaders(headers)
	else:
		headers = {
			'User-Agent'               : 'Mozilla/5.0 (X11; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/78.0',
			'Accept'                   : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'Accept-Language'          : 'en-US,en;q=0.5',
			'Accept-Encoding'          : 'gzip, deflate',
			'DNT'                      : '1',
			'Connection'               : 'keep-alive',
			'Upgrade-Insecure-Requests': '1'
			}
	if url_file:
		urls_list_maker()
	param_list_maker()
	start()
	output()
