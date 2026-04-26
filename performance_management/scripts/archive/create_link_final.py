import frappe

def create_standard_link():
	frappe.init(site="workspace.test", sites_path="sites")
	frappe.connect()
	
	page_title = "PM User Dashboard"
	page_id = "pm-user-dashboard"
	
	# 1. Create a dummy Page if it doesn't exist
	# This satisfies the Workspace Link validation
	if not frappe.db.exists("Page", page_id):
		frappe.get_doc({
			"doctype": "Page",
			"name": page_id,
			"page_name": page_id,
			"title": page_title,
			"module": "Performance Management",
			"standard": "Yes",
			"roles": [{"role": "All"}]
		}).insert(ignore_permissions=True)
		print(f"Created Page {page_id}")
	
	# 2. Update the parent workspace sidebar
	parent_name = "Performance Management"
	if frappe.db.exists("Workspace", parent_name):
		parent = frappe.get_doc("Workspace", parent_name)
		
		# Remove old attempts
		frappe.db.sql(f"DELETE FROM `tabWorkspace Link` WHERE parent='{parent_name}' AND label='User Dashboard'")
		
		# Add standard link
		parent.append("links", {
			"type": "Link",
			"label": "User Dashboard",
			"link_type": "Page",
			"link_to": page_id,
			"onboard": 1,
			"idx": 2 # Near top
		})
		parent.save(ignore_permissions=True)
		print(f"Added sidebar link to {parent_name}")

	# 3. Ensure the child Workspace has matching name for routing
	# Actually, the routing /app/pm-user-dashboard will hit the Workspace if it shares the name
	# I'll rename the child workspace to the slugified name if needed
	if frappe.db.exists("Workspace", "Performance User Dashboard"):
		frappe.rename_doc("Workspace", "Performance User Dashboard", page_id, force=True)
		print(f"Renamed Workspace to {page_id}")

	frappe.db.commit()

if __name__ == "__main__":
	create_standard_link()
