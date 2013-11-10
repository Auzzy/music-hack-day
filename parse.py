import re

import mwsiteext
site = mwsiteext.Site("en.wikipedia.org")

class Discog(object):
	def __init__(self, section, page):
		self.section = section
		self.page = page


def get_section(page_name, section_name):
	sections = site.parse_page(page_name, props=["sections"])["sections"]
	section_title_map = {section["line"]:section["index"] for section in sections}
	section_number = section_title_map.get(section_name, None)
	if not section_number:
		return None
	return site.parse_page(page_name, section_number, props=["wikitext"])["wikitext"]["*"]

def get_discog_page(artist_page_name, discogs_section):
	expanded_discogs_section = site.expandtemplates(discogs_section, artist_page_name)
	if expanded_discogs_section == discogs_section:
		return None

	template_re = re.search(r"(?P<template><div.*<\/div>)", expanded_discogs_section)
	template_text = template_re.group("template")
	return site.parse_text(artist_page_name, template_text, props=["links"])["links"][0]["*"]

def get_discog_section(artist_page_name):
	return get_section(artist_page_name, "Discography")

def get_discog_page(artist_page_name):
	discogs_section = get_discog_section(artist_page_name)
	if discogs_section:
		discogs_page = get_discog_page(artist_page_name, discogs_section)
		return Discog(discogs_section, discogs_page)


# artist_page_name = "The Verve"
artist_page_name = "Depswa"

"""
html = site.api("expandtemplates", text=discogs_section, title="The Verve")
print html
print

# print site.api("parse", text=html, title="The Verve", prop="links")["parse"]["links"]
"""
