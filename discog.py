from bs4 import BeautifulSoup
import htmlutil
import util

SECTION_NAMES = ["albums", "singles"]

def extract_page_names(cells):
	page_names = []
	for cell in cells:
		link = cell.find("a")
		if link and "title" in link.attrs:
			page_names.append(link["title"])
	return page_names

def get_headers(table):
	headers = []
	header_row = None
	for row in table("tr"):
		row_headers = row("th", scope="col")
		if row_headers:
			header_row = row
			headers = row_headers
	
	header_text = []
	for header in headers:
		for ref in header(class_="reference"):
			ref.extract()
		header_text.append(list(header.stripped_strings)[0])
	cols = {header.lower():index for index,header in enumerate(header_text)}

	return cols,header_row

def parse_table(table):
	expanded_table = htmlutil.expand_table(table)
	cols,header_row = get_headers(expanded_table)
	name_cells = [row(("th", "td"))[cols["title"]] for row in header_row.find_next_siblings("tr")]
	return extract_page_names(name_cells)

def parse_section(site, page_name, section_name):
	section_html = util.get_section(site, page_name, section_name, output_wikitext=False).encode("utf-7")
	section_soup = BeautifulSoup(section_html)
	page_names = []
	for table in section_soup("table"):
		page_names.extend(parse_table(table))
	return page_names

def parse_discog_page(site, page_name):
	sections = util.get_sections(site, page_name)
	album_page_names = []
	for section_name in SECTION_NAMES:
		if section_name in sections:
			album_page_names.extend(parse_section(site, page_name, sections[section_name]))
	
	return album_page_names

def parse_discog_section(site, discog_section):
	pass

if __name__=="__main__":
	import mwsiteext
	site = mwsiteext.Site("en.wikipedia.org")
	album_page_names = parse_discog_page(site, "The Verve discography")
	for album_page_name in album_page_names:
		print album_page_name
