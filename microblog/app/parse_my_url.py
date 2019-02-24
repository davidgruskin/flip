from urllib.request import Request
from urllib.request import urlopen
from bs4 import BeautifulSoup

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}


TRIGGERS = ["sucide", "mental health", "CloudGoogle", "Learn"]

def parse_my_url(url):
	req = Request(url, headers=hdr)

	try:
		page = urlopen(req)
		#html = urlopen(url).read()
		html = page.read()
		soup = BeautifulSoup(html, 'lxml')

		# kill all script and style elements
		for script in soup(["script", "style"]):
		    script.extract()    # rip it out

		# get text
		text = soup.get_text()

		# break into lines and remove leading and trailing space on each
		lines = (line.strip() for line in text.splitlines())
		# break multi-headlines into a line each
		chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
		# drop blank lines
		text = ' '.join(chunk for chunk in chunks if chunk)

		header = ""
		# FIND HEADER
		for a in ["h1","h2","h3", "h4", "h5"]:
			header = soup.find_all(a)
			if header:
				break

		header = header[0].contents[0]
		found_triggers = []

		found_triggers = has_trigger_words(header, found_triggers) 
		found_triggers = has_trigger_words(text, found_triggers)
		
		print(header)
		print(text)

		return (header, text, found_triggers)
	except:
	    print("ERROR")

	return ("", "", [])

def has_trigger_words(text, found_triggers): 
	for t in TRIGGERS:
		if t in text:
			found_triggers.append(t) 
	return found_triggers

