def get_section(site, page_name, section_name, output_wikitext=True):
	sections = site.parse_page(page_name, props=["sections"])["sections"]
	section_title_map = {section["line"]:section["index"] for section in sections}
	section_number = section_title_map.get(section_name, None)
	if not section_number:
		return None
	fmt = "wikitext" if output_wikitext else "text"
	return site.parse_page(page_name, section_number, props=[fmt])[fmt]["*"]

def get_sub_section(site, title, text, section_name, output_wikitext=True):
	sections = site.parse_text(title, text, props=["sections"])["sections"]
	section_title_map = {section["line"]:section["index"] for section in sections}
	section_number = section_title_map.get(section_name, None)
	if not section_number:
		return None
	fmt = "wikitext" if output_wikitext else "text"
	return site.parse_text(title, text, section_number, props=[fmt])[fmt]["*"]

def get_sections(site, page_name):
	sections = site.parse_page(page_name, props=["sections"])["sections"]
	return {section["line"].lower():section["line"] for section in sections}

def get_sub_sections(site, title, text):
	sections = site.parse_text(title, text, props=["sections"])["sections"]
	return {section["line"].lower():section["line"] for section in sections}


if __name__=="__main__":
	import mwsiteext
	site = mwsiteext.Site("en.wikipedia.org")

	print get_sections(site, "The Verve discography")
	album_section = get_section(site, "The Verve discography", "Albums").encode("utf-7")
	print get_sub_sections(site, "The Verve discography", album_section)
	print get_sub_section(site, "The Verve discography", album_section, "Studio albums")
