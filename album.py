import re

from bs4 import BeautifulSoup

import util
import htmlutil

def _get_quoted_text(cell):
	text = ''.join(cell.stripped_strings)
	quoted_re = re.search("\"(?P<quoted>.*?)\"", text)
	return quoted_re.group("quoted") if quoted_re else None

def _extract_text(cells):
	"""
	Attempts to grab the name of the track from the given cell. First looks
	for a quoted string, and then extracts the text from any tags that it may be wrapped in
	Searches for a quoted string and uses that as its 
	"""
	track_names = []
	for cell in cells:
		container = cell
		text = _get_quoted_text(cell)
		if text:
			container = BeautifulSoup(text)
		link = container.find("a")
		container = link if link else container
		track_name = list(container.stripped_strings)[0]
		track_names.append(track_name)
	return track_names

def _is_length(row):
	"""
	Looks for the signs of a total_length row. The first cell (which is what
	this function detects) is of the form:
	
	 	<td align="right" colspan="3">
		<div style="width: 7.5em; text-align: left; padding-left: 10px;
		background-color: #eee; margin: 0;"><b>Total length:</b></div>
		</td>

	"""
	return row.td.div and row.td.div.string.startswith("Total length")
	# return row.td.get_text("", strip=True).startswith("Total length")

def _find_title_column_index(cols):
	title_col_index = None
	for title_col in TITLE_COLS:
		if title_col in cols:
			return cols[title_col]
	return None

def parse_tracklist_table(tracklist_table):
	"""
	Handles the table produced by the tracklist template. Grabs the title
	column from each row of the table and extracts the text.
	"""
	cols,header_row = htmlutil.get_table_headers(tracklist_table)
	title_col_index = cols["title"]
	
	track_titles = []
	if title_col_index:
		title_cells = [row(("th", "td"))[title_col_index] for row in header_row.find_next_siblings("tr") if not _is_length(row)]
		track_titles = _extract_text(title_cells)
	return track_titles

def parse_tracklist_section(section):
	"""
	Handles the "track listing" section of an album page. It currently looks
	for all ordered lists, and extracts the text contained as the track name.
	Sublists are ignored.
	"""
	lists = section("ol")
	track_list = set()
	for alist in lists:
		if alist.parent.name != "li":
			elements = alist("li", recursive=False)
			track_names = _extract_text(elements)
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
