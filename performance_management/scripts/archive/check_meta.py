import frappe

def check_meta():
	frappe.init(site="workspace.test", sites_path="sites")
	frappe.connect()
	meta = frappe.get_meta('Workspace Custom Block')
	for f in meta.fields:
		print(f"Field: {f.fieldname}, Type: {f.fieldtype}")

if __name__ == "__main__":
	check_meta()
