#!/bin/python


import argparse
import PyPDF2


def get_args():

	parser = argparse.ArgumentParser()
	parser.add_argument("-f", dest="file", action="store")
	parser.add_argument("--file", dest="file", action="store")
	parser.add_argument("-o", dest="output", action="store")
	parser.add_argument("--output", dest="output", action="store")
	args = parser.parse_args()

	return args


def extract_urls_from_pdf(pdf_file):

	links = []

	file_obj = open(pdf_file, "rb")
	pdf_reader = PyPDF2.PdfFileReader(file_obj)
	pages = pdf_reader.getNumPages()

	key = "/Annots"
	uri = "/URI"
	ank = "/A"

	for page in range(pages):

		sliced = pdf_reader.getPage(page)
		page_obj = sliced.getObject()

		if key in page_obj.keys():
			ann = page_obj[key]

			for a in ann:
				u = a.getObject()

				if uri in u[ank].keys():
					link = u[ank][uri]
					links.append(link)

	return links


def write_file(data, output):

	with open(output, "a") as write_file:
		for item in data:
			write_file.write(item + "\n")


def main():

	pdf_file = get_args().file
	output = get_args().output

	urls = extract_urls_from_pdf(pdf_file)

	write_file(urls, output)


if __name__ == "__main__":
	main()
