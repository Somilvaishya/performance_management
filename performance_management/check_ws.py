import frappe

def check_workspaces():
	frappe.init(site="workspace.test", sites_path="sites")
	frappe.connect()
	ws = frappe.get_all("Workspace", fields=["name", "label", "parent_page"])
	for w in ws:
		print(f"Name: {w.name}, Label: {w.label}, Parent: {w.parent_page}")

if __name__ == "__main__":
	check_workspaces()
