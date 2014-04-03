import re

from bs4 import BeautifulSoup

import util
import htmlutil

def strip_quotes(text):
	quoted_re = re.search("\"(?P<quoted>.*?)\"", text)
	return quoted_re.group("quoted") if quoted_re else text

def extract_text(cells):
	page_names = []
	for cell in cells:
		link = cell.find("a")
		container = link if link else cell
		page_name = list(container.stripped_strings)[0]
		page_name = strip_quotes(page_name)
		page_names.append(page_name)
	return page_names

def parse_tracklist_table(tracklist_table):
	cols,header_row = htmlutil.get_table_headers(tracklist_table)
	title_cells = [row(("th", "td"))[cols["title"]] for row in header_row.find_next_siblings("tr")]
	return extract_text(title_cells)

def parse_tracklist_section(section):
	lists = section("ol")
	track_list = set()
	for alist in lists:
		elements = alist("li", recursive=False)
		track_names = extract_text(elements)
		track_list.update(track_names)
	return track_list

def parse_tracklist(site, page_name):
	track_section_html = util.get_section(site, page_name, "Track listing", False)
	track_section = BeautifulSoup(track_section_html)

	tracklist_tables = track_section("table", class_="tracklist")
	tracks = set()
	if tracklist_tables:
		for tracklist_table in tracklist_tables:
			tracks.update(parse_tracklist_table(tracklist_table))
	else:
		track_section_markup = util.get_section(site, page_name, "Track listing")
		subsection_names = util.get_sub_sections(site, page_name, track_section_markup)
		for subsection_name in subsection_names:
			subsection_html = util.get_sub_section(site, page_name, track_section_markup, subsection_names[subsection_name], False)
			tracks.update(parse_tracklist_section(BeautifulSoup(subsection_html)))
	return tracks

if __name__ == "__main__":
	import mwsiteext

	site = mwsiteext.Site()
	# tracks = parse_tracklist(site, "A Northern Soul")
	tracks = parse_tracklist(site, "Urban Hymns")
	for track in sorted(tracks):
		print track.encode('utf-8')
