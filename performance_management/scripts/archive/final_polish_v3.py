import frappe

def final_polish():
	frappe.init(site="workspace.test", sites_path="sites")
	frappe.connect()
	
	admin_name = "Performance Management"
	user_name_old = "pm-user-dashboard"
	user_name_new = "User Performance Dashboard"
	
	# 1. Clean Admin Workspace: HTML block ONLY
	if frappe.db.exists("Workspace", admin_name):
		doc = frappe.get_doc("Workspace", admin_name)
		doc.links = []
		doc.shortcuts = []
		doc.number_cards = []
		doc.title = doc.label or admin_name # Ensure not None
		
		# Fix roles
		doc.set("roles", [])
		doc.append("roles", {"role": "System Manager"})
		
		doc.save(ignore_permissions=True)
		print(f"Admin {admin_name} isolated to HTML block.")

	# 2. Fix User Workspace: Top-level Sidebar
	current_user_name = user_name_old if frappe.db.exists("Workspace", user_name_old) else user_name_new
	
	if frappe.db.exists("Workspace", current_user_name):
		# Ensure name is clean
		if current_user_name != user_name_new and not frappe.db.exists("Workspace", user_name_new):
			frappe.rename_doc("Workspace", current_user_name, user_name_new, force=True)
			current_user_name = user_name_new
			
		doc = frappe.get_doc("Workspace", current_user_name)
		doc.title = user_name_new
		doc.label = user_name_new
		doc.parent_page = "" # Make it top-level
		doc.public = 1
		doc.is_standard = 0
		
		# Set roles for visibility
		doc.set("roles", [])
		doc.append("roles", {"role": "All"})
		
		doc.save(ignore_permissions=True)
		print(f"User Dashboard {user_name_new} set as top-level sibling.")

	frappe.db.commit()
	print("Final polish complete. Clearing cache...")

if __name__ == "__main__":
	final_polish()
