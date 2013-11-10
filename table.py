from bs4 import BeautifulSoup
import util
import mwsiteext
site = mwsiteext.Site("en.wikipedia.org")

SECTION_NAMES = ["albums", "singles"]

def extract_page_names(cells):
	page_names = []
	for cell in cells:
		link = cell.find("a")
		if link and "title" in link.attrs:
			page_names.append(link["title"])
	return page_names

def parse_single_row_headers(headers, header_row):
	cols = {header.string.lower():index for index,header in enumerate(headers)}
	return cols,len(cols),header_row

def parse_multi_row_headers(headers, header_row):
	cols = {}
	header_count = 0
	for header in headers:
		if "rowspan" in header.attrs:
			cols[header.string.lower()] = header_count
			header_count += 1
		else:
			sub_header_row = header_row.find_next_sibling("tr")
			sub_headers = sub_header_row.find_all("th", scope="col")
			header_count += len(sub_headers)
	return cols,header_count,sub_header_row

def is_multi_row_header(headers):
	for header in headers:
		if "rowspan" in header.attrs and header["rowspan"] != "1":
			return True
	return False

def parse_table(table):
	header_row = table.tr
	headers = header_row("th", scope="col")
	parse_headers = parse_multi_row_headers if is_multi_row_header(headers) else parse_single_row_headers
	cols,header_count,final_header_row = parse_headers(headers, header_row)
	
	name_col = cols["title"]
	name_cells = []
	for row in final_header_row.find_next_siblings("tr"):
		cells = row.find_all(["th", "td"])
		if len(cells) == header_count:
			name_cells.append(cells[name_col])
	
	return extract_page_names(name_cells)

def parse_section(site, page_name, section_name):
	section_html = util.get_section(site, page_name, section_name, output_wikitext=False).encode("utf-7")
	section_soup = BeautifulSoup(section_html)
	page_names = []
	for table in section_soup.find_all("table"):
		page_names.extend(parse_table(table))
	return page_names

page_name = "The Verve discography"
sections = util.get_sections(site, page_name)
album_page_names = []
for section_name in SECTION_NAMES:
	if section_name in sections:
		album_page_names.extend(parse_section(site, page_name, sections[section_name]))

for album_page_name in album_page_names:
	print album_page_name
