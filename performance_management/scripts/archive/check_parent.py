import frappe

def check_parent():
	frappe.init(site="workspace.test", sites_path="sites")
	frappe.connect()
	parent = frappe.get_doc("Workspace", "Performance Management")
	print(f"Parent: {parent.name}, Label: {parent.label}")
	print(f"Links in parent: {[l.label for l in parent.links]}")
	
	child = frappe.get_doc("Workspace", "Performance User Dashboard")
	print(f"Child: {child.name}, Parent Page: {child.parent_page}")

if __name__ == "__main__":
	check_parent()
