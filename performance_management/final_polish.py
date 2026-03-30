import frappe

def final_polish():
	frappe.init(site="workspace.test", sites_path="sites")
	frappe.connect()
	
	admin_ws_name = "Performance Management"
	user_ws_name = "pm-user-dashboard" # Current name after rename
	
	# 1. Clean up Admin Workspace: Remove all links and shortcuts, keep only custom blocks
	if frappe.db.exists("Workspace", admin_ws_name):
		admin_ws = frappe.get_doc("Workspace", admin_ws_name)
		admin_ws.links = []
		admin_ws.shortcuts = []
		admin_ws.number_cards = []
		# Ensure the Custom HTML Block is linked
		if not any(b.custom_html_block == "PM Admin Dashboard" for b in admin_ws.custom_blocks):
			admin_ws.append("custom_blocks", {
				"custom_html_block": "PM Admin Dashboard",
				"idx": 0
			})
		admin_ws.save(ignore_permissions=True)
		print(f"Cleaned up {admin_ws_name}")

	# 2. Fix User Dashboard Visibility:
	# Make it a top-level workspace with its own sidebar presence
	if frappe.db.exists("Workspace", user_ws_name):
		user_ws = frappe.get_doc("Workspace", user_ws_name)
		user_ws.parent_page = ""
		user_ws.public = 1
		user_ws.is_standard = 0 # Custom makes it show up better
		user_ws.label = "Performance User Dashboard" # Nice label
		user_ws.title = "Performance User Dashboard"
		# Set sequence to be right after Admin
		parent_seq = frappe.db.get_value("Workspace", admin_ws_name, "sequence_id") or 0
		user_ws.sequence_id = parent_seq + 0.1
		user_ws.save(ignore_permissions=True)
		print(f"Promoted {user_ws_name} to top-level")

	frappe.db.commit()

if __name__ == "__main__":
	final_polish()
