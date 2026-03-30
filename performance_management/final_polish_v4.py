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
		doc.type = "Workspace" # Mandatory
		doc.links = []
		doc.shortcuts = []
		doc.number_cards = []
		doc.title = doc.label or admin_name
		
		# Fix roles
		doc.set("roles", [])
		doc.append("roles", {"role": "System Manager"})
		
		doc.save(ignore_permissions=True)
		print(f"Admin {admin_name} isolated.")

	# 2. Fix User Workspace: Top-level Sidebar
	current_user_name = user_name_old if frappe.db.exists("Workspace", user_name_old) else user_name_new
	
	if frappe.db.exists("Workspace", current_user_name):
		# Ensure name is clean
		if current_user_name != user_name_new and not frappe.db.exists("Workspace", user_name_new):
			frappe.rename_doc("Workspace", current_user_name, user_name_new, force=True)
			current_user_name = user_name_new
			
		doc = frappe.get_doc("Workspace", current_user_name)
		doc.type = "Workspace"
		doc.title = user_name_new
		doc.label = user_name_new
		doc.parent_page = "" # TOP LEVEL
		doc.public = 1
		doc.is_standard = 0
		
		# Set roles for visibility
		doc.set("roles", [])
		doc.append("roles", {"role": "All"})
		
		doc.save(ignore_permissions=True)
		print(f"User Dashboard {user_name_new} finalized.")

	frappe.db.commit()
	print("Final polish complete.")

if __name__ == "__main__":
	final_polish()
