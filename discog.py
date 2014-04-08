from bs4 import BeautifulSoup
import htmlutil
import util

SECTION_NAMES = ["albums", "singles"]
TITLE_COLS = ["title", "album details", "song"]

def extract_page_names(cells):
	page_names = []
	for cell in cells:
		link = cell.find("a")
		if link and "title" in link.attrs:
			page_names.append(link["title"])
	return page_names

def _find_title_column_index(cols):
	title_col_index = None
	for title_col in TITLE_COLS:
		if title_col in cols:
			return cols[title_col]
	return None

def parse_table(table):
	table = htmlutil.expand_table(table)
	cols,header_row = htmlutil.get_table_headers(table)
	title_col_index = _find_title_column_index(cols)

	page_names = []
	if title_col_index:
		name_cells = [row(("th", "td"))[title_col_index] for row in header_row.find_next_siblings("tr")]
		page_names = extract_page_names(name_cells)
	return page_names

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
