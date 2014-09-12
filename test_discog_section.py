import discog
import mwsiteext

site = mwsiteext.Site()

album_page_names = discog.parse_discog_section(site, "Curve (band)", "Discography")
for album_page_name in album_page_names:
	print album_page_name

'''
album_page_names = discog.parse_discog_section(site, "Depswa", "Discography")
for album_page_name in album_page_names:
	print album_page_name
'''
