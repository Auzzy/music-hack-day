from bs4 import BeautifulSoup,NavigableString,Tag

def _copy_tag(root, tag):
	if isinstance(tag, Tag):
		new_tag = root.new_tag(tag.name, **tag.attrs)
		for child in tag.children:
			new_child = _copy_tag(root, child)
			new_tag.append(new_child)
		return new_tag
	elif isinstance(tag, NavigableString):
		return root.new_string(tag)

def _handle_rowspan(root, row, cell, colnum):
	rows = int(cell["rowspan"])
	del cell["rowspan"]
	for next_row in row.find_next_siblings("tr", limit=rows-1):
		children_no_whitespace = next_row.find_all(("td", "th"), recursive=False)
		cell_copy = _copy_tag(root, cell)
		if colnum < len(children_no_whitespace):
			children_no_whitespace[colnum].insert_before(cell_copy)
		else:
			children_no_whitespace[-1].insert_after(cell_copy)

def _handle_colspan(root, cell, cols):
	del cell["colspan"]
	for num in range(cols-1):
		cell_copy = _copy_tag(root, cell)
		cell.insert_after(cell_copy)

def normalize_table(table):
	# Some versions of BeautifulSoup seem to inject this tbody tag and some
	# don't. This flattens its rows into the tap-level table if it's present.
	if table("tbody"):
		tbody = table.tbody.extract()
		for row in tbody:
			table.append(row)
	
	# It can be assumed the first row of a table is a header row. This ensures
	# it uses header (th) tags.
	if not table("th"):
		first_row = table.find_next("tr")
		for cell in first_row("td"):
			cell.name = "th"
	
	root = list(table.parents)[-1]
	for row in table:
		colnum = 0
		for cell in row:
			if isinstance(cell, Tag):
				if "rowspan" in cell.attrs:
					_handle_rowspan(root, row, cell, colnum)
				
				cols = int(cell.get("colspan", "1"))
				colnum += cols
				if "colspan" in cell.attrs:
					_handle_colspan(root, cell, cols)
	
	return table

def get_table_headers(table):
	def th_scope(tag):
		return tag.name == "th" and ("scope" not in tag.attrs or tag.attrs["scope"] == "col")

	headers = []
	header_row = None
	
	if table("th"):
		for row in table("tr"):
			# row_headers = row("th", scope="col")
			row_headers = row(th_scope)
			if row_headers:
				header_row = row
				headers = row_headers
	else:
		pass
	
	headers_text = []
	for header in headers:
		for ref in header(class_="reference"):
			ref.extract()
		headers_text.append(list(header.stripped_strings)[0])
	cols = {header_text.lower():index for index,header_text in enumerate(headers_text)}

	return cols,header_row
