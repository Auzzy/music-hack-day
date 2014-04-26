import mwclient

class Site(mwclient.Site):
	def __init__(self, host="en.wikipedia.org", *args, **kwargs):
		super(Site, self).__init__(host, *args, **kwargs)

	def _parse(self, *props, **kwargs):
		props_str = '|'.join(props)
		return self.api("parse", prop=props_str, **kwargs)["parse"]
	
	def _parse_base(self, section, props, **kwargs):
		if section:
			kwargs["section"] = section
		if not props:
			props.append("text")
		
		result = self._parse(*props, **kwargs)

		if len(props) == 1 and props[0] in ["text", "wikitext"]:
			return result[props[0]]['*']
		else:
			return result

	def parse_text(self, text, section=None, props=[]):
		return self._parse_base(section, props, text=text, contentmodel="wikitext")

	def parse_page(self, page_name, section=None, props=[]):
		return self._parse_base(section, props, page=page_name)
