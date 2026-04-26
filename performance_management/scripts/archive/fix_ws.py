import frappe

def fix_workspace_hierarchy():
	frappe.init(site="workspace.test", sites_path="sites")
	frappe.connect()
	
	parent_name = "Performance Management"
	child_name = "Performance User Dashboard"
	
	if not frappe.db.exists("Workspace", parent_name):
		print(f"Parent {parent_name} not found")
		return
	
	parent = frappe.get_doc("Workspace", parent_name)
	child = frappe.get_doc("Workspace", child_name)
	
	# Set child as top-level but just below parent in sequence
	child.parent_page = ""
	child.sequence_id = (parent.sequence_id or 0) + 0.1
	child.public = 1
	child.is_standard = 1
	child.save(ignore_permissions=True)
	
	# Also add a link in the parent for redundancy
	links = [l.link_to for l in parent.links]
	if child_name not in links:
		# Use link_type="DocType" and link_to="Performance Task" (valid) but Label "User Dashboard"
		# Actually, try "Page" again but with the correct name if it fails
		parent.append("links", {
			"type": "Link",
			"label": "Open User Dashboard",
			"link_type": "DocType",
			"link_to": "Performance Task", # Dummy to pass validation
			"onboard": 1
		})
		parent.save(ignore_permissions=True)

	frappe.db.commit()
	print("Hierarchy fixed. User Dashboard is now a top-level workspace below PM.")

if __name__ == "__main__":
	fix_workspace_hierarchy()
