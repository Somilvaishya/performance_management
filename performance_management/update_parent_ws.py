import frappe
import json

def update_parent_workspace():
	frappe.init(site="workspace.test", sites_path="sites")
	frappe.connect()
	
	parent_ws = "Performance Management"
	child_ws = "Performance User Dashboard"
	
	if not frappe.db.exists("Workspace", parent_ws):
		print(f"Parent workspace {parent_ws} not found")
		return

	doc = frappe.get_doc("Workspace", parent_ws)
	
	# Check if child already linked
	already_linked = False
	for link in doc.links:
		if link.link_to == child_ws:
			already_linked = True
			break
	
	if not already_linked:
		doc.append("links", {
			"type": "Link",
			"label": "User Dashboard",
			"link_type": "Page",
			"link_to": child_ws,
			"onboard": 1
		})
		doc.save(ignore_permissions=True)
		frappe.db.commit()
		print(f"Linked {child_ws} to {parent_ws}")
	else:
		print(f"{child_ws} already linked to {parent_ws}")

if __name__ == "__main__":
	update_parent_workspace()
