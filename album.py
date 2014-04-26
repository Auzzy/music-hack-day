import re

from bs4 import BeautifulSoup

import util
import htmlutil

QUOTED_RE = re.compile("\"(?P<quoted>.*?)\"")
LENGTH_RE = re.compile("\d?\d[:.][0-5]\d")

VIDEO_STRINGS = ["dvd", "vhs", "video"]

def _remove_length(track_name):
	split_text = track_name.rsplit('-', 1)
	if len(split_text) == 1:
		return track_name
	
	name,length = split_text
	return name.strip() if LENGTH_RE.search(length) else track_name

def _get_quoted_text(cell):
	text = ''.join(cell.stripped_strings)
	quoted_re = QUOTED_RE.search(text)
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
		track_name = _remove_length(track_name)
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

def _is_video(section_name):
	for video_str in VIDEO_STRINGS:
		if video_str in section_name:
			return True
	return False

def prepare_tracklist_section(site, track_section_markup):
	sub_section_names = util.map_sub_section_names(site, track_section_markup)
	for sub_section_name in sub_section_names.keys()[:]:
		if _is_video(sub_section_name):
			video_section = util.get_sub_section(site, track_section_markup, sub_section_names[sub_section_name])
			if video_section:
				video_section_start = track_section_markup.index(video_section)
				track_section_markup = track_section_markup[:video_section_start] + track_section_markup[video_section_start + len(video_section):]
				del sub_section_names[sub_section_name]
	return track_section_markup,sub_section_names

def _get_track_listing_section(site, page_name):
	section_name = util.find_section_name(site, page_name, ["track listing", "track listings"])
	section_text = util.get_section(site, page_name, section_name) if section_name else None
	return section_name, section_text

def parse_tracklist(site, page_name):
	tracks = set()
	track_section_name,track_section_text = _get_track_listing_section(site, page_name)
	if track_section_text:
		track_section_markup,sub_section_names = prepare_tracklist_section(site, track_section_text)
		
		track_section_html = site.parse_text(track_section_markup)
		track_section = BeautifulSoup(track_section_html)
		tracklist_tables = track_section("table", class_="tracklist")
		if tracklist_tables:
			for tracklist_table in tracklist_tables:
				tracks.update(parse_tracklist_table(tracklist_table))
		else:
			for sub_section_name in sub_section_names:
				sub_section_html = util.get_sub_section(site, track_section_markup, sub_section_names[sub_section_name], False)
				tracks.update(parse_tracklist_section(BeautifulSoup(sub_section_html)))
	
	return tracks
