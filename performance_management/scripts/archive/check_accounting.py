import frappe
import json

def check_accounting():
	frappe.init(site="workspace.test", sites_path="sites")
	frappe.connect()
	try:
		ws = frappe.get_doc("Workspace", "Accounting")
		for l in ws.links:
			print(f"Label: {l.label}, Link Type: {l.link_type}, Link To: {l.link_to}")
	except:
		print("Accounting not found")

if __name__ == "__main__":
	check_accounting()
