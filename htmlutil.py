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

def expand_table(table):
	if table("tbody"):
		tbody = table.tbody.extract()
		for row in tbody:
			table.append(row)
	
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
	for row in table("tr"):
		# row_headers = row("th", scope="col")
		row_headers = row(th_scope)
		if row_headers:
			header_row = row
			headers = row_headers
	
	header_text = []
	for header in headers:
		for ref in header(class_="reference"):
			ref.extract()
		header_text.append(list(header.stripped_strings)[0])
	cols = {header.lower():index for index,header in enumerate(header_text)}

	return cols,header_row
