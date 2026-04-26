import frappe

def verify_and_fix():
	frappe.init(site="workspace.test", sites_path="sites")
	frappe.connect()
	
	page_id = "pm-user-dashboard"
	parent_ws = "Performance Management"
	
	# Check Page
	exists = frappe.db.exists("Page", page_id)
	print(f"Page {page_id} exists: {exists}")
	
	if not exists:
		# Force insert Page
		frappe.db.sql(f"INSERT INTO `tabPage` (name, page_name, title, module, standard, creation, modified, owner, modified_by) VALUES ('{page_id}', '{page_id}', 'User Dashboard', 'Performance Management', 1, NOW(), NOW(), 'Administrator', 'Administrator')")
		frappe.db.sql(f"INSERT INTO `tabHas Role` (name, parent, parenttype, parentfield, role, idx) VALUES (UUID(), '{page_id}', 'Page', 'roles', 'All', 1)")
		print("Force-inserted missing Page.")
	
	# Check Link
	link_exists = frappe.db.exists("Workspace Link", {"parent": parent_ws, "label": "User Dashboard"})
	print(f"Link 'User Dashboard' exists: {link_exists}")
	
	if not link_exists:
		# Insert with high Idx to avoid conflicts
		frappe.db.sql(f"""
			INSERT INTO `tabWorkspace Link` 
			(name, parent, parenttype, parentfield, type, label, link_type, link_to, onboard, idx, creation, modified, owner, modified_by)
			VALUES 
			(REPLACE(UUID(), '-', ''), '{parent_ws}', 'Workspace', 'links', 'Link', 'User Dashboard', 'Page', '{page_id}', 1, 8, NOW(), NOW(), 'Administrator', 'Administrator')
		""")
		print("Force-inserted missing Link at idx 8.")
	
	frappe.db.commit()
	
	# Verify again
	print(f"Post-fix Links: {[l.label for l in frappe.get_doc('Workspace', parent_ws).links]}")

if __name__ == "__main__":
	verify_and_fix()
