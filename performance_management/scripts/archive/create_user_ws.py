import frappe
import json

@frappe.whitelist()
def create_user_workspace():
	# frappe already connected if run via bench execute
	frappe.flags.in_import = True
	frappe.flags.in_patch = True
	frappe.conf.developer_mode = 1

	ws_name = "Performance User Dashboard"
	if frappe.db.exists("Workspace", ws_name):
		frappe.delete_doc("Workspace", ws_name, force=1, ignore_permissions=True)

	links = [
		{
			"type": "Link",
			"label": "My Performance Tasks",
			"link_type": "DocType",
			"link_to": "Performance Task",
			"onboard": 1
		},
		{
			"type": "Link",
			"label": "My Extension Requests",
			"link_type": "DocType",
			"link_to": "Task Extension Request",
			"onboard": 1
		}
	]

	blocks = [
		{
			"type": "header",
			"data": {
				"text": "My Performance Overview",
				"level": 2
			}
		},
		{
			"type": "custom_html",
			"data": {
				"html_name": "PM User Dashboard"
			}
		}
	]

	doc = frappe.get_doc({
		"doctype": "Workspace",
		"title": ws_name,
		"name": ws_name,
		"module": "Performance Management",
		"label": ws_name,
		"icon": "user",
		"type": "Workspace",
		"parent_page": "Performance Management",
		"is_standard": 1,
		"public": 1,
		"roles": [{"role": "All"}],
		"links": links,
		"content": json.dumps(blocks)
	})
	doc.insert(ignore_permissions=True)
	
	frappe.db.commit()
	print(f"Workspace {ws_name} created successfully!")

