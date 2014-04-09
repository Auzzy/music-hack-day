import album
import mwsiteext

def print_results(tracks):
	print [track.encode('utf-8') for track in sorted(tracks)]

site = mwsiteext.Site()

print_results(album.parse_tracklist(site, "Urban Hymns"))
print_results(album.parse_tracklist(site, "Faceless"))