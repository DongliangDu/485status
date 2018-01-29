#!/bin/python

#used to check the USCIS-SRC I-485 cases status
#first get the 485 case numbers you want to check and put it in a file named "input-casenum"
#you can check the status weekly or monthly, just run "python check-485status.py"

import sys
import urllib

def getHtml(url):
	try:
		page = urllib.urlopen(url)
		html = page.read()
		return html
	except:
		pass


def getInfo(filename,casenum):
	try:
		fh = open(filename, "r")
	except:
		print "No file named %s" % (filename)
		sys.exit(1)
	
	status = ""
	while True:
		line = fh.readline()
		line = line.strip()
		if not line: break
		if line.startswith("<p>On") and line.find(casenum) != -1:
			status = line
		else:
			status = ",,No status infor."
	return status


def main():
	try:
		input_fh = open("input-casenum","r")
	except:
		print "No input file: input-casenum"
		sys.exit(1)
	
	dic = {}
	
	while True:
		input_line = input_fh.readline()
		if not input_line: break
		input_line = input_line.strip()
		print input_line
		#download the html page
		html_address = "https://egov.uscis.gov/casestatus/mycasestatus.do?multiFormAappReceiptNum=SRC" + input_line
		html_file = "SRC" + input_line + ".html"
		html_fh = open(html_file,"w")
		try:
			html = getHtml(html_address)
			html_fh.write(html)
			html_fh.close()
		except:
			pass

		case_status = getInfo(html_file,input_line)
		dic[input_line] = case_status
	
	output_fh = open("output-casestatus", "w")
	
	for key, value in dic.iteritems():
		date = value.split(",")[0][6:]
		status = value.split(",")[2]
		output_fh.write("%s\t%s\t%s\n" % (key, date, status))
	output_fh.close()
	
if __name__ == '__main__':
	main()

