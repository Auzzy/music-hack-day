import re

import discog
import album
import util

TEMPLATE_RE = re.compile(r"(?P<template><div.*<\/div>)")

def _get_discog_page_name(site, artist_page_name, discogs_section):
	expanded_discogs_section = site.expandtemplates(discogs_section, artist_page_name)
	if expanded_discogs_section == discogs_section:
		return None

	template_re = TEMPLATE_RE.search(expanded_discogs_section)
	if template_re:
		template_text = template_re.group("template")
		link_obj = site.parse_text(artist_page_name, template_text, props=["links"])["links"][0]
		if "exists" in link_obj:
			return link_obj["*"]
	return None

def _get_discog_section(site, artist_page_name):
	return util.get_section(site, artist_page_name, "Discography")

def parse_artist_page(site, artist_page_name):
	discogs_section = _get_discog_section(site, artist_page_name)
	if discogs_section:
		discogs_page = _get_discog_page_name(site, artist_page_name, discogs_section)
		return discogs_section,discogs_page
	return None,None
