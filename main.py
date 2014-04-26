import re

import artist
import discog
import album
import util
import mwsiteext

def parse_pages(site, artist_page, discog_page, album_pages):
	print "ARTIST PAGE: " + artist_page
	discog_section = None
	if not discog_page:
		discog_section,discog_page = artist.parse_artist_page(site, artist_page)
	
	if discog_section or discog_page:
		album_page_names = discog.parse_discog(site, artist_page, discog_section, discog_page)
		album_page_names.update(album_pages)
		
		tracks = set()
		for album_page_name in album_page_names:
			print "ALBUM PAGE NAME: " + album_page_name.encode('utf-8')
			tracks.update(album.parse_tracklist(site, album_page_name))
		
		print "TRACKS"
		for track in sorted(tracks):
			print track.encode('utf-8')


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
	# return page_title_map[discog_name] if discog_name in page_title_map else None
	return page_title_map.get(discog_name)

def filter_artist_page(page_title_map, artist_name):
	band_name = "{artist} (band)".format(artist=artist_name)
	# return page_title_map[artist_name] if artist_name in page_title_map else None
	return page_title_map[band_name] if band_name in page_title_map else page_title_map.get(artist_name)

def filter_search_results(page_title_map, artist_name):
	artist_page = filter_artist_page(page_title_map, artist_name)
	discog_page = filter_discog_page(page_title_map, artist_name)
	album_pages = filter_album_pages(page_title_map, artist_name)
	return artist_page, discog_page, album_pages

def search_artist(site, artist_name):
	query = "intitle:{artist}".format(artist=artist_name)
	page_titles = [result["title"] for result in site.search(query, what="text")]
	page_title_map = {title.lower():title for title in page_titles}
	return filter_search_results(page_title_map, artist_name.lower())

def query(artist_name, title_name):
	site = mwsiteext.Site()
	artist_page, discog_page, album_pages = search_artist(site, artist_name)
	parse_pages(site, artist_page, discog_page, album_pages)
