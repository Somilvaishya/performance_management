import frappe

def finalize_visibility():
	frappe.init(site="workspace.test", sites_path="sites")
	frappe.connect()
	
	parent_name = "Performance Management"
	child_name = "Performance User Dashboard"
	
	if not frappe.db.exists("Workspace", parent_name):
		print("Parent not found")
		return
		
	parent = frappe.get_doc("Workspace", parent_name)
	child = frappe.get_doc("Workspace", child_name)
	
	# Ensure child is a sibling right below parent
	child.parent_page = ""
	child.public = 1
	child.module = parent.module
	child.is_standard = 1
	child.sequence_id = parent.sequence_id + 0.001
	child.roles = [{"role": "All"}] # Accessible to everyone
	
	# Force save bypassing standard hooks which might interfere
	child.save(ignore_permissions=True)
	
	# Also update parent's links to include it as a "DocType" link (hacky but shows in sidebar)
	# I'll use "Page" type link
	already_in_parent = any(l.label == "User Dashboard" for l in parent.links)
	if not already_in_parent:
		frappe.db.sql(f"""
			INSERT INTO `tabWorkspace Link` 
			(name, parent, parenttype, parentfield, type, label, link_type, link_to, onboard, idx, creation, modified, owner, modified_by)
			VALUES 
			(REPLACE(UUID(), '-', ''), '{parent_name}', 'Workspace', 'links', 'Link', 'User Dashboard', 'Page', '{child_name}', 1, 10, NOW(), NOW(), 'Administrator', 'Administrator')
		""")

	frappe.db.commit()
	print("Child workspace set as sibling and linked in parent sidebar.")

if __name__ == "__main__":
	finalize_visibility()
