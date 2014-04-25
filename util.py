def _parse_page_func(site, page_name):
	def parse(*args, **kwargs):
		return site.parse_page(page_name, *args, **kwargs)
	return parse

def _parse_text_func(site, page_name, section_text):
	def parse(*args, **kwargs):
		return site.parse_text(page_name, section_text, *args, **kwargs)
	return parse

def _get_nameless_section(parse_func, output_wikitext):
	wikitext = parse_func(props=["wikitext"])
	sections = parse_func(props=["sections"])["sections"]
	if len(sections) == 1 :
		section_end = len(wikitext)
	else:
		section_end = sections[0]["byteoffset"] if sections[0]["byteoffset"] != 0 else sections[1]["byteoffset"]
	section_wikitext = wikitext[:section_end]
	if output_wikitext:
		return section_wikitext
	else:
		# TODO: This doesn't work right now, since I don't have access to site or page_name, and I need t parse
		# this wikitext. It might help for me to use contentmodel instead of title for parse_text
		return parse_func(props=["text"])


def _get(parse_func, section_name, output_wikitext):
	if not section_name:
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
	# return {section["line"].lower():section["line"] for section in sections}
	return {section["line"].lower():section["line"] for section in sections if section["byteoffset"] != 0}

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

def get_sub_section(site, page_name, section_text, section_name, output_wikitext=True):
	"""
	Parses the given wikitext to find the section with the given name, and
	return its text. The output will be in wikitext or HTML, as determined
	by the "output_wikitext" variable.
	"""
	return _get(_parse_text_func(site, page_name, section_text), section_name, output_wikitext)

def map_section_names(site, page_name):
	"""
	Maps the lower case form of each section name in the given page to its
	true form.
	"""
	return _get_names(_parse_page_func(site, page_name))

def map_sub_section_names(site, page_name, section_text):
	"""
	Maps the lower case form of each section name in the given wikitext to
	its true form.
	"""
	return _get_names(_parse_text_func(site, page_name, section_text))

def find_section_name(site, page_name, names):
	"""
	Retrieves the first valid section name for the given page in the provided
	list of names.
	"""
	return _find_name(_parse_page_func(site, page_name), names)

def find_sub_section_name(site, page_name, section_text, names):
	"""
	Retrieves the first valid section name for the given wikitext in the
	provided list of names.
	"""
	return _find_name(_parse_text_func(site, page_name, section_text), names)

def lookup_section_names(site, page_name, names):
	return _lookup_names(_parse_page_func(site, page_name), names)

def lookup_sub_section_names(site, page_name, section_text, names):
	return _lookup_names(_parse_text_func(site, page_name, section_text), names)


'''
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

def get_section_names(site, page_name):
	sections = site.parse_page(page_name, props=["sections"])["sections"]
	return {section["line"].lower():section["line"] for section in sections}

def get_sub_section_names(site, title, text):
	sections = site.parse_text(title, text, props=["sections"])["sections"]
	return {section["line"].lower():section["line"] for section in sections}

def find_section_name(site, page_name, section_names):
	page_section_names = get_section_names(site, page_name)
	for section_name in section_names:
		if section_name in page_section_names:
			return page_section_names[section_name]
	return None

def find_sub_section_name(site, title, text, sub_section_names):
	page_sub_section_names = get_sub_section_names(site, title, text)
	for sub_section_name in sub_section_names:
		if sub_section_name in page_sub_section_names:
			return page_sub_section_names[sub_section_name]
	return None

def lookup_section_names(site, page_name, section_names):
	page_section_names = get_section_names(site, page_name)
	names = {}
	for section_name in section_names:
		if section_name in page_section_names:
			names[section_name] = page_section_names[section_name]
	return names

def lookup_sub_section_names(site, title, text, sub_section_names):
	page_sub_section_names = get_sub_section_names(site, title, text)
	names = {}
	for sub_section_name in sub_section_names:
		if sub_section_name in page_sub_section_names:
			names[sub_section_name] = page_sub_section_names[sub_section_name]
	return names
'''
