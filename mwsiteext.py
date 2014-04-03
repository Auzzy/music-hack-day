import mwclient

class Site(mwclient.Site):
	def __init__(self, host="en.wikipedia.org", *args, **kwargs):
		super(Site, self).__init__(host, *args, **kwargs)

	def _parse(self, *props, **kwargs):
		props_str = '|'.join(props)
		return self.api("parse", prop=props_str, **kwargs)["parse"]

	def parse_text(self, title, text, section=None, props=[]):
		kwargs = dict(title=title, text=text)
		if section:
			kwargs["section"] = section
		return self._parse(*props, **kwargs)

	def parse_page(self, page, section=None, props=[]):
		kwargs = dict(page=page)
		if section:
			kwargs["section"] = section
		return self._parse(*props, **kwargs)
