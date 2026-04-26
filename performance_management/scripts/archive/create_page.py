import frappe

def create_dummy_page():
	frappe.init(site="workspace.test", sites_path="sites")
	frappe.connect()
	
	page_name = "Performance User Dashboard"
	if not frappe.db.exists("Page", page_name):
		frappe.get_doc({
			"doctype": "Page",
			"name": page_name,
			"title": "User Dashboard",
			"module": "Performance Management",
			"standard": "Yes",
			"roles": [{"role": "All"}]
		}).insert(ignore_permissions=True)
		print(f"Created dummy Page {page_name}")
	else:
		print(f"Page {page_name} already exists")
		
	# Now update the sidebar link in the parent workspace to be a "Page" link
	parent_name = "Performance Management"
	parent = frappe.get_doc("Workspace", parent_name)
	
	# Clear previous attempts
	frappe.db.sql(f"DELETE FROM `tabWorkspace Link` WHERE parent='{parent_name}' AND label='User Dashboard'")
	
	# Add clear-cut link
	parent.append("links", {
		"type": "Link",
		"label": "User Dashboard",
		"link_type": "Page",
		"link_to": page_name,
		"onboard": 1,
		"idx": 2 # Right after Core Features (idx 1)
	})
	parent.save(ignore_permissions=True)
	
	frappe.db.commit()
	print("Sidebar link added successfully via Page proxy.")

if __name__ == "__main__":
	create_dummy_page()
