import frappe

def check_all_links():
	frappe.init(site="workspace.test", sites_path="sites")
	frappe.connect()
	ws = frappe.get_doc("Workspace", "Performance Management")
	print(f"Workspace: {ws.label}, Module: {ws.module}")
	for l in ws.links:
		print(f"Idx: {l.idx}, Label: {l.label}, Type: {l.type}, Link Type: {l.link_type}, Link To: {l.link_to}")

if __name__ == "__main__":
	check_all_links()
