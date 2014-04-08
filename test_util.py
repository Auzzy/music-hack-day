import util
import mwsiteext

site = mwsiteext.Site()

print util.get_sections(site, "The Verve discography")
album_section = util.get_section(site, "The Verve discography", "Albums").encode("utf-7")
print util.get_sub_sections(site, "The Verve discography", album_section)
print util.get_sub_section(site, "The Verve discography", album_section, "Studio albums")
