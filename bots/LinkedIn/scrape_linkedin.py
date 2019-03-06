#!/usr/bin/env python3
import requests
import re
import argparse


# Declare global variables
google_key = "X"
people = []
goog_results = 20
final_list_of_people = []
end_text = "\033[0m"
yellow_text = "\033[93m"
green_text = "\033[92m"
output_file = 0


def scrape_linkedin(company,goog_results,output_file):
	# Assemble the URL from user input + API Key
	print("{0}[+] Scraping...{1}".format(green_text,end_text))
	url = ("https://www.google.com/search?q=site:linkedin.com+inurl:/in/+{0}&key={1}&num={2}".format(
															company,google_key,goog_results))
	
	# Attempt to retrieve the results
	try:
		r = requests.get(url)
	except:
		print("{0}[-] Connection failed, are you online?{1}".format(yellow_text,end_text))

	# Regex out just Google result entries, send it to sanitize_results for further clean up
	result_regex = "<h3 class=\"r\">.*</h3>"
	search_results = re.findall(result_regex,r.text)
	sanitize_results(search_results)

	# Take the sanitized list, and print the final clean list of enumerated users
	final_list_of_people.sort()
	print("{0}[+] Results: {1}".format(green_text,end_text))
	for person in final_list_of_people:
		print(person)

	# If an output file is desired, send the results to save_results.
	if output_file is not 0:
		save_results(final_list_of_people,output_file)


def sanitize_results(search_results):
	print("{0}[+] Sanitizing List...{1}".format(green_text,end_text))

	# Remove all of the HTML and non-Name portions of the result title
	for person in search_results:
		person = re.sub("<.*?>", "", person)
		person = re.sub("\|.*", "", person)
		person = re.sub(" - .*", "", person)
		person = re.sub(" at .*", "", person)
		people.append(person)

		# Remove all of the "Top Jobs at $Company" etc type results
		for person in people:
			if ("Best" in person or "Jobs" in person or "Hiring" in person or 
				"Top" in person or "hiring" in person or "Salaries" in person):
				people.remove(person)

		# Make sure each person is only in the list once
		for person in people:
			if person not in final_list_of_people:
				final_list_of_people.append(person)

	# Pass the clean results back to the scrape_linkedin function
	return final_list_of_people


def save_results(final_list_of_people,output_file):
	f = open(output_file, "w+")
	for person in final_list_of_people:
		f.write("{0}\n".format(person))
	f.close()
	print("{0}[+] Results saved to {1}{2}".format(green_text,output_file,end_text))


# Set up Argparse, 
progdesc = """Scrape LinkedIn via Google Dorks. Collect employee names from LinkedIn Profiles
				using Google advanced search operators. Filters results to give just the 
				first and last name (in most cases). Note that you need a Google CSE API Key
				(free) which limits you to 1,000 queries per month. """

parser = argparse.ArgumentParser(description=progdesc)
parser.add_argument('-c', metavar='Company', help='Company Name')
parser.add_argument('-o', metavar='Output File', default=0, help="Output Location")
parser.add_argument('-r', metavar='Results', default=20, 
					help="Results to return. Valid options: 10, 20, 30, 40, 50, and 100")
args = parser.parse_args()


# Ensure the Pages value is valid. Currently only these values are allowed by Google Search
if args.r:
	if int(args.r) in [10,20,30,40,50,100]:
		goog_results = args.r
	else:
		print("You must enter a valid number of pages to search: 10, 20, 30, 40, 50, 100")
		exit()

#Check to see if an output file has been defined
if args.o is not 0:
	output_file = args.o

# Ensure the user enters a company value.
if args.c:
	company = args.c
else:
	parser.help()
	exit()

# Send the user-supplied values to the scrape_linkedin function 
print("{0}ScrapedIN: An OSINT Tool for LinkedIn via Google Advanced Search{1}".format(green_text,end_text))
scrape_linkedin(company,goog_results,output_file)

