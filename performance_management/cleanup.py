import frappe

def cleanup():
	frappe.init(site="workspace.test", sites_path="sites")
	frappe.connect()
	
	parent_name = "Performance Management"
	if frappe.db.exists("Workspace", parent_name):
		# Remove redundant links
		frappe.db.sql(f"DELETE FROM `tabWorkspace Link` WHERE parent='{parent_name}' AND label='Open User Dashboard'")
		frappe.db.sql(f"DELETE FROM `tabWorkspace Link` WHERE parent='{parent_name}' AND label='Employee Dashboard'")
		
	frappe.db.commit()
	print("Cleanup complete.")

if __name__ == "__main__":
	cleanup()
