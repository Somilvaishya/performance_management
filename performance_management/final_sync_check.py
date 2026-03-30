import frappe
from frappe.desk.desktop import get_workspace_sidebar_items

def final_sync_check():
	frappe.init(site="workspace.test", sites_path="sites")
	frappe.connect()
	
	sidebar_items = get_workspace_sidebar_items()
	# Link should be in the 'Performance Management' section
	found = False
	pm_ws = None
	for item in sidebar_items:
		if item.get('label') == 'Performance Management':
			pm_ws = item
			break
	
	if pm_ws:
		print(f"PM Sidebar Items: {[i.get('label') for i in pm_ws.get('links', [])]}")
		# Actually get_workspace_sidebar_items might only return top-level
		pass
	
	# Check the actual doc one last time
	doc = frappe.get_doc("Workspace", "Performance Management")
	labels = [l.label for l in doc.links]
	print(f"Database Labels for PM: {labels}")
	if "User Dashboard" in labels:
		print("SUCCESS: User Dashboard is in the database links.")
	else:
		print("FAILURE: User Dashboard is still missing from database.")

if __name__ == "__main__":
	final_sync_check()
