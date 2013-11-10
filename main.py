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

def get_artist_discog_page(artist_page_name):
	discogs_section = get_discog_section(artist_page_name)
	if discogs_section:
		discogs_page = get_discog_page(artist_page_name, discogs_section)
		return Discog(discogs_section, discogs_page)

def filter_album_pages(page_title_map, artist_name):
	def search(title, search_strs):
		for search_str in search_strs:
			if search_str in title:
				return True
		return False

	album_disambig_str = " ({artist} album)".format(artist=artist_name)
	ep_disambig_str = " ({artist} ep)".format(artist=artist_name)
	song_disambig_str = " ({artist} song)".format(artist=artist_name)
	search_strs = [album_disambig_str, ep_disambig_str, song_disambig_str]
	return [page_title_map[page_title] for page_title in page_title_map if search(page_title, search_strs)]

def filter_discog_page(page_title_map, artist_name):
	discog_name = "{artist} discography".format(artist=artist_name)
	return page_title_map[discog_name] if discog_name in page_title_map else None

def filter_artist_page(page_title_map, artist_name):
	return page_title_map[artist_name] if artist_name in page_title_map else None

def filter_search_results(page_title_map, artist_name):
	artist_page = filter_artist_page(page_title_map, artist_name)
	discog_page = filter_discog_page(page_title_map, artist_name)
	album_pages = filter_album_pages(page_title_map, artist_name)
	return artist_page, discog_page, album_pages

def search_artist(artist_name):
	query = "intitle:{artist}".format(artist=artist_name)
	page_titles = [result["title"] for result in site.search(query, what="text")]
	page_title_map = {title.lower():title for title in page_titles}
	
	artist_page, discog_page, album_pages = filter_search_results(page_title_map, artist_name.lower())

	discog = get_artist_discog_page(artist_page)
	print discog.page
	print discog.section
	

def query(artist_name, title_name):
	search_artist(artist_name)

if __name__=="__main__":
	query("Depswa", "Two Angels and a Dream")
