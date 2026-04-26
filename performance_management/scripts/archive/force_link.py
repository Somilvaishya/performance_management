import frappe

def force_link():
	frappe.init(site="workspace.test", sites_path="sites")
	frappe.connect()
	
	parent = "Performance Management"
	child = "Performance User Dashboard"
	
	# Clear existing links that might be broken
	frappe.db.sql(f"DELETE FROM `tabWorkspace Link` WHERE parent='{parent}' AND label='User Dashboard'")
	
	# Insert the link bypassing validation
	# We use idx=6 because there are 5 links now
	frappe.db.sql(f"""
		INSERT INTO `tabWorkspace Link` 
		(name, parent, parenttype, parentfield, type, label, link_type, link_to, onboard, idx, creation, modified, owner, modified_by)
		VALUES 
		(REPLACE(UUID(), '-', ''), '{parent}', 'Workspace', 'links', 'Link', 'User Dashboard', 'Page', '{child}', 1, 6, NOW(), NOW(), 'Administrator', 'Administrator')
	""")
	
	frappe.db.commit()
	print(f"Force-linked {child} to {parent} sidebar.")

if __name__ == "__main__":
	force_link()
