class PageLoader(object):
	@staticmethod
	def load(site, name):
		result = site.api("parse", page=name, prop=["text", "wikitext", "sections"])
		sections = PageLoader.load_sections(result["sections"])
	
	@staticmethod
	def load_sections(site, sections):
		end = -1
		for section in reversed(result["sections"]):
			text = result["wikitext"][section["byteoffset"]:end]
			section = SectionLoader.load(section["line"], text)
			end = section["byteoffset"]

		intro = SectionLoader.load("Intro", result["wikitext"][:end])

class SectionLoader(object):
	@staticmethod
	def load(site, name, text):
		site.api("parse", text=text, contentmodel="wikitext", prop=["text", "wikitext", "links"])

class Block(object):
	def __init__(self, text, html):
		self.text = text
		self.html = html

if __name__ == "__main__":
	import mwsiteext

	PageLoader.load(mwsiteext.Site(), "Collide (band)")
