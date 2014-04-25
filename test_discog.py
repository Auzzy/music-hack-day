import discog
import mwsiteext

site = mwsiteext.Site()

album_page_names = discog.parse_discog_page(site, "The Verve discography")
for album_page_name in album_page_names:
	print album_page_name.encode('utf-8')
'''
album_page_names = discog.parse_discog_page(site, "Godsmack discography")
for album_page_name in album_page_names:
	print album_page_name
'''
