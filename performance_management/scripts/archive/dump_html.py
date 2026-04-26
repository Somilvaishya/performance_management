import frappe

def dump_html():
	frappe.init(site="workspace.test", sites_path="sites")
	frappe.connect()
	h = frappe.db.get_value("Custom HTML Block", "PM User Dashboard", "html")
	if h:
		with open("/tmp/check_html.txt", "w") as f:
			f.write(h)
		print(f"Dumped {len(h)} characters to /tmp/check_html.txt")
	else:
		print("PM User Dashboard block not found")

if __name__ == "__main__":
	dump_html()
