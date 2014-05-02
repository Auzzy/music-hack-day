_NAMELESS = None

def _parse_page_func(site, page_name):
	def parse(*args, **kwargs):
		page = page_name if "subject" not in kwargs else kwargs["subject"]
		if "subject" in kwargs:
			del kwargs["subject"]
		return site.parse_page(page, *args, **kwargs)
	return parse

def _parse_text_func(site, section_text):
	def parse(*args, **kwargs):
		text = section_text if "subject" not in kwargs else kwargs["subject"]
		if "subject" in kwargs:
			del kwargs["subject"]
		return site.parse_text(text, *args, **kwargs)
	return parse

def _get_nameless_section(parse_func, output_wikitext):
	wikitext = parse_func(props=["wikitext"])
	sections = parse_func(props=["sections"])["sections"]
	if len(sections) == 1:
		section_end = len(wikitext)
	else:
		section_end = sections[0]["byteoffset"] if sections[0]["byteoffset"] != 0 else sections[1]["byteoffset"]
	section_wikitext = wikitext[:section_end]
	if output_wikitext:
		return section_wikitext
	else:
		return parse_func(subject=section_wikitext, props=["text"])


def _get(parse_func, section_name, output_wikitext):
	if section_name == _NAMELESS:
		return _get_nameless_section(parse_func, output_wikitext)

	sections = parse_func(props=["sections"])["sections"]
	section_title_map = {section["line"]:section["index"] for section in sections}
	section_number = section_title_map.get(section_name, None)
	if not section_number:
		return None
	fmt = "wikitext" if output_wikitext else "text"
	return parse_func(section_number, props=[fmt])

def _get_names(parse_func):
	sections = parse_func(props=["sections"])["sections"]
	names_dict = {}
	for section in sections:
		names_dict[section["line"].lower()] = _NAMELESS if section["byteoffset"] == 0 else section["line"]
	return names_dict

def _find_name(parse_func, names):
	page_names = _get_names(parse_func)
	for name in names:
		if name in page_names:
			return page_names[name]
	return None

def _lookup_names(parse_func, names):
	page_names = _get_names(site, parse_func)
	names_dict = {}
	for name in names:
		if name in page_names:
			names_dict[name] = page_names[name]
	return names_dict




def get_section(site, page_name, section_name, output_wikitext=True):
	"""
	Retrieves the full text of the named section. The output will be in
	wikitext or HTML, as determined by the "output_wikitext" variable.
	"""
	return _get(_parse_page_func(site, page_name), section_name, output_wikitext)

def get_sub_section(site, section_text, section_name, output_wikitext=True):
	"""
	Parses the given wikitext to find the section with the given name, and
	return its text. The output will be in wikitext or HTML, as determined
	by the "output_wikitext" variable.
	"""
	return _get(_parse_text_func(site, section_text), section_name, output_wikitext)

def map_section_names(site, page_name):
	"""
	Maps the lower case form of each section name in the given page to its
	true form.
	"""
	return _get_names(_parse_page_func(site, page_name))

def map_sub_section_names(site, section_text):
	"""
	Maps the lower case form of each section name in the given wikitext to
	its true form.
	"""
	return _get_names(_parse_text_func(site, section_text))

def find_section_name(site, page_name, names):
	"""
	Retrieves the first valid section name for the given page in the provided
	list of names.
	"""
	return _find_name(_parse_page_func(site, page_name), names)

def find_sub_section_name(site, section_text, names):
	"""
	Retrieves the first valid section name for the given wikitext in the
	provided list of names.
	"""
	return _find_name(_parse_text_func(site, section_text), names)

def lookup_section_names(site, page_name, names):
	return _lookup_names(_parse_page_func(site, page_name), names)

def lookup_sub_section_names(site, section_text, names):
	return _lookup_names(_parse_text_func(site, section_text), names)
