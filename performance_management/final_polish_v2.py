import frappe

def final_polish():
	frappe.init(site="workspace.test", sites_path="sites")
	frappe.connect()
	
	# Current names
	admin_ws_name = "Performance Management"
	user_ws_name = "pm-user-dashboard"
	
	# 1. Clean Admin Workspace
	if frappe.db.exists("Workspace", admin_ws_name):
		admin_ws = frappe.get_doc("Workspace", admin_ws_name)
		admin_ws.links = []
		admin_ws.shortcuts = []
		admin_ws.number_cards = []
		# Fix invalid roles: Use standard ones
		admin_ws.set("roles", [])
		admin_ws.append("roles", {"role": "System Manager"})
		admin_ws.save(ignore_permissions=True)
		print(f"Cleaned up {admin_ws_name}")

	# 2. Finalize User Workspace
	# We'll rename it to something clean and set it to top-level Sidebar
	if frappe.db.exists("Workspace", user_ws_name):
		# Rename to a nice clean name
		new_user_name = "User Dashboard"
		if not frappe.db.exists("Workspace", new_user_name):
			frappe.rename_doc("Workspace", user_ws_name, new_user_name, force=True)
			user_ws_name = new_user_name
		
		user_ws = frappe.get_doc("Workspace", user_ws_name)
		user_ws.label = "User Performance Dashboard"
		user_ws.title = "User Performance Dashboard"
		user_ws.parent_page = "" # TOP LEVEL SIDEBAR
		user_ws.public = 1
		user_ws.set("roles", [])
		user_ws.append("roles", {"role": "All"})
		# Ensure sequence is right after Admin
		admin_seq = frappe.db.get_value("Workspace", admin_ws_name, "sequence_id") or 0
		user_ws.sequence_id = admin_seq + 0.1
		user_ws.save(ignore_permissions=True)
		print(f"User Dashboard promoted and cleaned.")

	frappe.db.commit()

if __name__ == "__main__":
	final_polish()
