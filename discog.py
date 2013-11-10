import util

def parse_discog_page(site, page_name):
	sections_map = util.get_sections(page_name)

	if "albums" in sections_map:
		albums_section = util.get_section(page_name, sections_map["album"])

def parse_discog_site(site, discog_section):
	pass
